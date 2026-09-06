import os
import re
import json
import urllib.request
import urllib.error
import unicodedata
from typing import Optional, List, Dict, Any
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from dotenv import load_dotenv

# Carrega variáveis locais do .env se disponível
load_dotenv()

# Inicialização do app FastAPI
app = FastAPI(
    title="PetGuardian / Clyvo Care — AI Microservice",
    description="API de IA Generativa e Triagem Preventiva para pets com respostas limpas e guardrails de segurança.",
    version="1.1.0"
)

# Habilita CORS total para conexão com React Native Mobile e Web
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==============================================================================
# 1. FUNÇÕES DE SANITIZAÇÃO E LIMPEZA DE TEXTO (Otimizado para Mobile)
# ==============================================================================

def limpar_texto_mobile(texto: str) -> str:
    """
    Remove marcadores brutos de Markdown (como **negrito**, # títulos, etc.)
    garantindo que o componente <Text> do React Native exiba um texto limpo,
    elegante e sem asteriscos.
    """
    if not texto:
        return ""
    
    # Remove marcações de negrito e itálico markdown (**texto** ou *texto* ou __texto__)
    t = re.sub(r'\*\*(.*?)\*\*', r'\1', texto)
    t = re.sub(r'__(.*?)__', r'\1', t)
    t = re.sub(r'(?<!\*)\*(?!\*)(.*?)(?<!\*)\*(?!\*)', r'\1', t)
    
    # Remove marcadores de cabeçalho Markdown (###, ##, #)
    t = re.sub(r'^#{1,6}\s*', '', t, flags=re.MULTILINE)
    
    # Normaliza marcadores de lista
    t = re.sub(r'^\s*[\*\-]\s+', '• ', t, flags=re.MULTILINE)
    
    # Remove múltiplos espaços e quebras de linha excessivas (mais de 2 consecutivas)
    t = re.sub(r'\n{3,}', '\n\n', t)
    
    return t.strip()

def normalizar_texto(texto: str) -> str:
    if not texto:
        return ""
    nfkd = unicodedata.normalize("NFKD", str(texto))
    return "".join([c for c in nfkd if not unicodedata.combining(c)]).strip().lower()

# ==============================================================================
# 2. BASES DE CONHECIMENTO DETERMINÍSTICAS E SEMÂNTICAS
# ==============================================================================

