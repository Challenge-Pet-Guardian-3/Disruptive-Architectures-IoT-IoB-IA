"""
Router de IA Generativa, Triagem Clínica Preventiva e Persistência SQLite
"""
from typing import Optional
from fastapi import APIRouter, Query
from src.schemas.chat import (
    ChatRequest,
    ChatResponse,
    HistoricoResponse,
    AuditoriaResponse,
    MensagemBancoItem,
    AuditoriaBancoItem
)
from src.schemas.pet import PetContextPayload
from src.schemas.insights import InsightsResponse
from src.services.chat_service import ChatService
from src.services.insights_service import InsightsService
from src.repositories.chat_repository import ChatRepository

ai_router = APIRouter(prefix="/ai", tags=["AI"])

@ai_router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest) -> ChatResponse:
    """
    Processa interação no chat clínico com contexto do animal e histórico multi-turnos,
    persistindo automaticamente a conversa e a auditoria da triagem no SQLite.
    """
    return ChatService.processar_chat(request)

@ai_router.post("/insights", response_model=InsightsResponse)
async def insights_endpoint(pet: PetContextPayload) -> InsightsResponse:
    """
    Gera insights preventivos personalizados de acordo com porte e idade do animal.
    """
    return InsightsService.gerar_insights(pet)

@ai_router.get("/history", response_model=HistoricoResponse)
def buscar_historico_endpoint(
    session_id: Optional[str] = Query(None, description="Filtrar por ID da sessão"),
    pet_id: Optional[int] = Query(None, description="Filtrar por ID do pet"),
    limit: int = Query(50, ge=1, le=200, description="Limite máximo de mensagens")
) -> HistoricoResponse:
    """
    Consulta o histórico de mensagens gravadas no SQLite por sessão ou por pet.
    """
    dados = ChatRepository.buscar_historico(session_id=session_id, pet_id=pet_id, limit=limit)
    itens = [MensagemBancoItem(**row) for row in dados]
    return HistoricoResponse(total=len(itens), mensagens=itens)

@ai_router.get("/audit", response_model=AuditoriaResponse)
def listar_auditorias_endpoint(
    pet_id: Optional[int] = Query(None, description="Filtrar por ID do pet"),
    limit: int = Query(20, ge=1, le=100, description="Limite máximo de auditorias")
) -> AuditoriaResponse:
    """
    Consulta as últimas triagens clínicas auditadas no banco de dados SQLite.
    """
    dados = ChatRepository.listar_auditorias(pet_id=pet_id, limit=limit)
    itens = [AuditoriaBancoItem(**row) for row in dados]
    return AuditoriaResponse(total=len(itens), auditorias=itens)
