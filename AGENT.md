# 🤖 AGENT.md — Guia Arquitetural & Especificação Técnica Completa (Disruptive-Architectures-IoT-IoB-IA)

Este documento serve como a **referência definitiva e fonte única da verdade** para desenvolvedores, arquitetos de software e agentes de IA sobre o microserviço inteligente **Guardian AI** (PetGuardian / Clyvo Care). Aqui estão documentados em detalhes a arquitetura de software, catálogo de módulos, modelos de dados Pydantic, engenharia de prompts, guardrails clínicos e éticos, base vetorial RAG com ChromaDB, motor de resiliência determinístico (fallback offline) e contratos REST de integração.

---

## 🏛️ 1. Visão Geral da Arquitetura & Proposta de Valor

O **Guardian AI** é um microserviço em **Python 3.11+** construído sobre o framework **FastAPI**, projetado para atuar como o copiloto inteligente de saúde preventiva, triagem clínica de emergência, nutrição animal e adestramento positivo gamificado para a plataforma **PetGuardian** (Challenge Clyvo 2026 — 2TDSPG / FIAP).

### 🎯 Problema de Negócio & Missão
Tutores de animais de estimação frequentemente enfrentam dilemas críticos no cuidado diário:
1. **Pânico desinformado ou automedicação perigosa:** Uso de medicamentos humanos alopáticos letais (como Paracetamol para felinos ou Dipirona em dosagens inadequadas) ou tentativas de indução de vômito caseiro com água oxigenada e sal.
2. **Subestimação de sinais de emergência:** Demora na identificação de intoxicações agudas (chocolate, uvas, cebola, xilitol, venenos) ou condições fulminantes (torção gástrica, convulsões prolongadas).
3. **Falta de adesão a rotinas preventivas:** Esquecimento de esquemas vacinais, ausência de higiene bucal preventiva e desmotivação no adestramento comportamental.

O microserviço **Guardian AI** soluciona essa dor ao prover:
- **Inteligência Centrada no Pet:** Ingestão contextual dos metadados do animal ativo (espécie, raça, porte, idade, sexo, castração, peso, alergias, medicações e histórico).
- **RAG Vetorial Ancorado:** Consulta semântica a um corpus veterinário curado em Markdown indexado no **ChromaDB**, reduzindo alucinações a zero.
- **Guardrails Clínicos & Éticos Invioláveis:** Bloqueio estrito de perguntas fora de escopo (programação, finanças, culinária humana, política) e proibição absoluta de prescrição de medicamentos alopáticos sem consulta presencial.
- **Resiliência 100% Offline (Zero Downtime SLA):** Motor determinístico em regras clínicas e expressões regulares que garante respostas ricas mesmo na ausência de conexão com a internet ou sem chave de API do Gemini.

### 🛠️ Stack Tecnológica
- **Linguagem:** Python 3.11+
- **Framework Web:** FastAPI (`fastapi>=0.110.0`)
- **Servidor ASGI:** Uvicorn (`uvicorn[standard]>=0.28.0`)
- **SDK de IA Generativa:** Google GenAI SDK (`google-genai>=2.0.0`)
- **Modelo de LLM Principal:** Google Gemini 3.5 Flash Lite (`gemini-3.5-flash-lite` / `gemini-2.5-flash`)
- **Base de Conhecimento Vetorial (RAG):** ChromaDB (`chromadb>=0.4.24`) com persistência em disco SQLite/HNSW
- **Validação & Tipagem de Dados:** Pydantic v2 (`pydantic>=2.6.0`) e Pydantic Settings (`pydantic-settings>=2.2.0`)
- **Variáveis de Ambiente:** Python-Dotenv (`python-dotenv>=1.0.1`)

---

## 🏗️ 2. Diagramas de Arquitetura & Fluxo de Dados

### 2.1. Arquitetura de Comunicação Ponta a Ponta

```text
 ┌────────────────────────────────────────────────────────────────────────┐
 │                      📱 FRONTEND REACT NATIVE                         │
 │                   Tela: AiAssistantScreen.tsx                          │
 └───────────────────────────────────┬────────────────────────────────────┘
                                     │
                        HTTP POST /ai/chat
                        Payload: { pergunta, petContext: { nome, porte, idade, ... } }
                                     │
                                     ▼
 ┌────────────────────────────────────────────────────────────────────────┐
 │                 🐍 BACKEND FASTAPI (PYTHON 3.11+)                      │
 │                                                                        │
 │  1. Validação Pydantic (ChatRequest Schema)                           │
 │  2. Verificação de Guardrail de Domínio (Rejeita fora de escopo)      │
 │  3. Busca Semântica RAG no ChromaDB (Busca top-3 chunks relevantes)    │
 │  4. Montagem Dinâmica de Prompt (Context Injection)                    │
 │  5. Invocação do Google Gemini Flash com System Instruction            │
 │  6. Sanitização & Formatação do Payload JSON de Retorno                │
 └───────────────────────────────────┬────────────────────────────────────┘
                                     │
                                     ▼
 ┌────────────────────────────────────────────────────────────────────────┐
 │                         RESPOSTA JSON ESTRUTURADA                      │
 │   { resposta, categoria, urgencia, alerta_clinica_24h, score_xp }      │
 └───────────────────────────────────┬────────────────────────────────────┘
                                     │
                                     ▼
 ┌────────────────────────────────────────────────────────────────────────┐
 │                      📱 FRONTEND REACT NATIVE                         │
 │               Exibição instantânea no balão do chat                    │
 └────────────────────────────────────────────────────────────────────────┘
```