BASE_ALIMENTOS_TOXICOS = {
    "chocolate": {
        "status": "toxico",
        "nivel_risco": "EMERGENCIA",
        "toxina": "Teobromina e Cafeína",
        "mecanismo": "Metabolização muito lenta pelo fígado de cães e gatos, gerando hiperestimulação neurológica e cardiovascular.",
        "sintomas": "Taquicardia, tremores musculares, vômitos, diarreia, arritmias e convulsões.",
        "conduta_imediata": "Levar imediatamente a um hospital veterinário 24h. Não induzir vômito com água oxigenada ou sal em casa."
    },
    "cacau": {
        "status": "toxico",
        "nivel_risco": "EMERGENCIA",
        "toxina": "Teobromina concentrada",
        "mecanismo": "Toxicidade extrema equivalente ao chocolate amargo puro.",
        "sintomas": "Convulsões, hipertermia e risco iminente de parada cardiorrespiratória.",
        "conduta_imediata": "Emergência clínica imediata. Levar ao pronto-socorro veterinário 24h."
    },
    "uva": {
        "status": "toxico",
        "nivel_risco": "EMERGENCIA",
        "toxina": "Ácido tartárico e derivados nefrotóxicos",
        "mecanismo": "Provoca necrose tubular renal aguda mesmo em quantidades mínimas.",
        "sintomas": "Vômitos nas primeiras horas, letargia, dor abdominal e ausência de urina (anúria).",
        "conduta_imediata": "Hospitalização imediata 24h com fluidoterapia intravenosa e monitoramento renal."
    },
    "uva-passa": {
        "status": "toxico",
        "nivel_risco": "EMERGENCIA",
        "toxina": "Ácido tartárico altamente concentrado",
        "mecanismo": "Potencial nefrotóxico ainda superior ao da uva fresca.",
        "sintomas": "Falência renal rápida, vômitos e apatia profunda.",
        "conduta_imediata": "Hospitalização imediata 24h."
    },
    "cebola": {
        "status": "toxico",
        "nivel_risco": "ALTO",
        "toxina": "Dissulfeto de alilpropila e compostos sulfurados",
        "mecanismo": "Oxidação da hemoglobina e destruição das hemácias (anemia hemolítica severa).",
        "sintomas": "Fraqueza intensa, gengivas pálidas ou azuladas, urina avermelhada/escura e respiração ofegante.",
        "conduta_imediata": "Consulta veterinária urgente para avaliação hematológica."
    },
    "alho": {
        "status": "toxico",
        "nivel_risco": "ALTO",
        "toxina": "Tiossulfatos concentrados",
        "mecanismo": "Destruição oxidativa das hemácias, cerca de 5 vezes mais tóxico que a cebola.",
        "sintomas": "Letargia, salivação, vômitos e mucosas pálidas.",
        "conduta_imediata": "Atendimento veterinário rápido no mesmo dia."
    },
    "xilitol": {
        "status": "toxico",
        "nivel_risco": "EMERGENCIA",
        "toxina": "Adoçante artificial (presente em chicletes, pastas e doces diet)",
        "mecanismo": "Liberação fulminante de insulina, gerando choque hipoglicêmico severo e necrose hepática aguda.",
        "sintomas": "Desorientação, fraqueza, andar cambaleante, convulsões e colapso em 30 a 60 minutos.",
        "conduta_imediata": "Emergência médica máxima. Correr imediatamente para o pronto-socorro veterinário 24h."
    },
    "macadamia": {
        "status": "toxico",
        "nivel_risco": "ALTO",
        "toxina": "Composto neurotóxico vegetal",
        "mecanismo": "Bloqueio neuromuscular temporário em cães.",
        "sintomas": "Fraqueza nas patas traseiras, febre, tremores e vômito.",
        "conduta_imediata": "Avaliação veterinária presencial."
    },
    "cafe": {
        "status": "toxico",
        "nivel_risco": "EMERGENCIA",
        "toxina": "Metilxantinas (Cafeína pura)",
        "mecanismo": "Superestimulação do sistema nervoso central e sobrecarga cardíaca aguda.",
        "sintomas": "Agitação extrema, taquicardia, arritmias, tremores e convulsões.",
        "conduta_imediata": "Atendimento veterinário urgente 24h."
    }
}

