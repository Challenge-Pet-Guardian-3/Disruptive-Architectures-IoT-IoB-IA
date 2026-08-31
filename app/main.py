import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.models.schemas import (
    ChatRequest,
    ChatResponse,
    InsightsRequest,
    InsightsResponse,
    TriageRequest,
    TriageResponse,
    TrainingPlanRequest,
    TrainingPlanResponse,
    HealthCheckResponse,
    PetContext,
)
from app.services.rag_service import rag_service
from app.services.gemini_service import gemini_service

# Configuração de Logs
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("clyvo_ai.main")

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("🚀 Inicializando microserviço Guardian AI...")
    try:
        rag_service.initialize()
    except Exception as e:
        logger.warning(f"Aviso na inicialização do RAG: {e}")
    yield
    # Shutdown
    logger.info("🛑 Encerrando serviço de IA...")

app = FastAPI(
    title=settings.APP_TITLE,
    description=settings.APP_DESCRIPTION,
    version=settings.APP_VERSION,
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configuração de CORS (Essencial para React Native e Web)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------------------------------------------
# Health Check
# -------------------------------------------------------------
@app.get(
    "/health",
    response_model=HealthCheckResponse,
    tags=["Saúde do Sistema"],
    summary="Verificar status e saúde do microserviço"
)
@app.get(
    "/api/v1/health",
    response_model=HealthCheckResponse,
    include_in_schema=False
)
def health_check():
    return HealthCheckResponse(
        status="ONLINE",
        version=settings.APP_VERSION,
        gemini_configured=gemini_service.is_configured(),
        rag_documents_loaded=rag_service.get_total_documents_loaded()
    )

# -------------------------------------------------------------
# Chat Inteligente com Guardrails & Contexto do Pet
# -------------------------------------------------------------
@app.post(
    "/ai/chat",
    response_model=ChatResponse,
    tags=["Assistente IA"],
    summary="Conversar com a IA passando o contexto do Pet selecionado"
)
@app.post(
    "/api/v1/ai/chat",
    response_model=ChatResponse,
    include_in_schema=False
)
async def chat_with_ai(request: ChatRequest):
    """
    Recebe a pergunta do tutor e o contexto do animal ativo (nome, raça, porte, idade, castrado, histórico).
    Executa busca vetorial RAG no ChromaDB e gera resposta estruturada via Google Gemini Flash com Guardrails.
    """
    if not request.pergunta.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A pergunta não pode estar vazia."
        )

    return await gemini_service.generate_chat_response(
        pergunta=request.pergunta,
        pet_context=request.petContext
    )

# -------------------------------------------------------------
# Insights Preventivos Automáticos
# -------------------------------------------------------------
@app.post(
    "/ai/insights",
    response_model=InsightsResponse,
    tags=["Saúde Preventiva"],
    summary="Gerar recomendações preventivas automáticas por perfil do Pet"
)
@app.post(
    "/api/v1/ai/insights",
    response_model=InsightsResponse,
    include_in_schema=False
)
async def generate_pet_insights(request: InsightsRequest):
    """
    Gera cards com 3 recomendações preventivas (saúde, nutrição e rotina)
    adaptadas especificamente para a espécie, porte, idade e condição do pet.
    """
    pet_ctx = PetContext(
        nome=request.nome,
        raca=request.raca,
        dataNasc=request.dataNasc,
        idade=request.idade,
        porte=request.porte,
        sexo=request.sexo,
        castrado=request.castrado,
        peso=request.peso,
        alergias=request.alergias,
        medicamentos=request.medicamentos
    )
    return await gemini_service.generate_insights(pet_ctx)

# -------------------------------------------------------------
# Triagem de Sintomas e Emergência 24h
# -------------------------------------------------------------
@app.post(
    "/ai/triage",
    response_model=TriageResponse,
    tags=["Triagem Clínica"],
    summary="Triagem de sintomas com classificação de risco e alerta 24h"
)
@app.post(
    "/api/v1/ai/triage",
    response_model=TriageResponse,
    include_in_schema=False
)
async def triage_symptoms(request: TriageRequest):
    """
    Avalia relatos de sintomas, classifica a gravidade (VERDE, AMARELO, VERMELHO),
    indica se deve acionar clínica 24h e fornece primeiros socorros seguros.
    """
    return await gemini_service.generate_triage(
        sintomas=request.sintomas,
        pet_context=request.petContext
    )

# -------------------------------------------------------------
# Treinamento Positivo & Gamificação (+XP)
# -------------------------------------------------------------
@app.post(
    "/ai/training/plan",
    response_model=TrainingPlanResponse,
    tags=["Adestramento & Gamificação"],
    summary="Gerar plano de treino positivo gamificado com pontuação XP"
)
@app.post(
    "/api/v1/ai/training/plan",
    response_model=TrainingPlanResponse,
    include_in_schema=False
)
async def generate_training_plan(request: TrainingPlanRequest):
    """
    Gera passos práticos de adestramento positivo sem punição e
    atribui pontuação de experiência (XP) ao pet.
    """
    return await gemini_service.generate_training_plan(
        comando=request.comando_ou_objetivo,
        nivel=request.nivel_experiencia or "INICIANTE",
        pet_context=request.petContext
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host=settings.HOST, port=settings.PORT, reload=True)
