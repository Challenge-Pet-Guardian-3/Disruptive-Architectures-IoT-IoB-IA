# 🤖 Disruptive Architectures: IoT, IoB & Generative IA — 🐾 PetGuardian

> **Clyvo AI — Assistente Inteligente de Saúde Preventiva e Treinamento do Pet**
> 
> *Challenge Clyvo 2026 — 2º Semestre (FIAP — 2TDSPG)*

---

## 👥 Integrantes

| Nome | RM | Turma | GitHub | LinkedIn |
| :--- | :---: | :---: | :--- | :--- |
| **Enzo Okuizumi** | **561432** | 2TDSPG | [EnzoOkuizumiFiap](https://github.com/EnzoOkuizumiFiap) | [Enzo Okuizumi](https://www.linkedin.com/in/enzo-okuizumi-b60292256/) |
| **Gustavo Okada** | **563428** | 2TDSPG | [Gdev3356](https://github.com/Gdev3356) | [Gustavo Okada](https://www.linkedin.com/in/gustavo-okada-53a3b8359/) |
| **Lucas Barros Gouveia** | **566422** | 2TDSPG | [LuzBGouveia](https://github.com/LuzBGouveia) | [Lucas Barros Gouveia](https://www.linkedin.com/in/lucas-barros-gouveia-09b147355/) |
| **Luna de Carvalho Guimarães** | **562290** | 2TDSPG | [lunaguima](https://github.com/lunaguima) | [Luna M. Guimarães](https://www.linkedin.com/in/luna-m-guimar%C3%A3es-1850ab173/) |
| **Milton Marcelino** | **564836** | 2TDSPG | [MiltonMarcelino](https://github.com/MiltonMarcelino) | [Milton Marcelino](http://linkedin.com/in/milton-marcelino-250298142) |

---

## 🔗 Repositório GitHub & Vídeo de Apresentação (Pitch)

* **Repositório GitHub:** [https://github.com/Challenge-Pet-Guardian-3/Disruptive-Architectures-IoT-IoB-IA](https://github.com/Challenge-Pet-Guardian-3/Disruptive-Architectures-IoT-IoB-IA)
* **Vídeo Pitch no YouTube (Não Listado):** [https://youtube.com/watch?v=SEU_VIDEO_AQUI]()

---

## 💡 1. Visão Geral da Solução

O módulo **Clyvo AI** do **PetGuardian** evolui a disciplina de Disruptive Architectures da abordagem focada em hardware/sensores para um ecossistema inteligente de software centrado no animal (**Arquitetura Pet-Centric**), combinando:
1. **Aplicação Backend em Python (FastAPI):** API assíncrona de alta performance com tipagem Pydantic V2.
2. **Camada de Inteligência Artificial Generativa:** LLM Engine (Google Gemini 1.5 Flash / OpenAI) orquestrado com **LangChain / LlamaIndex**.
3. **RAG Vetorial (Retrieval-Augmented Generation):** Base de conhecimento indexada no **ChromaDB** com protocolos clínicos veterinários, alimentos tóxicos para cães/gatos e guias de adestramento positivo.
4. **Gamificação Pet-Centric:** Pontuação e evolução de nível atribuídos diretamente ao **Pet** (`score_bem_estar` / `pontos_bem_estar`) após execução de módulos de adestramento e rotinas preventivas.
5. **Página Dedicada no Frontend (`AiAssistantScreen`):** Interface de conversação fluida no aplicativo React Native, com atalhos de triagem rápida e recomendação de clínicas 24h em emergências.

---

## 🏗️ 2. Arquitetura da Aplicação

```text
📱 App Mobile (AiAssistantScreen) / Web
             │
             ▼ [HTTP POST /api/v1/chat]
┌──────────────────────────────────────────────────────────┐
│             🐍 FastAPI Backend Application               │
│                                                          │
│  1. Ingestão e Sanitização do Prompt (Pydantic Schema)   │
│  2. Consulta de Perfil do Pet no Banco de Dados          │
│  3. Busca Semântica na Base Vetorial RAG (ChromaDB)      │
│  4. Montagem do Prompt Enriquecido (Context Injection)   │
│  5. Invocação da LLM Engine com Guardrails de Segurança  │
│  6. Serialização Estruturada da Resposta JSON             │
└──────────────────────────────────────────────────────────┘
             │                                   │
             ▼                                   ▼
    🗄️ Banco de Dados Relacional        🤖 LLM Cloud Engine
    (Histórico Clínico, Vacinas)      (Gemini / OpenAI API)
```

---

## 🔌 3. Especificação dos Endpoints REST

### `POST /api/v1/chat`
Envia mensagem do tutor para a IA com injeção automática de contexto do animal.

* **Request Body:**
```json
{
  "pet_id": 1,
  "tutor_id": 1,
  "mensagem": "Meu cachorro comeu um pedaço de chocolate ao leite, o que devo fazer?"
}
```

* **Response Body (200 OK):**
```json
{
  "resposta": "⚠️ Chocolate contém teobromina, substância altamente tóxica para cães. Como seu cão é de porte pequeno (5kg), recomendamos levá-lo imediatamente a uma clínica veterinária 24h para indução de vômito segura.",
  "categoria": "EMERGENCIA",
  "score_xp": 0,
  "alerta_clinica_24h": true,
  "acoes_recomendadas": [
    "Buscar pronto-socorro veterinário 24h mais próximo",
    "Não induzir vômito em casa sem orientação médica",
    "Levar a embalagem do chocolate para estimativa de dose"
  ]
}
```

### `GET /api/v1/pet/{id}/recommendations`
Gera recomendações preventivas de saúde, vacinas pendentes e sugestões de treinamento do Pet.

---

## 🚀 4. Como Executar Localmente

### Pré-requisitos:
* Python 3.11+ instalado
* Virtualenv configurado

```bash
# 1. Clonar o repositório
git clone https://github.com/Challenge-Pet-Guardian-3/Disruptive-Architectures-IoT-IoB-IA.git
cd Disruptive-Architectures-IoT-IoB-IA

# 2. Criar e ativar o ambiente virtual
python -m venv venv
# Windows:
.\venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate

# 3. Instalar dependências
pip install -r requirements.txt

# 4. Configurar variáveis de ambiente
cp .env.example .env

# 5. Executar o servidor FastAPI
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

* **Documentação Interativa (Swagger):** `http://localhost:8000/docs`
* **Health Check:** `http://localhost:8000/health`