BASE_RESPOSTAS_COTIDIANAS = {
    "pao": {
        "palavras_chave": ["pao", "paes", "pão", "pães", "torrada", "massa"],
        "resposta": (
            "Sim, cães podem comer um pedacinho pequeno de pão simples (como pão francês ou pão de forma tradicional), mas apenas como um agrado muito ocasional.\n\n"
            "Cuidados essenciais que você deve ter:\n"
            "• Baixo valor nutritivo: O pão é rico em carboidratos e calorias, o que pode levar ao ganho de peso e desequilíbrio nutricional se oferecido com frequência.\n"
            "• Sem recheios ou temperos: Nunca ofereça pães que contenham alho, cebola, queijo gorduroso, passas ou adoçante xilitol.\n"
            "• Proibição de massa crua: Massas de pão cruas com fermento biológico são extremamente perigosas, pois o fermento continua crescendo no estômago do pet e libera álcool, causando intoxicação e dilatação gástrica.\n\n"
            "💡 Dica saudável: Se quiser agradar seu pet com petiscos naturais seguros, prefira pedacinhos de cenoura crua ou maçã sem sementes!"
        ),
        "categoria": "nutricao",
        "urgencia": "baixa"
    },
    "arroz": {
        "palavras_chave": ["arroz", "arroz branco", "arroz integral"],
        "resposta": (
            "Sim! O arroz branco ou integral cozido é seguro e muito bem digerido por cães e gatos.\n\n"
            "Como oferecer corretamente:\n"
            "• Sempre cozido apenas em água, estritamente sem sal, óleo, alho ou cebola.\n"
            "• É muito utilizado como suporte em dietas brandas quando o pet está se recuperando de episódios gastrointestinais leves (sempre sob orientação profissional)."
        ),
        "categoria": "nutricao",
        "urgencia": "baixa"
    },
    "ovo": {
        "palavras_chave": ["ovo", "ovos", "ovo cozido", "omelete"],
        "resposta": (
            "Sim! O ovo é uma excelente fonte de proteína de alto valor biológico, aminoácidos essenciais e vitaminas para cães e gatos.\n\n"
            "Recomendações:\n"
            "• Ofereça sempre 100% cozido (cozido ou mexido sem óleo, sal ou temperos).\n"
            "• Evite ovos crus devido ao risco de contaminação por Salmonella e presença de avidina (que reduz a absorção de biotina)."
        ),
        "categoria": "nutricao",
        "urgencia": "baixa"
    },
    "queijo_leite": {
        "palavras_chave": ["leite", "queijo", "iogurte", "laticinio", "laticinios", "requeijao", "manteiga"],
        "resposta": (
            "Com muita cautela! A maioria dos cães e gatos adultos não produz lactase suficiente, tornando-se intolerantes à lactose.\n\n"
            "Pontos de atenção:\n"
            "• Leite de vaca integral e queijos amarelos/gordurosos costumam provocar diarreia, gases e desconforto abdominal.\n"
            "• Se o seu pet não for intolerante, pequenas quantidades de queijo branco magro sem sal (como ricota ou cottage) ou iogurte natural desnatado sem açúcar podem ser oferecidos ocasionalmente."
        ),
        "categoria": "nutricao",
        "urgencia": "baixa"
    },
    "carne_frango": {
        "palavras_chave": ["frango", "carne", "peixe", "bife", "boi", "porco"],
        "resposta": (
            "Sim! Carnes magras (como peito de frango ou carne bovina moída magra) são ótimas fontes de nutrientes.\n\n"
            "Regras de segurança:\n"
            "• Devem ser sempre bem cozidas e preparadas exclusivamente sem sal, cebola, alho ou pimentas.\n"
            "• ⚠️ ATENÇÃO: NUNCA ofereça ossos cozidos (de frango ou costela). O cozimento altera a estrutura do osso, fazendo com que ele se estilhace em pontas agudas capazes de perfurar o esôfago, estômago ou intestinos do animal."
        ),
        "categoria": "nutricao",
        "urgencia": "baixa"
    },
    "frutas_gerais": {
        "palavras_chave": ["fruta", "frutas", "maca", "banana", "melancia", "mamao", "morango", "manga"],
        "resposta": (
            "Muitas frutas são excelentes petiscos hidratantes e nutritivos para cães!\n\n"
            "Frutas seguras e recomendadas:\n"
            "• Maçã: Sempre sem sementes e sem o miolo duro (as sementes contêm vestígios de cianeto).\n"
            "• Banana: Em rodelas moderadas devido ao teor de frutose e potássio.\n"
            "• Melancia e Melão: Em cubos frescos, estritamente sem casca e sem sementes.\n"
            "• Morango e Manga: Sem caroço e sem folhas.\n\n"
            "⛔ PROIBIDAS: Uvas e uvas-passas são tóxicas e causam falência renal aguda."
        ),
        "categoria": "nutricao",
        "urgencia": "baixa"
    },
    "vomito_diarreia": {
        "palavras_chave": ["vomito", "vomitando", "vomitou", "diarreia", "fezes moles", "mole", "desarranjo"],
        "resposta": (
            "Episódios isolados de vômito ou diarreia podem ocorrer por indiscrição alimentar leve, mas exigem atenção redobrada.\n\n"
            "O que você deve fazer:\n"
            "1. Mantenha água limpa e fresca sempre disponível para evitar desidratação.\n"
            "2. Não administre nenhum medicamento humano por conta própria.\n"
            "3. Se houver sangue nas fezes ou vômito, prostração, febre ou se os episódios se repetirem mais de 2 vezes no mesmo dia, leve seu pet imediatamente a um hospital veterinário."
        ),
        "categoria": "saude",
        "urgencia": "media"
    },
    "vacinas_geral": {
        "palavras_chave": ["vacina", "vacinas", "vacinacao", "v8", "v10", "antirrabica", "giardia", "gripe"],
        "resposta": (
            "A vacinação é o pilar mais importante da medicina preventiva para cães e gatos!\n\n"
            "Protocolos essenciais:\n"
            "• Filhotes: Iniciam com 3 a 4 doses de vacina múltipla (V8 ou V10 para cães / V3, V4 ou V5 para gatos) com intervalo de 21 a 28 dias, mais a vacina antirrábica aos 4 meses.\n"
            "• Importante: Filhotes só devem passear na rua ou ter contato com outros animais 15 dias após a conclusão do esquema vacinal.\n"
            "• Adultos e Idosos: Necessitam de reforço anual de todas as vacinas para manter a imunidade ativa."
        ),
        "categoria": "saude",
        "urgencia": "baixa"
    }
}