### 2.2. Pipeline de RAG (Retrieval-Augmented Generation) com ChromaDB

```text
 [Arquivos Markdown em app/data/knowledge_base/]
  ├── adestramento_positivo.md
  ├── alimentos_toxicos.md
  ├── cuidados_por_porte_idade.md
  └── primeiros_socorros_emergencia.md
                     │
                     ▼
 [RagService._load_and_chunk_documents()]
  Dividido por cabeçalhos '## ' em seções temáticas com metadados
                     │
                     ▼
 [ChromaDB Persistent Client (data/chroma_db/)]
  Coleção: 'petguardian_vet_knowledge'
  Embeddings automáticos + persistência local em disco
                     │
                     ├──────────────────────────────┐
                     ▼                              ▼
             (Pergunta do Tutor)           (Busca Semântica top_k=3)
                     │                              │
                     └──────────────┬───────────────┘
                                    ▼
                     [Prompt Enriquecido com Contexto]
                                    │
                                    ▼
                     [Google Gemini 3.5 Flash Lite]
                                    │
                                    ▼
                     [ChatResponse JSON Tipado]
```

### 2.3. Pipeline de Resiliência & Fallback Determinístico (Zero-Downtime)

```text
                     [Requisição de IA Recebida]
                                 │
                                 ▼
                     ¿Chave Gemini Configurada?
                            /          \
                         SIM            NÃO
                         /                \
                        ▼                  ▼
             [Invocação Gemini SDK]   [FallbackService (Offline Engine)]
                 /          \                  │
              SUCESSO      FALHA (Timeout/429) │
                /            \                 │
               ▼              └───────┬────────┘
        [ChatResponse]                ▼
    (origem: "gemini_rag")      [ChatResponse]
                             (origem: "fallback_rules")
```

---

## 📁 3. Estrutura de Diretórios & Catálogo de Módulos

```text
Disruptive-Architectures-IoT-IoB-IA/
├── .env                              → Variáveis de ambiente locais (não versionado)
├── .env.example                      → Modelo de variáveis de ambiente do projeto
├── .gitignore                        → Exclusões Git (__pycache__, data/chroma_db, .env)
├── AGENT.md                          → Este documento mestre de arquitetura e especificação
├── BACKLOG_DISRUPTIVE_ARCHITECTURES.md → Backlog formal Azure Boards (Sprint 3)
├── README.md                         → Documentação com quickstart e guia de execução
├── requirements.txt                  → Dependências Python fixadas
├── app/
│   ├── __init__.py                   → Declaração do pacote app
│   ├── config.py                     → Pydantic BaseSettings e variáveis globais
│   ├── main.py                       → Ponto de entrada FastAPI, middlewares e rotas HTTP
│   ├── models/
│   │   ├── __init__.py               → Exportação dos modelos
│   │   └── schemas.py                → Schemas Pydantic v2 (Requests, Responses, Enums)
│   ├── prompts/
│   │   ├── __init__.py               → Exportação dos prompts
│   │   └── system_prompts.py         → System Instructions, Guardrails e Prompt Builders
│   ├── services/
│   │   ├── __init__.py               → Exportação dos serviços
│   │   ├── fallback_service.py       → Motor determinístico de contingência offline
│   │   ├── gemini_service.py         → Orquestrador Google GenAI SDK (Singleton POO)
│   │   └── rag_service.py            → Indexador e buscador vetorial ChromaDB
│   └── data/
│       └── knowledge_base/           → Corpus veterinário curado em Markdown
│           ├── adestramento_positivo.md
│           ├── alimentos_toxicos.md
│           ├── cuidados_por_porte_idade.md
│           └── primeiros_socorros_emergencia.md
└── data/
    └── chroma_db/                    → Diretório de persistência do banco vetorial ChromaDB
```

---

## 🧩 4. Detalhamento dos Componentes do Sistema

### 4.1. `app/config.py` — Gestão Centralizada de Configurações
Utiliza o `pydantic-settings` para carregar e validar variáveis de ambiente a partir do arquivo `.env`:

