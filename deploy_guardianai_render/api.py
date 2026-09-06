import os
import unicodedata
from typing import Optional, List, Dict, Any
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from dotenv import load_dotenv

# Carrega variaveis locais do .env se disponivel
load_dotenv()

# Inicializacao do app FastAPI
app = FastAPI(
    title="PetGuardian / Clyvo Care — AI Microservice",
    description="API de IA Generativa para triagem clínica preventiva, nutrição e cuidados de pets.",
    version="1.0.0"
)

# Habilita CORS total para conexao com React Native Mobile e Web
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==============================================================================
# 1. BASES DE CONHECIMENTO DETERMINÍSTICAS (Zero Alucinação)
# ==============================================================================

BASE_ALIMENTOS_TOXICOS = {
    "chocolate": {
        "status": "toxico",
        "nivel_risco": "EMERGENCIA",
        "toxina": "Teobromina e Cafeína",
        "mecanismo": "Metabolização lenta pelo fígado de cães e gatos, hiperestimulação neurológica e cardiovascular.",
        "sintomas": "Taquicardia, tremores musculares, vômitos, diarreia, arritmias e convulsões.",
        "conduta_imediata": "Levar IMEDIATAMENTE a um hospital veterinário 24h. NÃO induzir vômito com água oxigenada ou sal em casa."
    },
    "cacau": {
        "status": "toxico",
        "nivel_risco": "EMERGENCIA",
        "toxina": "Teobromina concentrada",
        "mecanismo": "Toxicidade equivalente ao chocolate amargo puro.",
        "sintomas": "Convulsões, hipertermia, risco de parada cardiorrespiratória.",
        "conduta_imediata": "Emergência clínica imediata. Levar ao pronto-socorro veterinário 24h."
    },
    "uva": {
        "status": "toxico",
        "nivel_risco": "EMERGENCIA",
        "toxina": "Ácido tartárico e compostos nefrotóxicos",
        "mecanismo": "Provoca necrose tubular aguda nos rins mesmo em pequenas quantidades.",
        "sintomas": "Vômitos, letargia, dor abdominal e insuficiência renal aguda anúrica.",
        "conduta_imediata": "Emergência imediata. Requer fluidoterapia intravenosa e monitoramento renal hospitalar."
    },
    "uva-passa": {
        "status": "toxico",
        "nivel_risco": "EMERGENCIA",
        "toxina": "Ácido tartárico altamente concentrado",
        "mecanismo": "Potencial nefrotóxico ainda maior que o da uva fresca.",
        "sintomas": "Falência renal rápida, anúria e apatia.",
        "conduta_imediata": "Hospitalização imediata 24h."
    },
    "cebola": {
        "status": "toxico",
        "nivel_risco": "ALTO",
        "toxina": "Dissulfeto de alilpropila e compostos de enxofre",
        "mecanismo": "Oxidação da hemoglobina, formação de Corpúsculos de Heinz e anemia hemolítica severa.",
        "sintomas": "Fraqueza intensa, gengivas pálidas ou azuladas, urina escura e respiração ofegante.",
        "conduta_imediata": "Consulta veterinária urgente para avaliação hematológica."
    },
    "alho": {
        "status": "toxico",
        "nivel_risco": "ALTO",
        "toxina": "Tiossulfatos (5x mais concentrado que na cebola)",
        "mecanismo": "Destruição oxidativa de hemácias causando anemia hemolítica.",
        "sintomas": "Letargia, vômitos, icterícia e dor abdominal.",
        "conduta_imediata": "Atendimento veterinário rápido no mesmo dia."
    },
    "xilitol": {
        "status": "toxico",
        "nivel_risco": "EMERGENCIA",
        "toxina": "Adoçante artificial (presente em gomas, doces diet e pastas)",
        "mecanismo": "Liberação fulminante de insulina causando choque hipoglicêmico severo e necrose hepática.",
        "sintomas": "Desorientação, tremores, ataxia (andar cambaleante), convulsões e colapso em 30 a 60 min.",
        "conduta_imediata": "Emergência médica máxima. Correr para hospital veterinário 24h."
    },
    "macadamia": {
        "status": "toxico",
        "nivel_risco": "ALTO",
        "toxina": "Composto neurotóxico vegetal",
        "mecanismo": "Fraqueza motora neuromotora temporária em cães.",
        "sintomas": "Incapacidade de apoiar as patas traseiras, febre, vômito e dor muscular.",
        "conduta_imediata": "Avaliação veterinária presencial."
    }
}