BASE_CUIDADOS_PORTE_IDADE = {
    "pequeno": {
        "alerta_clinico": "Propensão natural a acúmulo de tártaro nos dentes e alterações na válvula mitral após a meia-idade.",
        "nutricao": "Metabolismo acelerado, necessitando de grãos menores e maior densidade energética balanceada.",
        "cuidados_gerais": "Escovação dental frequente e acompanhamento cardiológico regular a partir dos 6 anos."
    },
    "medio": {
        "alerta_clinico": "Tendência ao ganho de peso se não mantiver uma rotina diária de passeios e atividades físicas.",
        "nutricao": "Alimentação balanceada com controle calórico e petiscos apenas como agrado moderado.",
        "cuidados_gerais": "Recomenda-se cerca de 40 a 60 minutos de exercícios e enriquecimento ambiental diários."
    },
    "grande": {
        "alerta_clinico": "Maior vulnerabilidade articular (displasia) e risco de dilatação/torção gástrica.",
        "nutricao": "Dietas ricas em protetores articulares (condroitina e glicosamina) e uso de comedouros lentos.",
        "cuidados_gerais": "Evitar exercícios intensos logo antes ou após as refeições para proteger o sistema digestivo."
    }
}

BASE_FAIXA_ETARIA = {
    "filhote": {
        "fase": "Filhote (0 a 12 meses)",
        "protocolo": "Esquema vacinal inicial completo (V8/V10 + Antirrábica) e vermifugação periódica. Passeios externos liberados apenas após a imunização completa.",
        "socializacao": "Fase de ouro para socialização com diferentes estímulos, sons e toques amigáveis."
    },
    "adulto": {
        "fase": "Adulto (1 a 7 anos)",
        "protocolo": "Reforço anual de vacinas, prevenção contínua contra pulgas/carrapatos e exames de rotina anuais.",
        "socializacao": "Manutenção do peso saudável através de rotina ativa e estímulos mentais."
    },
    "senior": {
        "fase": "Sênior / Idoso (7+ anos)",
        "protocolo": "Check-up veterinário semestral com exames laboratoriais (rins, fígado, hemograma) e avaliação cardíaca.",
        "socializacao": "Ambiente confortável com camas macias, tapetes antiderrapantes e caminhadas leves."
    }
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
# 3. MODELOS PYDANTIC DE ENTRADA E SAÍDA (Alinhados ao Mobile)
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
    origem_resposta: str = "Guardian AI (PetGuardian Care)"

class InsightItem(BaseModel):
    categoria: str
    titulo: str
    descricao: str
    urgencia: str

class InsightsResponse(BaseModel):
    insights: List[InsightItem]

# ==============================================================================
# 4. MOTOR DE INFERÊNCIA GEMINI (MODELO ÚNICO)
# ==============================================================================

MODEL = "gemini-3.5-flash-lite"

SYSTEM_INSTRUCTION = """Você é o copiloto de saúde preventiva e nutrição animal "Guardian AI" da plataforma PetGuardian (Clyvo Care).

Suas diretrizes fundamentais:
1. FOCO NO ASSUNTO: Responda diretamente e de forma completa à pergunta do tutor sobre cães, gatos, alimentação, saúde e bem-estar.
2. RESPOSTA LIMPA PARA MOBILE: NÃO utilize marcações de negrito com asteriscos brutos (NUNCA use **texto** ou *texto* ou cabeçalhos com ###). Escreva em parágrafos claros e fluidos, usando emojis temáticos (🐾, 💡, 🩺, ⚠️, etc.) e marcadores simples com "• " para listas.
3. SEGURANÇA FARMACOLÓGICA ABSOLUTA: NUNCA prescreva ou autorize Paracetamol, Dipirona ou Ibuprofeno para pets. O Paracetamol é ALTAMENTE LETAL para felinos.
4. SEGURANÇA EM INTOXICAÇÕES: NUNCA recomende induzir vômito caseiro com sal ou água oxigenada. Recomende atendimento veterinário 24h em suspeitas de envenenamento.
5. TOM DE VOZ: Amigável, acolhedor, empático e com fundamentação veterinária preventiva de fácil entendimento."""

def chamar_gemini_rest(api_key: str, prompt_completo: str) -> Optional[str]:
    """
    Executa chamada direta via REST API para o modelo oficial único.
    """
    payload = {
        "contents": [
            {
                "parts": [
                    {"text": f"{SYSTEM_INSTRUCTION}\n\n{prompt_completo}"}
                ]
            }
        ],
        "generationConfig": {
            "temperature": 0.6,
            "maxOutputTokens": 800
        }
    }
    
    headers = {"Content-Type": "application/json"}
    body_bytes = json.dumps(payload).encode("utf-8")
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent?key={api_key}"
    
    try:
        req = urllib.request.Request(url, data=body_bytes, headers=headers, method="POST")
        with urllib.request.urlopen(req, timeout=15) as response:
            if response.status == 200:
                dados = json.loads(response.read().decode("utf-8"))
                candidates = dados.get("candidates", [])
                if candidates and "content" in candidates[0]:
                    parts = candidates[0]["content"].get("parts", [])
                    if parts and "text" in parts[0]:
                        return parts[0]["text"]
    except Exception as e:
        print(f"[Gemini REST] Modelo {MODEL} falhou: {e}")
            
    return None

def chamar_gemini_sdk(api_key: str, prompt_completo: str) -> Optional[str]:
    """
    Executa chamada via SDK oficial google-genai para o modelo único.
    """
    try:
        from google import genai
        from google.genai import types
        client = genai.Client(api_key=api_key)
        
        response = client.models.generate_content(
            model=MODEL,
            contents=prompt_completo,
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_INSTRUCTION,
                temperature=0.6,
                max_output_tokens=800
            )
        )
        if response and response.text:
            return response.text
    except Exception as e:
        print(f"[Gemini SDK] Modelo {MODEL} falhou: {e}")
    return None