```python
class Settings(BaseSettings):
    APP_ENV: str = "development"
    APP_TITLE: str = "Guardian AI API"
    APP_DESCRIPTION: str = "Microserviço de Inteligência Artificial Generativa e RAG para o ecossistema PetGuardian (Challenge Clyvo 2026)"
    APP_VERSION: str = "1.0.0"
    
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    # Google Gemini
    GEMINI_API_KEY: str = ""
    GEMINI_MODEL: str = "gemini-3.5-flash-lite"
    
    # ChromaDB RAG
    CHROMA_PERSIST_DIR: str = str(BASE_DIR / "data" / "chroma_db")
    KNOWLEDGE_BASE_DIR: str = str(BASE_DIR / "app" / "data" / "knowledge_base")
    
    # CORS
    CORS_ORIGINS: list[str] = ["*"]
```

### 4.2. `app/main.py` — Ponto de Entrada FastAPI & Ciclo de Vida
- **Gerenciador de Ciclo de Vida (`lifespan`):** Executa o bootstrap automático do `rag_service.initialize()` no startup da aplicação, indexando os arquivos Markdown sem necessidade de scripts manuais prévios.
- **Middleware CORS:** Permite comunicação irrestrita (`allow_origins=["*"]`, `allow_methods=["*"]`, `allow_headers=["*"]`) com o aplicativo mobile React Native (`Mobile-Application-Development`) e painéis web.
- **Roteamento de Endpoints & Aliases:** Cada funcionalidade é exposta na rota principal e em seu alias de versionamento formal (ex: `/ai/chat` e `/api/v1/ai/chat`), garantindo retrocompatibilidade.
- **Documentação Automática:** Swagger UI interativo em `/docs` e ReDoc em `/redoc`.

### 4.3. `app/models/schemas.py` — Schemas de Dados & Enums Pydantic v2
Define contratos estritos e imutáveis com validações de tamanho, padrões e documentação embutida:

| Modelo / Enum | Descrição | Campos Principais |
| :--- | :--- | :--- |
| `PetPorteEnum` | Porte do animal | `PEQUENO`, `MEDIO`, `GRANDE` |
| `UrgencyEnum` | Nível de urgência da situação | `BAIXA`, `MEDIA`, `ALTA`, `EMERGENCIA` |
| `CategoryEnum` | Classificação temática | `SAUDE`, `NUTRICAO`, `COMPORTAMENTO`, `ROTINA`, `EMERGENCIA`, `GERAL`, `FORA_DE_ESCOPO` |
| `PetContext` | Contexto completo do pet selecionado | `id`, `nome`, `raca`, `porte`, `dataNasc`, `idade`, `sexo`, `castrado`, `peso`, `alergias`, `medicamentos`, `ultimaVacina`, `ultimaConsulta` |
| `ChatRequest` | Requisição do chat | `pergunta` (1-1000 chars), `petContext`, `historicoMensagens` |
| `ChatResponse` | Resposta estruturada do chat | `resposta`, `categoria`, `urgencia`, `alerta_clinica_24h`, `acoes_recomendadas`, `score_xp_sugerido`, `origem_resposta` |
| `InsightsRequest` | Requisição de insights | `nome`, `raca`, `dataNasc`, `idade`, `porte`, `sexo`, `castrado`, `peso`, `alergias`, `medicamentos` |
| `InsightsResponse` | Resposta com cards preventivos | `pet_nome`, `insights` (lista de `PetInsight` contendo `titulo`, `descricao`, `categoria`, `urgencia`) |
| `TriageRequest` | Requisição de triagem clínica | `sintomas`, `tempo_sintomas`, `petContext` |
| `TriageResponse` | Resposta de triagem de sintomas | `classificacao`, `nivel_cor` (`VERDE`, `AMARELO`, `VERMELHO`), `diagnostico_provavel_ou_orientacao`, `deve_buscar_emergencia_24h`, `primeiros_socorros_seguros`, `o_que_nao_fazer` |
| `TrainingPlanRequest` | Requisição de treino positivo | `comando_ou_objetivo`, `nivel_experiencia`, `petContext` |
| `TrainingPlanResponse` | Resposta de plano de adestramento | `titulo`, `duracao_sessao_minutos`, `passos_praticos`, `dica_reforco_positivo`, `pontos_xp_recompensa` |
| `HealthCheckResponse` | Verificação de integridade | `status`, `version`, `gemini_configured`, `rag_documents_loaded` |

### 4.4. `app/prompts/system_prompts.py` — Engenharia de Prompts & Guardrails
Concentra a `SYSTEM_INSTRUCTION_CLYVO_AI` e funções construtoras de prompt. Impõe a personalidade da "Guardian AI", os guardrails éticos e a formatação compulsória em JSON.