BASE_ALIMENTOS_PERMITIDOS = {
    "cenoura": {
        "status": "seguro",
        "beneficios": "Excelente para auxílio na limpeza mecânica dos dentes e aporte de fibras.",
        "recomendacao": "Oferecer crua em palitos ou cozida no vapor sem sal nem temperos."
    },
    "maca": {
        "status": "seguro",
        "beneficios": "Rica em vitaminas A e C e fibras hidrossolúveis.",
        "recomendacao": "Oferecer SEMPRE sem sementes e sem o miolo duro (sementes contêm glicosídeos cianogênicos)."
    },
    "abobora": {
        "status": "seguro",
        "beneficios": "Excelente regulador do trânsito gastrointestinal de cães e gatos.",
        "recomendacao": "Cozida em água, sem temperos e amassada."
    },
    "banana": {
        "status": "seguro",
        "beneficios": "Rica em potássio e energia rápida.",
        "recomendacao": "Oferecer em rodelas com moderação devido ao teor de frutose."
    },
    "melancia": {
        "status": "seguro",
        "beneficios": "Excelente fonte de hidratação nos dias de calor.",
        "recomendacao": "Oferecer em cubos, estritamente sem casca e sem sementes."
    }
}

BASE_CUIDADOS_PORTE_IDADE = {
    "pequeno": {
        "alerta_clinico": "Alta propensão à formação de cálculo dentário (tártaro) e doença valvar mitral após os 6 anos.",
        "nutricao": "Metabolismo acelerado, exigindo grãos menores e maior densidade energética.",
        "cuidados_gerais": "Escovação dental diária e avaliação cardíaca anual a partir da meia-idade."
    },
    "medio": {
        "alerta_clinico": "Tendência ao sedentarismo e sobrepeso se não houver rotina diária de estímulo.",
        "nutricao": "Rações balanceadas com controle calórico e ingestão moderada de petiscos.",
        "cuidados_gerais": "Exigência de 45 a 60 minutos de atividade física e mental diária."
    },
    "grande": {
        "alerta_clinico": "Vulnerabilidade articular (displasia coxofemoral) e risco crítico de Dilatação e Torção Gástrica (DTG).",
        "nutricao": "Alimentos enriquecidos com sulfato de condroitina e glicosamina. Comedouro elevado e lento.",
        "cuidados_gerais": "NUNCA alimentar logo antes ou após exercícios intensos. Considerados idosos a partir dos 6 a 7 anos."
    }
}

BASE_FAIXA_ETARIA = {
    "filhote": {
        "fase": "Filhote (0 a 12 meses)",
        "protocolo": "Esquema vacinal inicial com V8/V10 (3 a 4 doses) e Antirrábica aos 4 meses. Proibido passear em locais públicos antes de 15 dias após a última dose.",
        "socializacao": "Janela de ouro de habituação a sons, toques e outros animais até os 4 meses."
    },
    "adulto": {
        "fase": "Adulto (1 a 7 anos)",
        "protocolo": "Reforço anual de vacinas (V8/V10, Antirrábica, Giárdia e Gripe). Controle rigoroso de ectoparasitas (pulgas/carrapatos).",
        "socializacao": "Manutenção do peso ideal e enriquecimento ambiental constante."
    },
    "senior": {
        "fase": "Sênior / Idoso (7+ anos)",
        "protocolo": "Check-up veterinário semestral com exames laboratoriais (função renal, hepática, hemograma, glicemia) e ecocardiograma.",
        "socializacao": "Camas ortopédicas macias, tapetes antiderrapantes para proteção articular e iluminação adequada."
    }
}

def normalizar_texto(texto: str) -> str:
    if not texto:
        return ""
    nfkd = unicodedata.normalize("NFKD", str(texto))
    return "".join([c for c in nfkd if not unicodedata.combining(c)]).strip().lower()