def gerar_resposta_ia(prompt_completo: str) -> Optional[str]:
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        return None
        
    # Tenta SDK primeiro
    texto = chamar_gemini_sdk(api_key, prompt_completo)
    if texto:
        return texto
        
    # Tenta REST direto como fallback resiliente
    return chamar_gemini_rest(api_key, prompt_completo)

# ==============================================================================
# 5. ROTAS DA API FASTAPI
# ==============================================================================

@app.get("/")
def root():
    return {
        "status": "online",
        "service": "PetGuardian AI Microservice",
        "model": f"{MODEL} / Semantic Knowledge Engine",
        "framework": "FastAPI + Clean Mobile Pipeline",
        "version": "1.2.0"
    }

@app.post("/ai/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    pergunta_norm = normalizar_texto(request.pergunta)
    
    # 1. Guardrail de Segurança Farmacológica / Paracetamol em Gatos
    if "paracetamol" in pergunta_norm and any(k in pergunta_norm for k in ["gato", "felino", "mingau", "gatinho"]):
        texto_limpo = limpar_texto_mobile(
            "⛔ ALERTA VITAL: NUNCA DÊ PARACETAMOL PARA UM GATO!\n\n"
            "O Paracetamol é ALTAMENTE LETAL PARA FELINOS mesmo em doses mínimas. Os gatos não possuem a enzima necessária para metabolizar o medicamento, causando destruição rápida das hemácias (asfixia interna) e necrose hepática fulminante em poucas horas.\n\n"
            "🚨 O que fazer agora:\n"
            "• Não administre nenhum medicamento caseiro ou humano.\n"
            "• Se o animal ingeriu acidentalmente, leve IMEDIATAMENTE a um pronto-socorro veterinário 24h."
        )
        return ChatResponse(
            resposta=texto_limpo,
            categoria="EMERGENCIA",
            urgencia="EMERGENCIA",
            acoes_recomendadas=["Não medicar em casa", "Procurar clínica veterinária urgente"],
            score_xp_sugerido=0,
            origem_resposta="Guardrail de Segurança Farmacológica PetGuardian"
        )

    # 2. Verificação de Alimentos Tóxicos Críticos
    for chave, dados_tox in BASE_ALIMENTOS_TOXICOS.items():
        if chave in pergunta_norm:
            urgencia_val = dados_tox["nivel_risco"]
            texto_alerta = (
                f"🚨 ALERTA TOXICOLÓGICO: {chave.upper()} É PERIGOSO PARA PETS!\n\n"
                f"• Toxina: {dados_tox['toxina']}\n"
                f"• Efeito no organismo: {dados_tox['mecanismo']}\n"
                f"• Sintomas de alerta: {dados_tox['sintomas']}\n\n"
                f"👉 Conduta recomendada: {dados_tox['conduta_imediata']}"
            )
            return ChatResponse(
                resposta=limpar_texto_mobile(texto_alerta),
                categoria="EMERGENCIA" if urgencia_val == "EMERGENCIA" else "SAUDE",
                urgencia=urgencia_val,
                acoes_recomendadas=["Levar ao hospital 24h", "Não induzir vômito caseiro"],
                score_xp_sugerido=15,
                origem_resposta="Base de Toxicologia Determinística PetGuardian"
            )

    # 3. Tentativa de Inferência via Gemini (com sanitização para mobile)
    contexto_pet_str = ""
    nome_pet = "seu pet"
    if request.petContext and request.petContext.nome:
        p = request.petContext
        nome_pet = p.nome
        contexto_pet_str = (
            f"[Dados do Pet: Nome={p.nome}, Raça={p.raca or 'SRD'}, "
            f"Porte={p.porte or 'médio'}, Idade={p.idade or 'não informada'} anos, "
            f"Peso={p.peso or 'não informado'}kg, Alergias={p.alergias or 'nenhuma'}]"
        )

    prompt_completo = f"{contexto_pet_str}\n\nPergunta do Tutor: {request.pergunta}"
    
    resposta_ia = gerar_resposta_ia(prompt_completo)
    if resposta_ia:
        texto_limpo = limpar_texto_mobile(resposta_ia)
        return ChatResponse(
            resposta=texto_limpo,
            categoria="saude",
            urgencia="baixa",
            acoes_recomendadas=["Acompanhar o bem-estar", "Manter hidratação regular"],
            score_xp_sugerido=10,
            origem_resposta="Guardian AI (Gemini 2.5 Flash)"
        )

    # 4. Fallback Semântico Inteligente para Perguntas Cotidianas
    for chave_tema, dados_tema in BASE_RESPOSTAS_COTIDIANAS.items():
        if any(palavra in pergunta_norm for palavra in dados_tema["palavras_chave"]):
            return ChatResponse(
                resposta=limpar_texto_mobile(dados_tema["resposta"]),
                categoria=dados_tema["categoria"],
                urgencia=dados_tema["urgencia"],
                acoes_recomendadas=["Manter rotina equilibrada", "Consultar veterinário em caso de dúvidas"],
                score_xp_sugerido=10,
                origem_resposta="Guardian AI (Base Semântica Especializada)"
            )

    # 5. Fallback Contextual por Porte e Idade (Resposta Natural e Limpa)
    porte_req = request.petContext.porte if request.petContext and request.petContext.porte else "medio"
    idade_num = request.petContext.idade if request.petContext and request.petContext.idade is not None else 3
    faixa_calc = "senior" if idade_num >= 7 else ("filhote" if idade_num <= 1 else "adulto")
    dados_cuidado = consultar_cuidados_porte_idade(porte_req, faixa_calc)

    resposta_contextual = (
        f"Olá! Analisei sua dúvida sobre o {nome_pet} ({dados_cuidado['fase_vida']}).\n\n"
        f"🐾 Orientações para a fase atual do {nome_pet}:\n"
        f"• Nutrição & Manejo: {dados_cuidado['recomendacao_nutricional']}\n"
        f"• Cuidados Clínicos: {dados_cuidado['alerta_porte']}\n"
        f"• Protocolo Preventivo: {dados_cuidado['protocolo_veterinario']}\n\n"
        f"Para diagnósticos específicos, alterações de comportamento ou sintomas agudos, consulte sempre um médico-veterinário presencial."
    )

    return ChatResponse(
        resposta=limpar_texto_mobile(resposta_contextual),
        categoria="saude",
        urgencia="baixa",
        acoes_recomendadas=["Check-up periódico", "Rotina de bem-estar ativa"],
        score_xp_sugerido=10,
        origem_resposta="Guardian AI (Mecanismo Preventivo)"
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