**Funções Construtoras:**
- `build_user_prompt_with_context(pergunta, pet_context, rag_chunks)`: Consolida dados do pet ativo, trechos recuperados do ChromaDB e a pergunta do tutor em um bloco contextual delimitado.
- `build_insights_prompt(pet_context)`: Instrui a geração de 3 recomendações preventivas direcionadas ao perfil (porte, idade e castração).
- `build_triage_prompt(sintomas, pet_context)`: Exige classificação de gravidade médica com primeiros socorros seguros e advertências de contraindicações ("o que NÃO fazer").
- `build_training_prompt(comando, nivel, pet_context)`: Estrutura plano prático de 4 a 5 passos baseado no modelo R+ (Reforço Positivo) com atribuição de pontos XP.

### 4.5. `app/services/gemini_service.py` — Orquestrador GenAI Singleton
Implementa o padrão Singleton POO orientado aos princípios SOLID (SRP, OCP e DIP) e Clean Code:
- **Despacho Genérico Tipado (`_execute_structured_inference`):** Método genérico parametrizado por `TypeVar("T", bound=BaseModel)` que configura a chamada ao SDK com `response_mime_type="application/json"`, deserializa e valida o JSON retornado via `model_validate_json()` e, em caso de erro ou ausência de chave de API, invoca a fábrica de fallback correspondente de forma transparente.
- **Estratégia de Temperaturas:**
  * Triagem Clínica (`generate_triage`): `temperature = 0.1` (alta precisão determinística, minimizando variações em segurança clínica).
  * Chat & Insights (`generate_chat_response`, `generate_insights`): `temperature = 0.2` (equilíbrio entre empatia comunicativa e rigor técnico).
  * Plano de Treino (`generate_training_plan`): `temperature = 0.3` (variabilidade criativa pedagógica nos exercícios de adestramento).

### 4.6. `app/services/rag_service.py` — Base Vetorial ChromaDB & Chunking
- **Inicialização Idempotente:** Garante que a ingestão só ocorre uma vez durante o ciclo de vida da aplicação.
- **Chunking Semântico Estruturado (`_load_and_chunk_documents`):** Lê os arquivos Markdown em `app/data/knowledge_base/`, divide por seções `## ` preservando o título principal do documento e os subtítulos de seção, indexando metadados enriquecidos (`source_file`, `topic`, `section`).
- **Persistência em Disco:** Utiliza `chromadb.PersistentClient` apontando para `data/chroma_db/`, preservando a base de vetores indexada entre reinicializações.
- **Busca Semântica & Fallback Léxico:** Executa busca semântica `top_k=3` na coleção do ChromaDB. Caso o ChromaDB encontre instabilidade, aciona automaticamente o buscador léxico em memória (`_search_memory`), ranqueando chunks por intersecção de palavras-chave relevantes.

### 4.7. `app/services/fallback_service.py` — Motor Offline Determinístico
Garante 100% de disponibilidade através de um mecanismo baseado em regras e padrões de regex:
- **Expressões Regulares Compiladas:**
  * `OFF_TOPIC_REGEX`: Detecta termos alheios ao universo pet (ex: programação, matemática, política, finanças, culinária humana) e redireciona com mensagem amigável.
  * `EMERGENCY_REGEX`: Identifica toxinas críticas (chocolate, teobromina, uvas, passas, cebola, alho, xilitol, chumbinho, veneno, lírio) e sinais vitais alarmantes (convulsão, sangramento arterial, asfixia, torção gástrica), ativando imediatamente `alerta_clinica_24h = True` e categoria `EMERGENCIA`.
- **Conjuntos de Palavras-Chave:** Filtros eficientes para identificar intenções de adestramento (`BEHAVIOR_KEYWORDS`), nutrição (`NUTRITION_KEYWORDS`) e saúde preventiva (`HEALTH_KEYWORDS`).
- **Normalização de Metadados (`_extract_pet_metadata`):** Helper DRY que extrai nome, porte, idade e condição de castração do `PetContext`, tratando valores nulos e aplicando valores padrão clinicamente seguros.

---

## 🛡️ 5. Guardrails Clínicos, Éticos & Protocolos de Emergência

A integridade clínica e a segurança biológica dos animais de estimação constituem a premissa prioritária do sistema.