def verificar_alimento_toxico(alimento: str) -> dict:
    alimento_norm = normalizar_texto(alimento)
    for chave, dados in BASE_ALIMENTOS_TOXICOS.items():
        if chave in alimento_norm or alimento_norm in chave:
            return {
                "alimento": chave,
                "status": "TOXICO_PERIGOSO",
                "nivel_risco": dados["nivel_risco"],
                "toxina": dados["toxina"],
                "sintomas": dados["sintomas"],
                "conduta_imediata": dados["conduta_imediata"]
            }
    for chave, dados in BASE_ALIMENTOS_PERMITIDOS.items():
        if chave in alimento_norm or alimento_norm in chave:
            return {
                "alimento": chave,
                "status": "SEGURO_PERMITIDO",
                "beneficios": dados["beneficios"],
                "recomendacao": dados["recomendacao"]
            }
    return {
        "alimento": alimento,
        "status": "NAO_ENCONTRADO_NA_BASE",
        "aviso": f"O alimento '{alimento}' não consta na lista prioritária. Em caso de dúvida, não ofereça antes de consultar um veterinário."
    }

def consultar_cuidados_porte_idade(porte: str, faixa_etaria: str) -> dict:
    porte_norm = normalizar_texto(porte)
    faixa_norm = normalizar_texto(faixa_etaria)
    
    if "gigante" in porte_norm:
        porte_norm = "grande"
    elif any(k in porte_norm for k in ["mini", "micro", "toy"]):
        porte_norm = "pequeno"

    if any(k in faixa_norm for k in ["idoso", "velho", "geriatrico", "senior"]):
        faixa_norm = "senior"
    elif any(k in faixa_norm for k in ["bebe", "puppy", "filhote"]):
        faixa_norm = "filhote"
    elif any(k in faixa_norm for k in ["jovem", "adulto"]):
        faixa_norm = "adulto"

    dados_porte = BASE_CUIDADOS_PORTE_IDADE.get(porte_norm, BASE_CUIDADOS_PORTE_IDADE["medio"])
    dados_faixa = BASE_FAIXA_ETARIA.get(faixa_norm, BASE_FAIXA_ETARIA["adulto"])

    return {
        "porte": porte_norm,
        "faixa_etaria": faixa_norm,
        "fase_vida": dados_faixa["fase"],
        "alerta_porte": dados_porte["alerta_clinico"],
        "recomendacao_nutricional": dados_porte["nutricao"],
        "cuidados_gerais": dados_porte["cuidados_gerais"],
        "protocolo_veterinario": dados_faixa["protocolo"],
        "estilo_de_vida": dados_faixa["socializacao"]
    }

# ==============================================================================
# 2. MODELOS PYDANTIC DE ENTRADA E SAÍDA (Alinhados ao Mobile)
# ==============================================================================

class PetContextPayload(BaseModel):
    id: Optional[int] = None
    nome: Optional[str] = None
    raca: Optional[str] = None
    porte: Optional[str] = None
    dataNasc: Optional[str] = None
    idade: Optional[int] = None
    sexo: Optional[str] = None
    castrado: Optional[bool] = None
    peso: Optional[str] = None
    alergias: Optional[str] = None
    medicamentos: Optional[str] = None
    ultimaVacina: Optional[str] = None
    ultimaConsulta: Optional[str] = None

class ChatRequest(BaseModel):
    pergunta: str = Field(..., description="Pergunta ou relato do tutor")
    petContext: Optional[PetContextPayload] = None

class ChatResponse(BaseModel):
    resposta: str
    categoria: str = "saude"
    urgencia: str = "baixa"
    acoes_recomendadas: Optional[List[str]] = None
    score_xp_sugerido: Optional[int] = 10
    origem_resposta: str = "Guardian AI (Gemini 2.5 Flash)"

class InsightItem(BaseModel):
    categoria: str
    titulo: str
    descricao: str
    urgencia: str

class InsightsResponse(BaseModel):
    insights: List[InsightItem]

# ==============================================================================
# 3. MOTOR DE INFERÊNCIA GOOGLE GENAI
# ==============================================================================

