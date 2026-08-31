import logging
from typing import Optional, Type, TypeVar, Callable
from pydantic import BaseModel
# pyrefly: ignore [missing-import]
from google.genai import Client, types

from app.config import settings
from app.models.schemas import (
    PetContext,
    ChatResponse,
    InsightsResponse,
    TriageResponse,
    TrainingPlanResponse,
)
from app.prompts.system_prompts import (
    SYSTEM_INSTRUCTION_CLYVO_AI,
    build_user_prompt_with_context,
    build_insights_prompt,
    build_triage_prompt,
    build_training_prompt,
)
from app.services.rag_service import rag_service
from app.services.fallback_service import fallback_service

logger = logging.getLogger("clyvo_ai.gemini")

T = TypeVar("T", bound=BaseModel)

class GeminiService:
    """
    Orquestrador POO de IA Generativa (Google Gemini 3.5 Flash Lite) com RAG e Guardrails.
    Aplica Clean Code, SOLID (SRP, OCP e DIP) e DRY via despacho genérico tipado.
    """

    def __init__(self):
        self._client: Optional[Client] = None
        self._is_configured: bool = False
        self._initialize_client()

    def _initialize_client(self) -> None:
        """Inicializa o cliente GenAI de forma segura."""
        api_key = settings.GEMINI_API_KEY.strip()
        if api_key and api_key != "sua_chave_gemini_aqui":
            try:
                self._client = Client(api_key=api_key)
                self._is_configured = True
                logger.info(f"Google GenAI conectado com o modelo {settings.GEMINI_MODEL}.")
            except Exception as e:
                logger.warning(f"Falha ao inicializar SDK Google GenAI: {e}")

    def is_configured(self) -> bool:
        return self._is_configured

    def _execute_structured_inference(
        self,
        prompt: str,
        response_model: Type[T],
        fallback_factory: Callable[[], T],
        system_instruction: Optional[str] = None,
        temperature: float = 0.2
    ) -> T:
        """Pipeline genérico POO: executa inferência tipada com fallback resiliente."""
        if not self._is_configured or not self._client:
            return fallback_factory()

        try:
            config = types.GenerateContentConfig(
                temperature=temperature,
                response_mime_type="application/json",
                system_instruction=system_instruction
            )
            response = self._client.models.generate_content(
                model=settings.GEMINI_MODEL,
                contents=prompt,
                config=config
            )
            return response_model.model_validate_json(response.text.strip())
        except Exception as err:
            logger.error(f"Erro na inferência Gemini: {err}. Executando fallback.")
            return fallback_factory()

    async def generate_chat_response(
        self,
        pergunta: str,
        pet_context: Optional[PetContext] = None
    ) -> ChatResponse:
        """Gera resposta de chat unindo RAG vetorial + Gemini 3.5 Flash Lite + Guardrails."""
        rag_chunks = rag_service.buscar_contexto_relevante(pergunta, top_k=3)
        prompt = build_user_prompt_with_context(pergunta, pet_context, rag_chunks)
        return self._execute_structured_inference(
            prompt=prompt,
            response_model=ChatResponse,
            fallback_factory=lambda: fallback_service.process_chat(pergunta, pet_context),
            system_instruction=SYSTEM_INSTRUCTION_CLYVO_AI,
            temperature=0.2
        )

    async def generate_insights(self, pet_context: PetContext) -> InsightsResponse:
        """Gera insights preventivos automáticos baseados no perfil do Pet."""
        return self._execute_structured_inference(
            prompt=build_insights_prompt(pet_context),
            response_model=InsightsResponse,
            fallback_factory=lambda: fallback_service.generate_insights(pet_context),
            temperature=0.2
        )

    async def generate_triage(
        self,
        sintomas: str,
        pet_context: Optional[PetContext] = None
    ) -> TriageResponse:
        """Realiza triagem clínica de sintomas."""
        return self._execute_structured_inference(
            prompt=build_triage_prompt(sintomas, pet_context),
            response_model=TriageResponse,
            fallback_factory=lambda: fallback_service.process_triage(sintomas, pet_context),
            temperature=0.1
        )

    async def generate_training_plan(
        self,
        comando: str,
        nivel: str,
        pet_context: Optional[PetContext] = None
    ) -> TrainingPlanResponse:
        """Gera plano de treinamento positivo gamificado."""
        return self._execute_structured_inference(
            prompt=build_training_prompt(comando, nivel, pet_context),
            response_model=TrainingPlanResponse,
            fallback_factory=lambda: fallback_service.generate_training_plan(comando, nivel, pet_context),
            temperature=0.3
        )

gemini_service = GeminiService()