```text
 ┌────────────────────────────────────────────────────────────────────────┐
 │                    DIRETRIZES ÉTICAS E GUARDRAILS                      │
 ├────────────────────────────────────────────────────────────────────────┤
 │ 1. DOMÍNIO EXCLUSIVO PET:                                              │
 │    Perguntas de programação, política, receitas para humanos ou outras │
 │    temáticas não veterinárias são gentilmente recusadas.               │
 │    -> Categoria: FORA_DE_ESCOPO | Urgência: BAIXA                      │
 │                                                                        │
 │ 2. PROIBIÇÃO DE PRESCRIÇÃO ALOPÁTICA HUMANA:                           │
 │    NUNCA prescrever doses de Paracetamol, Dipirona, Ibuprofeno ou      │
 │    remédios controlados humanos sem receita veterinária presencial.    │
 │    (Paracetamol é letal para gatos e altamente tóxico para cães).      │
 │                                                                        │
 │ 3. DETECÇÃO DE EMERGÊNCIA (NÍVEL VERMELHO):                            │
 │    Relatos de veneno, chocolate, uvas, plantas tóxicas, dilatação      │
 │    gástrica ou convulsões ativam 'alerta_clinica_24h: true'.           │
 │    -> Urgência: EMERGENCIA | Ação: Encaminhar imediatamente a 24h      │
 │                                                                        │
 │ 4. PROIBIÇÃO DE EMÉTICOS CASEIROS PERIGOSOS:                           │
 │    NUNCA orientar a indução de vômito com sal ou água oxigenada.       │
 └────────────────────────────────────────────────────────────────────────┘
```

### Matriz de Classificação de Risco (Triagem Clínica)

| Nível / Cor | Classificação | Critérios Clínicos | Conduta Recomendada | Alerta 24h |
| :---: | :---: | :--- | :--- | :---: |
| **VERMELHO** | `EMERGENCIA` | Ingestão de chocolate puro/amargo, uvas, cebola, alho, xilitol, chumbinho, lírios; convulsões > 2 min; torção gástrica; hemorragia arterial; asfixia; atropelamento. | Pronto-socorro veterinário 24h imediato. Não dar remédios humanos. Manter vias aéreas livres. | **`true`** |
| **AMARELO** | `ALTA` | Vômitos ou diarreia frequentes (> 3 episódios em 12h); claudicação aguda (mancando forte); secreção ocular purulenta; febre > 39.5°C com prostração prolongada. | Consulta presencial no mesmo dia. Oferecer água em pequenas doses. Não forçar sólidos. | **`false`** |
| **VERDE** | `BAIXA` | Coceira leve eventual; adaptação gradual de ração; rotina de escovação dentária; planejamento vacinal preventivo; dúvidas de adestramento. | Manejo domiciliar, reforço positivo e agendamento de check-up de rotina na Clyvo Care. | **`false`** |

---

## 📚 6. Base de Conhecimento RAG (Knowledge Base Catalog)

Localizada no diretório `app/data/knowledge_base/`, a base vetorial é composta por 4 compêndios especializados estruturados em Markdown:

### 6.1. `adestramento_positivo.md` (Adestramento & Gamificação)
- **Princípios do Modelo R+:** Marcação de comportamento em tempo real ("Isso!"), ausência de punição aversiva e sessões curtas de 3 a 5 minutos.
- **Trilhas de Lições:**
  * Lição 1: Comando "Senta" (Nível Básico — **+15 XP**)
  * Lição 2: Comando "Fica" e Autocontrole (Nível Intermediário — **+25 XP**)
  * Lição 3: Enriquecimento Ambiental e Ansiedade de Separação (Nível Avançado — **+30 XP**)
- **Progressão de Níveis no PetGuardian:**
  * Nível 1: *Filhote Curioso* (0 a 100 XP) 🐾
  * Nível 2: *Pet Aprendiz* (101 a 300 XP) 🎓
  * Nível 3: *Guardião Dedicado* (301 a 600 XP) ⭐
  * Nível 4: *Mestre dos Comandos* (601+ XP) 🏆

### 6.2. `alimentos_toxicos.md` (Toxicologia Veterinária)
- **Tóxicos Graves:** Chocolate/cacau (teobromina e cafeína), uvas e passas (ácido tartárico e necrose tubular aguda), cebola/alho (tiossulfatos e anemia hemolítica por Corpúsculos de Heinz), xilitol (hipoglicemia fulminante e necrose hepática) e nozes de macadâmia.
- **Petiscos Saudáveis Autorizados:** Cenoura crua ou cozida sem tempero, maçã sem sementes, abóbora cozida, banana em rodelas e melancia sem sementes.

### 6.3. `cuidados_por_porte_idade.md` (Manejo Clínico por Perfil)
- **Especificidades por Porte:**
  * Pequeno (até 10kg): Prevenção de cálculo dentário (tártaro) e cardiopatia valvar mitral.
  * Médio (10 a 25kg): Gasto energético diário (45-60 min) e prevenção de sobrepeso.
  * Grande/Gigante (> 25kg): Displasia coxofemoral, condroprotetores e prevenção de dilatação/torção gástrica.
- **Especificidades por Idade:** Filhotes (vacinas V8/V10 aos 45, 65 e 85 dias + Antirrábica), Adultos (reforço anual) e Seniores 7+ anos (check-up semestral com hemograma, função renal/hepática e ecocardiograma).