SYSTEM_INSTRUCTION = """Você é a "Guardian AI", copiloto inteligente de saúde preventiva, nutrição e bem-estar animal da plataforma PetGuardian (Clyvo Care).

Suas diretrizes inegociáveis de segurança clínica:
1. BLINDAGEM DE DOMÍNIO: Responda APENAS sobre cães, gatos, saúde animal, nutrição pet, rotinas e comportamento. Recuse educadamente qualquer assunto desconexo (código, matemática, receitas humanas), mesmo quando o tutor usar o pet como pretexto.
2. PROIBIÇÃO DE REMÉDIOS HUMANOS: NUNCA prescreva Paracetamol, Dipirona ou Ibuprofeno. O Paracetamol é ALTAMENTE LETAL para felinos e hepatotóxico para cães.
3. PROIBIÇÃO DE INDUÇÃO DE VÔMITO CASEIRA: Vete terminantemente água oxigenada ou sal de cozinha.
4. CONDUTA CLÍNICA: Sempre recomende consulta médica presencial ou pronto-socorro 24h em situações de risco.
5. TOM DE VOZ: Empático, acolhedor, objetivo, estruturado com emojis caninos/felinos e foco no bem-estar do animal."""

def get_genai_client():
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        return None
    try:
        from google import genai
        return genai.Client(api_key=api_key)
    except Exception:
        return None

# ==============================================================================
# 4. ROTAS DA API FASTAPI
# ==============================================================================

@app.get("/")
def root():
    return {
        "status": "online",
        "service": "PetGuardian AI Microservice",
        "model": "gemini-2.5-flash",
        "framework": "FastAPI + Google GenAI SDK",
        "version": "1.0.0"
    }

