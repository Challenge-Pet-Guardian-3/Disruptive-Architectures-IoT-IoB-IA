from enum import Enum
from typing import Optional, List
from pydantic import BaseModel, Field

class PetPorteEnum(str, Enum):
    PEQUENO = "PEQUENO"
    MEDIO = "MEDIO"
    GRANDE = "GRANDE"

class UrgencyEnum(str, Enum):
    BAIXA = "BAIXA"
    MEDIA = "MEDIA"
    ALTA = "ALTA"
    EMERGENCIA = "EMERGENCIA"

class CategoryEnum(str, Enum):
    SAUDE = "SAUDE"
    NUTRICAO = "NUTRICAO"
    COMPORTAMENTO = "COMPORTAMENTO"
    ROTINA = "ROTINA"
    EMERGENCIA = "EMERGENCIA"
    GERAL = "GERAL"
    FORA_DE_ESCOPO = "FORA_DE_ESCOPO"

class PetContext(BaseModel):
    id: Optional[int] = Field(None, description="ID único do Pet")
    nome: Optional[str] = Field("Pet", description="Nome do animal de estimação")
    raca: Optional[str] = Field("SRD", description="Raça do animal")
    porte: Optional[str] = Field("MEDIO", description="Porte: PEQUENO, MEDIO ou GRANDE")
    dataNasc: Optional[str] = Field(None, description="Data de nascimento (YYYY-MM-DD)")
    idade: Optional[int] = Field(None, description="Idade em anos")
    sexo: Optional[str] = Field(None, description="Sexo: 'M' ou 'F'")
    castrado: Optional[bool] = Field(False, description="Se o pet é castrado")
    peso: Optional[str] = Field(None, description="Peso atual com unidade (ex: 12kg)")
    alergias: Optional[str] = Field(None, description="Alergias conhecidas")
    medicamentos: Optional[str] = Field(None, description="Medicamentos de uso contínuo")
    ultimaVacina: Optional[str] = Field(None, description="Data ou tipo da última vacina")
    ultimaConsulta: Optional[str] = Field(None, description="Data da última consulta clínica")

class ChatRequest(BaseModel):
    pergunta: str = Field(..., min_length=1, max_length=1000, description="Pergunta ou relato do tutor")
    petContext: Optional[PetContext] = Field(None, description="Contexto do pet ativo selecionado no Mobile")
    historicoMensagens: Optional[List[dict]] = Field(default_factory=list, description="Histórico de mensagens da conversa")

class ChatResponse(BaseModel):
    resposta: str = Field(..., description="Resposta amigável e explicativa da IA")
    categoria: CategoryEnum = Field(CategoryEnum.GERAL, description="Classificação temática da dúvida")
    urgencia: UrgencyEnum = Field(UrgencyEnum.BAIXA, description="Nível de urgência da situação")
    alerta_clinica_24h: bool = Field(False, description="Indica se deve sugerir atendimento veterinário de emergência 24h")
    acoes_recomendadas: List[str] = Field(default_factory=list, description="Lista de ações práticas sugeridas ao tutor")
    score_xp_sugerido: int = Field(0, description="Pontos de experiência (XP) sugeridos para gamificação")
    origem_resposta: str = Field("gemini_rag", description="Origem do processamento ('gemini_rag' ou 'fallback_rules')")

class PetInsight(BaseModel):
    titulo: str = Field(..., description="Título do insight preventivo")
    descricao: str = Field(..., description="Explicação detalhada da recomendação")
    categoria: str = Field(..., description="saude, nutricao, comportamento ou rotina")
    urgencia: str = Field("baixa", description="baixa, media ou alta")

class InsightsRequest(BaseModel):
    nome: Optional[str] = "Pet"
    raca: Optional[str] = "SRD"
    dataNasc: Optional[str] = None
    idade: Optional[int] = None
    porte: Optional[str] = "MEDIO"
    sexo: Optional[str] = None
    castrado: Optional[bool] = False
    peso: Optional[str] = None
    alergias: Optional[str] = None
    medicamentos: Optional[str] = None

class InsightsResponse(BaseModel):
    pet_nome: str
    insights: List[PetInsight]

class TriageRequest(BaseModel):
    sintomas: str = Field(..., min_length=2, description="Descrição dos sintomas do animal")
    tempo_sintomas: Optional[str] = Field(None, description="Há quanto tempo iniciaram os sintomas")
    petContext: Optional[PetContext] = None

class TriageResponse(BaseModel):
    classificacao: UrgencyEnum
    nivel_cor: str = Field(..., description="'VERDE', 'AMARELO' ou 'VERMELHO'")
    diagnostico_provavel_ou_orientacao: str
    deve_buscar_emergencia_24h: bool
    primeiros_socorros_seguros: List[str]
    o_que_nao_fazer: List[str]

class TrainingPlanRequest(BaseModel):
    comando_ou_objetivo: str = Field(..., description="Ex: 'Senta', 'Fica', 'Ansiedade ao sair de casa'")
    nivel_experiencia: Optional[str] = Field("INICIANTE", description="INICIANTE, INTERMEDIARIO ou AVANCADO")
    petContext: Optional[PetContext] = None

class TrainingPlanResponse(BaseModel):
    titulo: str
    duracao_sessao_minutos: int
    passos_praticos: List[str]
    dica_reforco_positivo: str
    pontos_xp_recompensa: int

class HealthCheckResponse(BaseModel):
    status: str
    version: str
    gemini_configured: bool
    rag_documents_loaded: int