### 6.4. `primeiros_socorros_emergencia.md` (Protocolos de Urgência)
- **Semáforo Clínico:** Regras determinísticas de priorização de atendimento (Vermelho, Amarelo e Verde).
- **Diretrizes Proibitivas:** Proibição de lavagem gástrica caseira e contraindicação absoluta de analgésicos humanos sem orientação médica.

---

## 🔌 7. Contratos da API REST (Endpoints & Schemas)

### 7.1. `GET /health` — Verificação de Saúde do Sistema
Verifica o status operacional da API, a conectividade com o SDK do Gemini e a contagem de documentos indexados no ChromaDB.

* **Alias:** `GET /api/v1/health`
* **Response (200 OK):**
```json
{
  "status": "ONLINE",
  "version": "1.0.0",
  "gemini_configured": true,
  "rag_documents_loaded": 12
}
```

---

### 7.2. `POST /ai/chat` — Chat Conversacional Contextualizado
Recebe a pergunta do tutor acompanhada do perfil do animal selecionado, recupera chunks relevantes via RAG e retorna resposta formatada com ações práticas e pontuação de XP.

* **Alias:** `POST /api/v1/ai/chat`
* **Request Body (Exemplo 1: Dúvida Nutricional):**
```json
{
  "pergunta": "Posso dar pedaços de cenoura ou maçã como petisco para o Thor?",
  "petContext": {
    "nome": "Thor",
    "raca": "Golden Retriever",
    "porte": "GRANDE",
    "idade": 4,
    "castrado": true,
    "peso": "32kg"
  }
}
```
* **Response (200 OK):**
```json
{
  "resposta": "Olá! Sim, você pode oferecer cenoura e maçã para o Thor! A cenoura (crua ou cozida sem sal) é excelente para cães de porte grande, pois auxilia na limpeza mecânica dos dentes e tem baixas calorias. A maçã também é muito saudável, rica em vitaminas A e C, mas lembre-se de retirar completamente todas as sementes e o miolo, pois contêm glicosídeos cianogênicos tóxicos. Ofereça em cubos moderados como recompensa positiva.",
  "categoria": "NUTRICAO",
  "urgencia": "BAIXA",
  "alerta_clinica_24h": false,
  "acoes_recomendadas": [
    "Oferecer cubos de cenoura crua como petisco crocante",
    "Remover todas as sementes da maçã antes de servir ao Thor",
    "Manter os petiscos em até 10% do total calórico diário"
  ],
  "score_xp_sugerido": 10,
  "origem_resposta": "gemini_rag"
}
```

* **Request Body (Exemplo 2: Alerta de Emergência Tóxica):**
```json
{
  "pergunta": "Minha gatinha comeu um pedaço de chocolate meio amargo que caiu no chão!",
  "petContext": {
    "nome": "Luna",
    "raca": "Siamês",
    "porte": "PEQUENO",
    "idade": 2,
    "castrado": true
  }
}
```
* **Response (200 OK):**
```json
{
  "resposta": "⚠️ ALERTA DE EMERGÊNCIA CRÍTICA: Chocolate contém teobromina e cafeína, alcaloides altamente tóxicos e potencialmente fatais para felinos como a Luna. Gatos não conseguem metabolizar essas toxinas, que causam sobrecarga cardiovascular, arritmias e convulsões rápidas. Leve a Luna imediatamente a um pronto-socorro veterinário 24h!",
  "categoria": "EMERGENCIA",
  "urgencia": "EMERGENCIA",
  "alerta_clinica_24h": true,
  "acoes_recomendadas": [
    "Transportar a Luna imediatamente ao pronto-socorro veterinário 24h",
    "Levar a embalagem do chocolate para cálculo de teobromina ingerida",
    "NÃO tentar induzir vômito em casa com água oxigenada ou sal",
    "Manter a gatinha aquecida e em ambiente silencioso no trajeto"
  ],
  "score_xp_sugerido": 0,
  "origem_resposta": "gemini_rag"
}
```

* **Request Body (Exemplo 3: Bloqueio por Guardrail Fora de Escopo):**
```json
{
  "pergunta": "Como escrever um algoritmo de busca binária em Python?",
  "petContext": {
    "nome": "Bob"
  }
}
```
* **Response (200 OK):**
```json
{
  "resposta": "Sou a Guardian AI, dedicada exclusivamente à saúde preventiva, nutrição, bem-estar e adestramento de animais de estimação. Como posso ajudar nos cuidados com o Bob hoje? 🐾",
  "categoria": "FORA_DE_ESCOPO",
  "urgencia": "BAIXA",
  "alerta_clinica_24h": false,
  "acoes_recomendadas": [
    "Perguntar sobre alimentos seguros e proibidos",
    "Solicitar dicas de adestramento positivo",
    "Consultar calendário de vacinas e vermifugação"
  ],
  "score_xp_sugerido": 0,
  "origem_resposta": "gemini_rag"
}
```