@app.post("/ai/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    pergunta_lower = request.pergunta.lower()
    
    # 1. Verificacao de Seguranca Farmacologica / Paracetamol em Gatos
    if "paracetamol" in pergunta_lower and any(k in pergunta_lower for k in ["gato", "felino", "mingau", "gatinho"]):
        return ChatResponse(
            resposta="⛔ **ALERTA VITAL: NUNCA DÊ PARACETAMOL PARA UM GATO!**\n\nO Paracetamol é **ALTAMENTE LETAL PARA FELINOS** mesmo em doses mínimas. Os gatos não possuem a enzima necessária para metabolizar o medicamento, causando destruição rápida das hemácias (asfixia interna) e necrose hepática fulminante em poucas horas.\n\n🚨 **O que fazer agora:**\n1. Não administre nenhum medicamento caseiro ou humano.\n2. Leve o gato imediatamente a uma clínica veterinária para investigar a causa dos sintomas com segurança.",
            categoria="EMERGENCIA",
            urgencia="EMERGENCIA",
            acoes_recomendadas=["Não medicar em casa", "Procurar clínica veterinária urgente"],
            score_xp_sugerido=0,
            origem_resposta="Guardrail de Segurança Farmacológica PetGuardian"
        )

    # 2. Verificacao Determinística de Alimentos Tóxicos
    alimentos_alvo = ["chocolate", "cacau", "uva", "passa", "cebola", "alho", "xilitol", "macadamia", "cenoura", "maca", "abobora", "banana", "melancia"]
    alimento_encontrado = next((a for a in alimentos_alvo if a in pergunta_lower), None)
    
    if alimento_encontrado:
        resultado_tox = verificar_alimento_toxico(alimento_encontrado)
        if resultado_tox.get("status") == "TOXICO_PERIGOSO":
            urgencia_val = resultado_tox.get("nivel_risco", "ALTO")
            return ChatResponse(
                resposta=f"🚨 **ALERTA TOXICOLÓGICO: {resultado_tox['alimento'].upper()} É PERIGOSO!**\n\n"
                         f"• **Toxina Ativa:** {resultado_tox.get('toxina')}\n"
                         f"• **Efeito:** {resultado_tox.get('mecanismo')}\n"
                         f"• **Sintomas Comuns:** {resultado_tox.get('sintomas')}\n\n"
                         f"👉 **Conduta Imediata:** {resultado_tox.get('conduta_imediata')}",
                categoria="EMERGENCIA" if urgencia_val == "EMERGENCIA" else "SAUDE",
                urgencia=urgencia_val,
                acoes_recomendadas=["Levar ao hospital 24h", "Não induzir vômito caseiro"],
                score_xp_sugerido=15,
                origem_resposta="Base de Toxicologia Determinística PetGuardian"
            )

    # 3. Tentativa de Inferencia via Gemini 2.5 Flash
    client = get_genai_client()
    if client:
        try:
            # Monta o contexto enriquecido do pet se fornecido
            contexto_pet_str = ""
            if request.petContext and request.petContext.nome:
                p = request.petContext
                contexto_pet_str = f"\n[Contexto do Pet Ativo: Nome={p.nome}, Raça={p.raca or 'SRD'}, Porte={p.porte or 'médio'}, Idade={p.idade or 'não informada'} anos, Peso={p.peso or 'não informado'}kg, Alergias={p.alergias or 'nenhuma'}]"

            prompt_completo = f"{contexto_pet_str}\n\nPergunta do Tutor: {request.pergunta}"
            
            # Chamada ao modelo Gemini
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt_completo,
                config={"system_instruction": SYSTEM_INSTRUCTION}
            )
            
            texto_resp = response.text or "Não foi possível gerar a resposta."
            
            return ChatResponse(
                resposta=texto_resp,
                categoria="saude",
                urgencia="baixa",
                acoes_recomendadas=["Manter rotina de hidratação", "Acompanhar bem-estar"],
                score_xp_sugerido=10,
                origem_resposta="Google Gemini 2.5 Flash (Interactions API)"
            )
        except Exception:
            pass

    # 4. Fallback Inteligente baseado em Porte / Idade
    porte_req = request.petContext.porte if request.petContext and request.petContext.porte else "medio"
    idade_num = request.petContext.idade if request.petContext and request.petContext.idade is not None else 3
    faixa_calc = "senior" if idade_num >= 7 else ("filhote" if idade_num <= 1 else "adulto")
    
    dados_cuidado = consultar_cuidados_porte_idade(porte_req, faixa_calc)
    nome_pet = request.petContext.nome if request.petContext and request.petContext.nome else "seu pet"

    return ChatResponse(
        resposta=f"Olá! Como copiloto de saúde do {nome_pet} ({dados_cuidado['fase_vida']}), analisei sua dúvida: \"{request.pergunta}\".\n\n"
                 f"🐾 **Orientações Preventivas Prioritárias:**\n"
                 f"• **Manejo e Cuidados:** {dados_cuidado['alerta_porte']}\n"
                 f"• **Nutrição:** {dados_cuidado['recomendacao_nutricional']}\n"
                 f"• **Protocolo Clínico:** {dados_cuidado['protocolo_veterinario']}\n\n"
                 f"Para diagnósticos específicos ou sintomas agudos, consulte sempre um médico-veterinário presencial.",
        categoria="saude",
        urgencia="baixa",
        acoes_recomendadas=["Check-up semestral", "Rotina de exercícios moderada"],
        score_xp_sugerido=10,
        origem_resposta="Guardian AI Knowledge Engine"
    )

@app.post("/ai/insights", response_model=InsightsResponse)
async def insights_endpoint(pet: PetContextPayload):
    nome_pet = pet.nome or "Seu pet"
    porte = pet.porte or "medio"
    idade = pet.idade if pet.idade is not None else 3
    faixa = "senior" if idade >= 7 else ("filhote" if idade <= 1 else "adulto")
    
    dados = consultar_cuidados_porte_idade(porte, faixa)
    
    insights_list = [
        InsightItem(
            categoria="saude",
            titulo=f"Cuidado Preventivo ({dados['fase_vida']})",
            descricao=dados["alerta_porte"],
            urgencia="baixa" if faixa != "senior" else "media"
        ),
        InsightItem(
            categoria="nutricao",
            titulo="Manejo Alimentar & Nutrição",
            descricao=dados["recomendacao_nutricional"],
            urgencia="baixa"
        ),
        InsightItem(
            categoria="rotina",
            titulo="Protocolo Veterinário Periódico",
            descricao=dados["protocolo_veterinario"],
            urgencia="baixa"
        )
    ]
    
    return InsightsResponse(insights=insights_list)

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("api:app", host="0.0.0.0", port=port, reload=True)
