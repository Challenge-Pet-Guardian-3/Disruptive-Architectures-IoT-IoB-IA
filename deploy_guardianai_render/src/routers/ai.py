"""
Router de IA Generativa e Triagem Clínica Preventiva
"""
from fastapi import APIRouter
from src.schemas.chat import ChatRequest, ChatResponse
from src.schemas.pet import PetContextPayload
from src.schemas.insights import InsightsResponse
from src.services.chat_service import ChatService
from src.services.insights_service import InsightsService

ai_router = APIRouter(prefix="/ai", tags=["AI"])

@ai_router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest) -> ChatResponse:
    """
    Processa interação no chat clínico com contexto do animal e histórico multi-turnos.
    """
    return ChatService.processar_chat(request)

@ai_router.post("/insights", response_model=InsightsResponse)
async def insights_endpoint(pet: PetContextPayload) -> InsightsResponse:
    """
    Gera insights preventivos personalizados de acordo com porte e idade do animal.
    """
    return InsightsService.gerar_insights(pet)
