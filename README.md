# 🤖 Disruptive Architectures: IoT, IoB & Generative IA — 🐾 PetGuardian

> **Guardian AI — Assistente Inteligente de Saúde Preventiva, Triagem Clínica e Adestramento Gamificado**
> 
> *Challenge Clyvo 2026 — 2º Semestre (FIAP — 2TDSPG)*  
> *Atendimento Integral aos Critérios Oficiais das Páginas 17, 18 e 19 do Edital*

---

## 👥 Integrantes do Grupo (Ordem Alfabética Estrita)

| Nome Completo | RM | Turma | Papel / Foco Técnico | GitHub | LinkedIn |
| :--- | :---: | :---: | :--- | :--- | :--- |
| **Enzo Okuizumi** | **561432** | 2TDSPG | Mobile Development, Integração API Java e Coordenação Geral | [EnzoOkuizumiFiap](https://github.com/EnzoOkuizumiFiap) | [LinkedIn](https://www.linkedin.com/in/enzo-okuizumi-b60292256/) |
| **Gustavo Okada** | **563428** | 2TDSPG | Java Advanced (Spring Security, Flyway e SOLID) & .NET Observabilidade | [Gdev3356](https://github.com/Gdev3356) | [LinkedIn](https://www.linkedin.com/in/gustavo-okada-53a3b8359/) |
| **Lucas Barros Gouveia** | **566422** | 2TDSPG | Database Advanced (PL/SQL, Funções, Procedures e Triggers DML) | [LuzBGouveia](https://github.com/LuzBGouveia) | [LinkedIn](https://www.linkedin.com/in/lucas-barros-gouveia-09b147355/) |
| **Luna de Carvalho Guimarães** | **562290** | 2TDSPG | Disruptive Architectures (IA Generativa, RAG, FastAPI, ChromaDB e Chat) | [lunaguima](https://github.com/lunaguima) | [LinkedIn](https://www.linkedin.com/in/luna-m-guimar%C3%A3es-1850ab173/) |
| **Milton Marcelino** | **564836** | 2TDSPG | DevOps Tools & Cloud Computing (Azure CLI, ACR, ACI e Containers) | [MiltonMarcelino](https://github.com/MiltonMarcelino) | [LinkedIn](http://linkedin.com/in/milton-marcelino-250298142) |

---

## 🔗 Repositório GitHub & Vídeo Pitch Oficial

* **Repositório GitHub:** [https://github.com/Challenge-Pet-Guardian-3/Disruptive-Architectures-IoT-IoB-IA](https://github.com/Challenge-Pet-Guardian-3/Disruptive-Architectures-IoT-IoB-IA)
* **Vídeo Pitch no YouTube (Modo Não Listado - 5 min):** [https://youtube.com/watch?v=SEU_VIDEO_AQUI]()

---

## 🎯 1. Definição do Problema de Negócio & Proposta de Valor

### O Desafio na Jornada do Tutor e da Clínica Clyvo
Tutores enfrentam frequentes incertezas sobre sinais clínicos, dosagens de petiscos, alimentos proibidos e técnicas de adestramento. Frequentemente, recorrem a buscas genéricas na internet ou fóruns não verificados, o que leva a duas falhas graves de jornada:
1. **Pânico desnecessário** ou aplicação de remédios humanos letais (como Paracetamol ou lavagem com água oxigenada).
2. **Subestimação de sintomas críticos** (como ingestão de chocolate ou uvas), atrasando a ida ao pronto-socorro veterinário 24h.

### A Solução Guardian AI (PetGuardian)
O **Guardian AI** é um microserviço inteligente em Python que atua como copiloto preventivo e educacional:
- **Personalização Ativa:** A IA analisa as características do animal ativo (espécie, raça, porte, idade, castração, histórico recente) para contextualizar suas respostas.
- **Guardrails Éticos & Segurança:** A IA recusa categoricamente assuntos não relacionados a pets e **nunca** prescreve medicamentos controlados sem consulta presencial.
- **RAG com ChromaDB:** Base vetorial com guias de toxicologia e reforço positivo para enriquecer a geração com fontes médicas verificadas.
- **Gamificação Pet-Centric:** Sugere pontuação de experiência (+XP) ao pet pela prática de comandos e hábitos preventivos.

---

## 🧠 2. Justificativa Técnica da Abordagem de IA

| Abordagem Adotada | Por que foi escolhida? | Papel no Sistema |
| :--- | :--- | :--- |
| **LLM (Google Gemini 3.5 Flash Lite)** | Baixa latência, altíssima aderência a System Instructions e capacidade nativa de formatação JSON estruturada. | Raciocínio clínico de alto nível, tom empático e redação de orientações claras ao tutor. |
| **RAG (Retrieval-Augmented Generation)** | Reduz alucinações a quase zero ao ancorar as respostas em corpus veterinário curado. | Busca semântica por similaridade de cosseno de alimentos tóxicos, protocolos de primeiros socorros e reforço positivo. |
| **Base Vetorial (ChromaDB)** | Banco de vetores leve, persistente em disco e de fácil integração com Python. | Indexação e recuperação semântica `top_k=3` dos chunks de documentos Markdown. |
| **Guardrails de Domínio & Clínicos** | Regras determinísticas de barreira antes e durante a geração. | Bloqueio de assuntos desconexos (política, matemática, código) e proibição de prescrição de medicamentos alopáticos. |
| **Motor de Fallback Local** | Garante 100% de disponibilidade mesmo sem internet ou sem chave de API. | Respostas curadas em regras determinísticas para testes locais e bancas sem interrupções. |

---

## 🏗️ 3. Diagrama de Arquitetura & Fluxo de Dados

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

---

## 📊 4. Dicionário de Dados Utilizados pela IA

| Dado do Pet | Origem | Estrutura | Finalidade na IA |
| :--- | :--- | :--- | :--- |
| `nome` | Mobile / BD | `string` | Personalização nominal e humanização da resposta. |
| `raca` | Mobile / BD | `string` | Identificação de predisposições genéticas e comportamentais. |
| `porte` | Mobile / BD | `PEQUENO`, `MEDIO`, `GRANDE` | Ajuste de cálculo calórico, risco articular e saúde bucal. |
| `idade` | Mobile / BD | `number` (anos) | Diferenciação de cuidados (Filhote vs Adulto vs Sênior). |
| `castrado` | Mobile / BD | `boolean` | Orientações sobre controle metabólico e prevenção de tumores. |
| `alergias` | Mobile / BD | `string` | Guardrail contra indicação de alimentos alergênicos. |
| `medicamentos`| Mobile / BD | `string` | Alerta de contraindicação medicamentosa. |
| `sintomas` | Input do Tutor | `string` | Triagem clínica e classificação de urgência (Verde, Amarelo, Vermelho). |

---

## 🔌 5. Especificação dos Endpoints REST

A documentação interativa Swagger está disponível em: `http://localhost:8000/docs`

### 1. `POST /ai/chat` (Chat com Guardrails & Contexto)
* **Request:**
```json
{
  "pergunta": "Meu cachorro comeu um pedaço de chocolate ao leite, o que devo fazer?",
  "petContext": {
    "nome": "Thor",
    "raca": "SRD",
    "porte": "PEQUENO",
    "idade": 3,
    "castrado": true
  }
}
```
* **Response (200 OK):**
```json
{
  "resposta": "⚠️ ALERTA DE EMERGÊNCIA: Chocolate contém teobromina, substância altamente tóxica para cães como o Thor. Como ele é de porte pequeno, a concentração tóxica no organismo é atingida rapidamente. Leve-o imediatamente a um pronto-socorro veterinário 24h.",
  "categoria": "EMERGENCIA",
  "urgencia": "EMERGENCIA",
  "alerta_clinica_24h": true,
  "acoes_recomendadas": [
    "Transportar o pet imediatamente a uma clínica veterinária 24h",
    "Não tentar induzir vômito em casa sem orientação médica",
    "Levar a embalagem do chocolate para estimar a quantidade ingerida"
  ],
  "score_xp_sugerido": 0,
  "origem_resposta": "gemini_flash_gemini-3.5-flash-lite"
}
```

### 2. `POST /ai/insights` (Recomendações Preventivas Automáticas)
* **Request:**
```json
{
  "nome": "Pipoca",
  "raca": "Poodle",
  "porte": "PEQUENO",
  "idade": 8,
  "castrado": false
}
```
* **Response (200 OK):**
```json
{
  "pet_nome": "Pipoca",
  "insights": [
    {
      "titulo": "Higiene Bucal e Prevenção de Tártaro",
      "descricao": "Cães de porte pequeno têm alta tendência ao tártaro. Escovação 3x na semana previne periodontite.",
      "categoria": "saude",
      "urgencia": "baixa"
    },
    {
      "titulo": "Fase Sênior: Check-up Preventivo",
      "descricao": "Pipoca tem 8 anos. Exames de sangue semestrais e ecocardiograma garantem longevidade.",
      "categoria": "saude",
      "urgencia": "alta"
    }
  ]
}
```

### 3. `POST /ai/triage` (Triagem Clínica de Sintomas)
* **Request:**
```json
{
  "sintomas": "O pet está vomitando e prostrado após mastigar uma folha de comigo-ninguém-pode.",
  "petContext": { "nome": "Mel", "porte": "MEDIO" }
}
```

### 4. `POST /ai/training/plan` (Plano de Treino Gamificado +XP)
* **Request:**
```json
{
  "comando_ou_objetivo": "Senta",
  "nivel_experiencia": "INICIANTE",
  "petContext": { "nome": "Rex" }
}
```

---

## 🚀 6. Como Executar Localmente

### Pré-requisitos
- Python 3.10, 3.11 ou superior
- Pip e venv instalados

```bash
# 1. Clonar o repositório
git clone https://github.com/Challenge-Pet-Guardian-3/Disruptive-Architectures-IoT-IoB-IA.git
cd Disruptive-Architectures-IoT-IoB-IA

# 2. Criar e ativar o ambiente virtual
python -m venv venv

# No Windows (PowerShell):
.\venv\Scripts\Activate.ps1
# No Linux/macOS:
source venv/bin/activate

# 3. Instalar as dependências
pip install -r requirements.txt

# 4. Configurar variáveis de ambiente
cp .env.example .env
# Edite o arquivo .env e adicione sua GEMINI_API_KEY se desejar (opcional, fallback funciona 100%)

# 5. Executar a aplicação FastAPI
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

* **Swagger UI:** [http://localhost:8000/docs](http://localhost:8000/docs)
* **Health Check:** [http://localhost:8000/health](http://localhost:8000/health)

---

## 🎬 7. Roteiro Sugerido para o Vídeo Pitch (5 Minutos)

| Minuto | Bloco da Apresentação | Conteúdo & Demonstração |
| :---: | :--- | :--- |
| **0:00 - 1:00** | **Introdução & Problema de Negócio** | Apresentação da equipe, proposta da Clyvo Vet e como a IA resolve a insegurança do tutor e a sobrecarga clínica. |
| **1:00 - 2:00** | **Arquitetura Técnica (LLM + RAG + Guardrails)** | Explicação da stack (FastAPI, Google Gemini Flash, ChromaDB) e do fluxo de dados centrado no pet. |
| **2:00 - 3:30** | **Demonstração Funcional Integrada** | Demonstração ao vivo no app Mobile: troca de pet, personalização nominal, pergunta de nutrição e teste de emergência com chocolate. |
| **3:30 - 4:15** | **Guardrail em Ação** | Demonstração do bloqueio de perguntas fora de escopo (ex: pedir código de programação) e segurança clínica. |
| **4:15 - 5:00** | **Benefícios para Clínica e Tutor & Conclusão** | Fidelização na Clyvo Care, agendamentos preventivos e encerramento. |