---

### 7.3. `POST /ai/insights` — Geração Automática de Insights Preventivos
Analisa o perfil biométrico do pet e gera cards de recomendações segmentadas por categoria (saúde, nutrição, rotina) e nível de urgência.

* **Alias:** `POST /api/v1/ai/insights`
* **Request Body:**
```json
{
  "nome": "Max",
  "raca": "Labrador Retriever",
  "porte": "GRANDE",
  "idade": 8,
  "castrado": true,
  "peso": "36kg",
  "alergias": "Frango"
}
```
* **Response (200 OK):**
```json
{
  "pet_nome": "Max",
  "insights": [
    {
      "titulo": "Proteção Articular e Monitoramento de Displasia",
      "descricao": "Max é um cão de porte grande com 8 anos (fase sênior). Recomenda-se suplementação com condroprotetores (glicosamina/condroitina) e passeios em piso macio para preservar as articulações.",
      "categoria": "saude",
      "urgencia": "alta"
    },
    {
      "titulo": "Nutrição Hipoalergênica e Controle de Peso",
      "descricao": "Devido à alergia a frango e metabolismo reduzido pela castração, mantenha ração com fonte proteica alternativa (cordeiro ou peixe) dosada na balança para evitar sobrepeso.",
      "categoria": "nutricao",
      "urgencia": "media"
    },
    {
      "titulo": "Check-up Geriátrico Semestral",
      "descricao": "Agende exames semestrais de sangue (função renal e hepática) e ultrassonografia abdominal preventiva na Clyvo Care.",
      "categoria": "rotina",
      "urgencia": "alta"
    }
  ]
}
```

---

### 7.4. `POST /ai/triage` — Triagem Clínica de Sintomas & Semáforo 24h
Classifica sintomas relatados pelo tutor, define a cor do semáforo de urgência, lista primeiros socorros seguros e emite avisos de contraindicação médica estrita.

* **Alias:** `POST /api/v1/ai/triage`
* **Request Body:**
```json
{
  "sintomas": "O pet comeu folhas da planta comigo-ninguém-pode no jardim, está babando excessivamente e esfregando a boca nas patas.",
  "tempo_sintomas": "há 30 minutos",
  "petContext": {
    "nome": "Pipoca",
    "porte": "PEQUENO"
  }
}
```
* **Response (200 OK):**
```json
{
  "classificacao": "EMERGENCIA",
  "nivel_cor": "VERMELHO",
  "diagnostico_provavel_ou_orientacao": "Intoxicação aguda por oxalato de cálcio insolúvel presente na planta comigo-ninguém-pode. Causa queimação intensa na mucosa oral, edema de glote e risco grave de asfixia em animais de pequeno porte.",
  "deve_buscar_emergencia_24h": true,
  "primeiros_socorros_seguros": [
    "Lavar abundantemente a cavidade oral com água corrente fria ou soro fisiológico para remover cristais aderidos",
    "Transportar imediatamente a Pipoca ao pronto-socorro veterinário 24h mais próximo",
    "Levar um ramo da planta ingerida para confirmação botânica pelo médico"
  ],
  "o_que_nao_fazer": [
    "NÃO tentar induzir vômito (o refluxo de cristais de oxalato causará nova queimação severa no esôfago)",
    "NÃO dar analgésicos humanos como Paracetamol, Dipirona ou Ibuprofeno",
    "NÃO forçar a ingestão de leite ou óleos caseiros"
  ]
}
```

---

### 7.5. `POST /ai/training/plan` — Plano de Treino Positivo & Gamificação (+XP)
Gera sessões práticas de adestramento pelo modelo de reforço positivo com passos claros, dicas de timing e pontuação gamificada de XP.

* **Alias:** `POST /api/v1/ai/training/plan`
* **Request Body:**
```json
{
  "comando_ou_objetivo": "Não pular nas visitas",
  "nivel_experiencia": "INTERMEDIARIO",
  "petContext": {
    "nome": "Zeus",
    "raca": "Border Collie"
  }
}
```
* **Response (200 OK):**
```json
{
  "titulo": "Treino Positivo: Quatro Patas no Chão para Zeus",
  "duracao_sessao_minutos": 5,
  "passos_praticos": [
    "1. Peça a uma pessoa conhecida para se aproximar de Zeus com calma.",
    "2. Se Zeus pular, a pessoa deve cruzar os braços, virar de costas e ignorar totalmente (sem toque, voz ou olhar).",
    "3. No milissegundo em que Zeus colocar as quatro patas no chão: marque verbalmente com 'Isso!' e entregue um petisco de alto valor.",
    "4. Repita a aproximação 4 vezes, recompensando unicamente o comportamento de quatro patas no chão."
  ],
  "dica_reforco_positivo": "A atenção humana funciona como recompensa. Ao retirar a atenção quando o cão pula, ele compreende rapidamente que o acerto é manter-se no chão.",
  "pontos_xp_recompensa": 25
}
```

