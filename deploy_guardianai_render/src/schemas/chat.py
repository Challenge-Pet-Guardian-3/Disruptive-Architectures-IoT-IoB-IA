"""
Schemas Pydantic: Conversação e Chat da IA
"""
from typing import Optional, List
from pydantic import BaseModel, Field
from src.schemas.pet import PetContextPayload

class MensagemHistorico(BaseModel):
    sender: str = Field(..., description="Remetente da mensagem: 'user' ou 'assistant'/'model'")
    text: str = Field(..., description="Conteúdo textual da mensagem")

class ChatRequest(BaseModel):
    pergunta: str = Field(..., description="Dúvida, queixa ou relato enviado pelo tutor")
    petContext: Optional[PetContextPayload] = Field(default=None, description="Contexto biológico e clínico do pet ativo")
    historico: Optional[List[MensagemHistorico]] = Field(default=None, description="Histórico de mensagens recentes para memória conversacional")
    sessionId: Optional[str] = Field(default=None, description="Identificador único opcional da sessão")

class ChatResponse(BaseModel):
    resposta: str = Field(..., description="Resposta processada e sanitizada para visualização mobile")
    categoria: str = Field(default="saude", description="Categoria clínica: 'saude', 'nutricao', 'rotina', 'EMERGENCIA'")
    urgencia: str = Field(default="baixa", description="Classificação de gravidade: 'baixa', 'media', 'alta', 'EMERGENCIA'")
    acoes_recomendadas: Optional[List[str]] = Field(default=None, description="Orientações e checklist de ações sugeridas para o tutor")
    score_xp_sugerido: Optional[int] = Field(default=10, description="Pontos de experiência (gamificação PetGuardian)")
    origem_resposta: str = Field(default="Guardian AI (PetGuardian Care)", description="Identificador do mecanismo responsável pela geração da resposta")