---

## 🚀 8. Guia de Execução, Setup & Desenvolvimento Local

### 8.1. Pré-requisitos
- Python 3.10, 3.11 ou superior instalado na máquina.
- Git instalado.
- Chave de API Google Gemini (opcional, gerada gratuitamente em [Google AI Studio](https://aistudio.google.com/)).

### 8.2. Instalação Passo a Passo

```powershell
# 1. Navegar até a pasta do microserviço
cd "c:\Users\Enzo\new_backup\FIAP\_Projetos\Challenge Clyvo 3\Disruptive-Architectures-IoT-IoB-IA"

# 2. Criar o ambiente virtual Python
python -m venv venv

# 3. Ativar o ambiente virtual
# No Windows (PowerShell):
.\venv\Scripts\Activate.ps1
# No Linux / macOS:
# source venv/bin/activate

# 4. Instalar as dependências do projeto
pip install -r requirements.txt

# 5. Configurar as variáveis de ambiente
cp .env.example .env
```

### 8.3. Configuração do `.env`
Edite o arquivo `.env` para apontar as credenciais desejadas:

```ini
APP_ENV=development
PORT=8000
HOST=0.0.0.0

# Chave do Google Gemini (se omitida ou inválida, o motor de fallback assume 100% dos fluxos)
GEMINI_API_KEY=sua_chave_gemini_aqui
GEMINI_MODEL=gemini-3.5-flash-lite

# Diretório persistente do ChromaDB
CHROMA_PERSIST_DIR=./data/chroma_db

# CORS
CORS_ORIGINS=*
```

### 8.4. Execução do Servidor FastAPI

```powershell
# Iniciar o servidor Uvicorn com hot-reload ativo
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Saída esperada no terminal:
```text
INFO:     2026-09-01 12:00:00 [INFO] clyvo_ai.main: 🚀 Inicializando microserviço Guardian AI...
INFO:     2026-09-01 12:00:01 [INFO] clyvo_ai.rag: RAG ChromaDB inicializado com sucesso: 12 chunks indexados.
INFO:     2026-09-01 12:00:01 [INFO] clyvo_ai.gemini: Google GenAI conectado com o modelo gemini-3.5-flash-lite.
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

### 8.5. Validação dos Endpoints via Terminal (PowerShell / cURL)

```powershell
# 1. Healthcheck
Invoke-RestMethod -Uri "http://localhost:8000/health" -Method Get

# 2. Chat Inteligente
$body = @{
    pergunta = "Qual a dose de ração diária para um filhote de Golden de 3 meses?"
    petContext = @{
        nome = "Thor"
        raca = "Golden Retriever"
        porte = "GRANDE"
        idade = 0
    }
} | ConvertTo-Json -Depth 5

Invoke-RestMethod -Uri "http://localhost:8000/ai/chat" -Method Post -Body $body -ContentType "application/json"

# 3. Triagem de Emergência
$triageBody = @{
    sintomas = "O cachorro comeu chocolate ao leite."
    petContext = @{
        nome = "Rex"
        porte = "PEQUENO"
    }
} | ConvertTo-Json -Depth 5

Invoke-RestMethod -Uri "http://localhost:8000/ai/triage" -Method Post -Body $triageBody -ContentType "application/json"
```

---

## 🏆 9. Alinhamento com os Critérios de Avaliação FIAP (Edital)

| Critério Oficial do Edital | Pontuação | Como o Microserviço Guardian AI Atende |
| :--- | :---: | :--- |
| **Aplicação Técnica de Conceitos de IA** | **60 pts** | • Arquitetura RAG vetorial no ChromaDB com indexação semântica e contextual injection.<br>• Modelo Google Gemini 3.5 Flash Lite com System Instructions de alto rigor clínico.<br>• Guardrails de domínio estritos e semáforo de urgência com flag de socorro 24h.<br>• Gamificação pet-centric com pontuação de XP por hábitos saudáveis. |
| **Didática da Apresentação em Vídeo** | **20 pts** | • Demonstração funcional fluida ao vivo via Swagger `/docs` e integração no app React Native `AiAssistantScreen.tsx`.<br>• Demonstração de testes reais de toxicologia, nutrição e bloqueio fora de escopo. |
| **Organização do Repositório & Documentação** | **20 pts** | • Código modular estruturado em camadas (`services`, `models`, `prompts`, `data`).<br>• Tipagem integral Pydantic v2 e conformidade PEP 8.<br>• Documentação técnica exaustiva em `AGENT.md` e `README.md`. |
