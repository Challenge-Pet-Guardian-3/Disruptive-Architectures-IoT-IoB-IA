# 📋 Backlog Master Azure Boards — Sprint 3: Disruptive Architectures (IoT, IoB & IA)

> **Projeto Integrado:** PetGuardian / Clyvo Care (Challenge FIAP 2026 - 2º Ano ADS / 2TDSPG)  
> **Disciplina:** Disruptive Architectures: IoT, IoB & Generative IA (FIAP — 2TDSPG)  
> **Epic Principal:** `[EPIC] Sprint 3 - Disruptive Architectures: Aplicação Python com IA Generativa, RAG e Integração Frontend`  
> **Start Date:** `2026-08-30`  
> **Target Date:** `2026-09-05`  
> **Arquitetura da Solução:** Aplicação Backend em Python (FastAPI + SQLAlchemy/Oracle) + IA Generativa (LLM/RAG ChromaDB) + Página Dedicada de IA no Frontend (React Native)  
> **Padrão:** Azure Boards (Scrum Process: Epic ➔ Feature ➔ PBI ➔ Task)  
> **Diretrizes Estratégicas:** Transição do IoT para IA Generativa centrada no animal, extração de dados reais do Pet no banco, base vetorial RAG com guardrails e gamificação (+XP).

---

## 🎯 1. Matriz de Requisitos & Critérios de Avaliação Oficiais (Páginas 17 a 19)

| Critério Avaliativo | Pontuação | Requisitos Obrigatórios da Banca (Slides 17 a 19) |
| :--- | :---: | :--- |
| **Aplicação Técnica de Conceitos de IA** | **60 pts** | • Definição clara do problema de negócio na jornada do pet.<br>• Escolha e justificativa técnica da abordagem de IA (LLM, RAG, NLP, Guardrails).<br>• Identificação e estruturação do fluxo de dados (perfil do pet, consultas, vacinas, peso, treinos).<br>• Demonstração da personalização, priorização de ações e apoio à tomada de decisão do tutor/clínica. |
| **Clareza e Didática da Apresentação em Vídeo** | **20 pts** | • Gravação de **Vídeo Pitch de aproximadamente 5 minutos** (máximo).<br>• Publicado no YouTube em modo **Não Listado**.<br>• Demonstração funcional (ao vivo no frontend e backend) dos recursos inteligentes de IA. |
| **Organização do Repositório & Documentação Técnica** | **20 pts** | • Repositório no GitHub organizado com código-fonte Python limpo e modular.<br>• **README.md completo** com instruções de execução, tecnologias utilizadas, arquitetura e resultados parciais.<br>• Diagrama arquitetural ilustrando a comunicação (Frontend ➔ Backend Python ➔ Banco de Dados ➔ Componentes de IA). |

---

## 🌳 2. Estrutura Hierárquica no Azure Boards

```text
[EPIC] Sprint 3 - Disruptive Architectures: Aplicação Python com IA Generativa, RAG e Integração Frontend
│
├── 🏆 [FEATURE 01] Modelagem do Problema, Engenharia de Prompts e Arquitetura de IA
│   ├── 📄 [PBI-01] Definição do Problema de Negócio e Jornada Contínua de Cuidado do Pet com IA (1 pt)
│   │   ├── 🔹 Task 1.1: Elaborar documento de proposta de valor e jornada do pet (1.5h)
│   │   └── 🔹 Task 1.2: Mapear cenários de intervenção proativa da IA (1.5h)
│   └── 📄 [PBI-02] Escolha e Justificativa Técnica da Abordagem de IA (LLM + RAG + Guardrails) (1 pt)
│       ├── 🔹 Task 2.1: Redigir a fundamentação técnica de IA Generativa e RAG (1.5h)
│       └── 🔹 Task 2.2: Desenvolver e testar templates de System Prompt com Guardrails (1.5h)
│
├── 🏆 [FEATURE 02] Camada de Persistência & Extração de Contexto do Pet no Banco de Dados
│   ├── 📄 [PBI-03] Implementação do Data Layer Python (SQLAlchemy) e Queries do Histórico do Pet (1 pt)
│   │   ├── 🔹 Task 3.1: Configurar conexão com o banco e modelos ORM SQLAlchemy (2.5h)
│   │   └── 🔹 Task 3.2: Implementar repositório e consolidação do contexto do pet (2.5h)
│   └── 📄 [PBI-04] Implementação da Base de Conhecimento Vetorial RAG (ChromaDB) (2 pts)
│       ├── 🔹 Task 4.1: Curar e formatar documentos de conhecimento veterinário (2.5h)
│       └── 🔹 Task 4.2: Desenvolver módulo de ingestão e busca semântica no ChromaDB (3.5h)
│
├── 🏆 [FEATURE 03] Aplicação Backend Python (FastAPI) & Orquestração de IA
│   ├── 📄 [PBI-05] Desenvolvimento da API REST FastAPI com Endpoints de Chat, Triagem e Treino (2 pts)
│   │   ├── 🔹 Task 5.1: Estruturar projeto FastAPI com routers e middlewares (2.0h)
│   │   ├── 🔹 Task 5.2: Implementar orquestração LLM + RAG + Banco em ai_service.py (3.0h)
│   │   └── 🔹 Task 5.3: Criar schemas Pydantic e testes de integração das rotas (2.0h)
│   └── 📄 [PBI-06] Elaboração do Diagrama Arquitetural de Fluxo de Dados e Integração Ponta a Ponta (1 pt)
│       ├── 🔹 Task 6.1: Desenvolver diagrama visual com blocos e setas numeradas (2.5h)
│       └── 🔹 Task 6.2: Redigir documentação descritiva do fluxo de dados (1.5h)
│
├── 🏆 [FEATURE 04] Integração Frontend: Página Dedicada da IA & Gamificação do Pet
│   ├── 📄 [PBI-07] Desenvolvimento da Página Dedicada da IA no Frontend (Chat, Chips & Cards) (2 pts)
│   │   ├── 🔹 Task 7.1: Construir interface visual da tela dedicada com chat e UI (3.0h)
│   │   └── 🔹 Task 7.2: Integrar tela com API Python e gerenciar estado da conversa (3.0h)
│   └── 📄 [PBI-08] Módulo de Treinamento com Gamificação do Pet e Triagem de Emergência 24h (1 pt)
│       ├── 🔹 Task 8.1: Implementar lógica de cálculo e persistência de XP do pet (2.5h)
│       └── 🔹 Task 8.2: Construir componente visual de triagem com botão 24h (2.5h)
│
└── 🏆 [FEATURE 05] Repositório Técnico, Documentação README e Vídeo Pitch Oficial
    ├── 📄 [PBI-09] Estruturação do Repositório GitHub e README.md Completo com Instruções (1 pt)
    │   ├── 🔹 Task 9.1: Configurar estrutura de pastas, .gitignore e requirements.txt (1.5h)
    │   └── 🔹 Task 9.2: Redigir README.md técnico com guia de execução e exemplos (1.5h)
    └── 📄 [PBI-10] Roteiro, Demonstração Funcional e Vídeo Pitch de 5 Minutos (YouTube) (1 pt)
        ├── 🔹 Task 10.1: Elaborar roteiro e preparar ambiente com dados reais (2.5h)
        └── 🔹 Task 10.2: Gravar, revisar e publicar vídeo pitch no YouTube (3.5h)
```

---

## 📊 3. Tabela Resumo do Backlog

| Feature Pai | ID do PBI | Título do Item de Backlog (PBI) | Story Points | Prioridade | Horas Estimadas |
| :--- | :--- | :--- | :---: | :---: | :---: |
| **[FEATURE 01] Modelagem & IA** | **PBI-01** | Definição do Problema de Negócio e Jornada do Pet com IA | 1 pts | 1 - Critical | 3.0h |
| | **PBI-02** | Escolha e Justificativa Técnica da Abordagem de IA | 1 pts | 1 - Critical | 3.0h |
| **[FEATURE 02] Banco & RAG** | **PBI-03** | Data Layer Python (SQLAlchemy) & Queries do Histórico do Pet | 1 pts | 1 - Critical | 5.0h |
| | **PBI-04** | Base de Conhecimento Vetorial RAG de Treinos e Saúde | 2 pts | 1 - Critical | 6.0h |
| **[FEATURE 03] Backend Python** | **PBI-05** | API Backend FastAPI com Orquestração LLM e Schemas Pydantic | 2 pts | 1 - Critical | 7.0h |
| | **PBI-06** | Diagrama Arquitetural de Fluxo de Dados e Integração | 1 pts | 1 - Critical | 4.0h |
| **[FEATURE 04] Frontend & IA** | **PBI-07** | Página Dedicada da IA no Frontend (Chat, Chips & Cards) | 2 pts | 1 - Critical | 6.0h |
| | **PBI-08** | Módulo de Treinamento com Gamificação do Pet e Triagem 24h | 1 pts | 2 - High | 5.0h |
| **[FEATURE 05] Docs & Pitch** | **PBI-09** | README.md Técnico e Organização do Repositório GitHub | 1 pts | 1 - Critical | 3.0h |
| | **PBI-10** | Roteiro, Demonstração Funcional e Vídeo Pitch (5 min) | 1 pts | 1 - Critical | 6.0h |
| **TOTAL CONSOLIDADO** | **5 Features** | **10 PBIs / 21 Child Tasks Técnicas** | **13 pts** | — | **48.0h** |

---

## 📦 4. Detalhamento dos Itens de Trabalho (Épico, Features, PBIs e Tasks)

---

### 🏛️ ÉPICO
* **Work Item Type:** `Epic`
* **Title:** `[EPIC] Sprint 3 - Disruptive Architectures: Aplicação Python com IA Generativa, RAG e Integração Frontend`
* **Tags:** `Sprint3, DisruptiveArchitectures, Python, FastAPI, GenAI, RAG, ChromaDB, Gemini, Frontend`
* **Start Date:** `2026-08-30`
* **Target Date:** `2026-09-05`
* **Priority:** `1 - Critical`
* **Effort (Story Points):** `13`
* **Business Value:** `100`
* **Description:** Construção de um ecossistema inteligente de IA Generativa em Python (FastAPI + SQLAlchemy) conectado ao banco de dados relacional (Oracle/PostgreSQL), base de conhecimento vetorial RAG (ChromaDB), Guardrails veterinários e interface conversacional integrada no Frontend (React Native).

---

### 🏆 [FEATURE 01] Modelagem do Problema, Engenharia de Prompts e Arquitetura de IA
* **Work Item Type:** `Feature`
* **Parent:** `[EPIC] Sprint 3 - Disruptive Architectures: Aplicação Python com IA Generativa, RAG e Integração Frontend`
* **Title:** `[FEATURE 01] Modelagem do Problema, Engenharia de Prompts e Arquitetura de IA`
* **Tags:** `Sprint3, DisruptiveArchitectures, PromptEngineering, BusinessProblem, Guardrails`
* **Start Date:** `2026-08-30`
* **Target Date:** `2026-08-31`
* **Priority:** `1 - Critical`
* **Effort (Story Points):** `2`
* **Description:** Definição do problema de negócio na jornada contínua de cuidado do pet e escolha fundamentada da abordagem de IA Generativa, RAG e Guardrails.

#### 🔹 [PBI-01] Definição do Problema de Negócio e Jornada Contínua de Cuidado do Pet com IA
* **Work Item Type:** `Product Backlog Item`
* **Parent Feature:** `[FEATURE 01] Modelagem do Problema, Engenharia de Prompts e Arquitetura de IA`
* **State:** `Approved`
* **Priority:** `1 - Critical`
* **Effort (Story Points):** `1`
* **Tags:** `Sprint3, DisruptiveArchitectures, BusinessProblem, PetCareJourney`

##### Descrição (História de Usuário)
> **Como** Product Owner e Arquiteto de Soluções,  
> **Eu quero** mapear e documentar o problema de negócio da Clyvo Vet na jornada contínua de cuidado do pet e o valor gerado pela IA,  
> **Para que** a aplicação em Python atenda com precisão às necessidades do tutor e da clínica veterinária, cumprindo os requisitos da Sprint 3.

##### Critérios de Aceite (Acceptance Criteria / Definition of Done)
- [ ] Mapeamento da jornada do pet: Perfil cadastrado ➔ Alimentação dos dados no banco ➔ Leitura contextual pela IA ➔ Planos de treino positivos ➔ Acompanhamento de peso ➔ Triagem de sintomas.
- [ ] Especificação do valor entregue para os 3 pilares: Bem-estar do pet, tranquilidade do tutor e retenção/fidelização para a clínica veterinária.
- [ ] Descrição de como a IA realiza personalização ativa com base no histórico real armazenado no banco.

##### Tarefas Técnicas (Child Tasks)
* **Task 1.1:** [TASK-01] Elaborar documento de proposta de valor e jornada do pet. *(Activity: Requirements, Est: 1.5h)*
  * *Descrição:* Redigir análise descritiva da atuação do assistente inteligente na rotina diária do animal.
* **Task 1.2:** [TASK-02] Mapear cenários de intervenção proativa da IA. *(Activity: Requirements, Est: 1.5h)*
  * *Descrição:* Documentar regras de acionamento de orientações personalizadas conforme dados históricos.

---

#### 🔹 [PBI-02] Escolha e Justificativa Técnica da Abordagem de IA (LLM + RAG + Guardrails)
* **Work Item Type:** `Product Backlog Item`
* **Parent Feature:** `[FEATURE 01] Modelagem do Problema, Engenharia de Prompts e Arquitetura de IA`
* **State:** `Approved`
* **Priority:** `1 - Critical`
* **Effort (Story Points):** `1`
* **Tags:** `Sprint3, DisruptiveArchitectures, Architecture, LLM, RAG, Guardrails`

##### Descrição (História de Usuário)
> **Como** Engenheiro de IA,  
> **Eu quero** justificar tecnicamente a escolha de LLM (Gemini/OpenAI) combinada com RAG vetorial e Guardrails éticos,  
> **Para que** a solução apresente embasamento técnico consistente, minimizando alucinações médicas e garantindo segurança operacional.

##### Critérios de Aceite (Acceptance Criteria / Definition of Done)
- [ ] Justificativa técnica formal da combinação de LLM + RAG vs. modelos puramente estatísticos.
- [ ] Definição de System Prompts com diretrizes veterinárias, tom acolhedor e persona "Assistente Clyvo".
- [ ] Configuração de guardrails éticos: restrição explícita para não prescrever medicamentos controlados e recomendação mandatória de consulta em emergências.

##### Tarefas Técnicas (Child Tasks)
* **Task 2.1:** [TASK-03] Redigir a fundamentação técnica da arquitetura de IA Generativa e RAG. *(Activity: Design, Est: 1.5h)*
  * *Descrição:* Detalhar a escolha do modelo LLM, estratégia de chunking e similaridade vetorial.
* **Task 2.2:** [TASK-04] Desenvolver e testar os templates de System Prompt com Guardrails. *(Activity: Development, Est: 1.5h)*
  * *Descrição:* Criar arquivos de prompts parametrizados com injeção segura de variáveis do pet e saída JSON.

---

### 🏆 [FEATURE 02] Camada de Persistência & Extração de Contexto do Pet no Banco de Dados
* **Work Item Type:** `Feature`
* **Parent:** `[EPIC] Sprint 3 - Disruptive Architectures: Aplicação Python com IA Generativa, RAG e Integração Frontend`
* **Title:** `[FEATURE 02] Camada de Persistência & Extração de Contexto do Pet no Banco de Dados`
* **Tags:** `Sprint3, DisruptiveArchitectures, Database, SQLAlchemy, ChromaDB, VectorStore`
* **Start Date:** `2026-08-31`
* **Target Date:** `2026-09-01`
* **Priority:** `1 - Critical`
* **Effort (Story Points):** `3`
* **Description:** Camada de persistência relacional com SQLAlchemy e base de conhecimento vetorial RAG no ChromaDB para contextualização das respostas da IA.

#### 🔹 [PBI-03] Implementação do Data Layer Python (SQLAlchemy) e Queries do Histórico do Pet
* **Work Item Type:** `Product Backlog Item`
* **Parent Feature:** `[FEATURE 02] Camada de Persistência & Extração de Contexto do Pet no Banco de Dados`
* **State:** `Approved`
* **Priority:** `1 - Critical`
* **Effort (Story Points):** `1`
* **Tags:** `Sprint3, DisruptiveArchitectures, Database, SQLAlchemy, Python, DataLayer`

##### Descrição (História de Usuário)
> **Como** Desenvolvedor Backend Python,  
> **Eu quero** criar a camada de conexão com o Banco de Dados relacional (Oracle/PostgreSQL) para consultar o perfil e histórico do pet,  
> **Para que** o assistente de IA receba automaticamente os dados reais do animal (idade, raça, vacinas, pesagens e treinos) para compor o contexto da resposta.

##### Critérios de Aceite (Acceptance Criteria / Definition of Done)
- [ ] Configuração do motor de banco de dados com SQLAlchemy lendo credenciais via `.env`.
- [ ] Mapeamento das tabelas de negócio: `TB_PET`, `TB_HISTORICO_SAUDE`, `TB_VACINA`, `TB_PESAGEM`, `TB_TREINAMENTO`.
- [ ] Criação de função de serviço `get_pet_full_context(pet_id: int)` que consolida esses dados para injeção no prompt.
- [ ] Função para salvar no banco os pontos ganhos pelo pet após a conclusão de uma sessão de treino.

##### Tarefas Técnicas (Child Tasks)
* **Task 3.1:** [TASK-05] Configurar conexão com o banco e modelos ORM SQLAlchemy. *(Activity: Development, Est: 2.5h)*
  * *Descrição:* Escrever `src/database/connection.py` e `src/database/models.py` com o mapeamento ORM.
* **Task 3.2:** [TASK-06] Implementar repositório de dados e consolidação do contexto do pet. *(Activity: Development, Est: 2.5h)*
  * *Descrição:* Criar `src/repositories/pet_repository.py` com queries para recuperar histórico clínico e treinos.

---

#### 🔹 [PBI-04] Implementação da Base de Conhecimento Vetorial RAG (ChromaDB)
* **Work Item Type:** `Product Backlog Item`
* **Parent Feature:** `[FEATURE 02] Camada de Persistência & Extração de Contexto do Pet no Banco de Dados`
* **State:** `Approved`
* **Priority:** `1 - Critical`
* **Effort (Story Points):** `2`
* **Tags:** `Sprint3, DisruptiveArchitectures, RAG, ChromaDB, Embeddings, VectorStore`

##### Descrição (História de Usuário)
> **Como** Especialista em IA,  
> **Eu quero** criar uma base vetorial indexada com materiais técnicos de adestramento positivo, cuidados preventivos e nutrição pet,  
> **Para que** o assistente utilize RAG para enriquecer as respostas da LLM com fontes confiáveis e especializadas.

##### Critérios de Aceite (Acceptance Criteria / Definition of Done)
- [ ] Criação do corpus de documentos técnicos em `data/knowledge_base/` cobrindo adestramento, alimentos tóxicos e primeiros socorros.
- [ ] Pipeline de chunking com sobreposição e geração de embeddings vetoriais.
- [ ] Armazenamento dos vetores no ChromaDB com persistência em disco.
- [ ] Módulo `rag_engine.py` com busca semântica por similaridade de cosseno retornando os top-k trechos mais relevantes.

##### Tarefas Técnicas (Child Tasks)
* **Task 4.1:** [TASK-07] Curar e formatar os documentos de conhecimento veterinário e adestramento. *(Activity: Requirements, Est: 2.5h)*
  * *Descrição:* Estruturar arquivos Markdown contendo guias de comandos, nutrição e primeiros socorros.
* **Task 4.2:** [TASK-08] Desenvolver o módulo de ingestão e busca semântica no ChromaDB. *(Activity: Development, Est: 3.5h)*
  * *Descrição:* Escrever pipeline de indexação vetorial e função de consulta semântica integrada ao fluxo de inferência.

---

### 🏆 [FEATURE 03] Aplicação Backend Python (FastAPI) & Orquestração de IA
* **Work Item Type:** `Feature`
* **Parent:** `[EPIC] Sprint 3 - Disruptive Architectures: Aplicação Python com IA Generativa, RAG e Integração Frontend`
* **Title:** `[FEATURE 03] Aplicação Backend Python (FastAPI) & Orquestração de IA`
* **Tags:** `Sprint3, DisruptiveArchitectures, FastAPI, Python, REST, LLM, Pydantic`
* **Start Date:** `2026-09-01`
* **Target Date:** `2026-09-03`
* **Priority:** `1 - Critical`
* **Effort (Story Points):** `3`
* **Description:** Construção da API REST em FastAPI com rotas de chat, planos de treino, triagem de sintomas e diagramação arquitetural do ecossistema.

#### 🔹 [PBI-05] Desenvolvimento da API REST FastAPI com Endpoints de Chat, Triagem e Treino
* **Work Item Type:** `Product Backlog Item`
* **Parent Feature:** `[FEATURE 03] Aplicação Backend Python (FastAPI) & Orquestração de IA`
* **State:** `Approved`
* **Priority:** `1 - Critical`
* **Effort (Story Points):** `2`
* **Tags:** `Sprint3, DisruptiveArchitectures, FastAPI, Python, REST, LLM, Pydantic`

##### Descrição (História de Usuário)
> **Como** Desenvolvedor Backend de IA,  
> **Eu quero** implementar a API REST em FastAPI com rotas completas de chat conversacional, recomendação de treino e triagem clínica,  
> **Para que** o frontend e outros serviços da aplicação consumam o assistente inteligente de forma segura e padronizada.

##### Critérios de Aceite (Acceptance Criteria / Definition of Done)
- [ ] Endpoints implementados e documentados no Swagger UI (`/docs`):
  - `POST /api/v1/ai/chat`: Chat interativo recebendo `pet_id`, histórico de mensagens e pergunta do usuário; busca dados do pet no banco + RAG e responde estruturadamente.
  - `POST /api/v1/ai/training/plan`: Gera plano de treino personalizado baseado na espécie/raça/energia do pet e retorna passos práticos e pontuação XP.
  - `POST /api/v1/ai/health/insights`: Avalia o histórico de peso e vacinas do banco e retorna diagnósticos preventivos.
  - `POST /api/v1/ai/triage`: Analisa queixas de saúde, classifica a urgência (Verde/Amarelo/Vermelho) e fornece instruções de pronto-socorro.
- [ ] Validação rigorosa dos payloads de entrada e saída com schemas Pydantic V2.
- [ ] Middleware de CORS habilitado para comunicação com a aplicação Frontend (Mobile e Web).

##### Tarefas Técnicas (Child Tasks)
* **Task 5.1:** [TASK-09] Estruturar o projeto FastAPI com routers, middlewares e injeção de dependência. *(Activity: Development, Est: 2.0h)*
  * *Descrição:* Configurar `main.py`, roteadores modulares, variáveis de ambiente `.env` e tratamento de erros.
* **Task 5.2:** [TASK-10] Implementar a orquestração do LLM + RAG + Dados do Banco em `ai_service.py`. *(Activity: Development, Est: 3.0h)*
  * *Descrição:* Integrar chamadas da SDK do Gemini/OpenAI unindo contexto do banco, busca vetorial e formatação JSON.
* **Task 5.3:** [TASK-11] Criar schemas Pydantic e testes de integração das rotas. *(Activity: Testing, Est: 2.0h)*
  * *Descrição:* Escrever modelos de request/response e testes automatizados com `pytest` e `httpx`.

---

#### 🔹 [PBI-06] Elaboração do Diagrama Arquitetural de Fluxo de Dados e Integração Ponta a Ponta
* **Work Item Type:** `Product Backlog Item`
* **Parent Feature:** `[FEATURE 03] Aplicação Backend Python (FastAPI) & Orquestração de IA`
* **State:** `Approved`
* **Priority:** `1 - Critical`
* **Effort (Story Points):** `1`
* **Tags:** `Sprint3, DisruptiveArchitectures, Architecture, Diagram, DataFlow`

##### Descrição (História de Usuário)
> **Como** Arquiteto de Software,  
> **Eu quero** criar e documentar o diagrama de arquitetura do ecossistema de IA e fluxo de dados ponta a ponta,  
> **Para que** a banca compreenda a integração técnica entre o Frontend, a Aplicação Python, o Banco de Dados e os componentes de IA.

##### Critérios de Aceite (Acceptance Criteria / Definition of Done)
- [ ] Diagrama elaborado em alta resolução destacando: Frontend, Backend Python, Banco de Dados Relacional e Camada de IA.
- [ ] Fluxo numerado sequencial detalhando a requisição desde o clique na tela até a exibição da resposta.
- [ ] Inclusão do diagrama no `README.md` e na pasta `docs/`.

##### Tarefas Técnicas (Child Tasks)
* **Task 6.1:** [TASK-12] Desenvolver o diagrama visual com blocos padronizados e setas numeradas. *(Activity: Design, Est: 2.5h)*
  * *Descrição:* Elaborar diagrama em ferramenta visual (Draw.io / Visual Paradigm) exportando PNG em alta resolução.
* **Task 6.2:** [TASK-13] Redigir a documentação descritiva do fluxo de dados. *(Activity: Documentation, Est: 1.5h)*
  * *Descrição:* Descrever cada etapa do ciclo de vida da mensagem e estratégias de fallback.

---

### 🏆 [FEATURE 04] Integração Frontend: Página Dedicada da IA & Gamificação do Pet
* **Work Item Type:** `Feature`
* **Parent:** `[EPIC] Sprint 3 - Disruptive Architectures: Aplicação Python com IA Generativa, RAG e Integração Frontend`
* **Title:** `[FEATURE 04] Integração Frontend: Página Dedicada da IA & Gamificação do Pet`
* **Tags:** `Sprint3, DisruptiveArchitectures, Frontend, ReactNative, Gamification, AIChatScreen`
* **Start Date:** `2026-09-03`
* **Target Date:** `2026-09-04`
* **Priority:** `1 - Critical`
* **Effort (Story Points):** `3`
* **Description:** Desenvolvimento da tela dedicada de IA no frontend com interface de chat, seleção do pet, gamificação com XP e botão de emergência 24h.

#### 🔹 [PBI-07] Desenvolvimento da Página Dedicada da IA no Frontend (Chat, Chips & Cards)
* **Work Item Type:** `Product Backlog Item`
* **Parent Feature:** `[FEATURE 04] Integração Frontend: Página Dedicada da IA & Gamificação do Pet`
* **State:** `Approved`
* **Priority:** `1 - Critical`
* **Effort (Story Points):** `2`
* **Tags:** `Sprint3, DisruptiveArchitectures, Frontend, ReactNative, UI-UX, AIChatScreen`

##### Descrição (História de Usuário)
> **Como** tutor de pet,  
> **Eu quero** acessar uma página dedicada ao Assistente de IA no aplicativo mobile/web com interface de chat, seleção do pet e sugestões rápidas,  
> **Para que** eu possa tirar dúvidas de adestramento, saúde e alimentação de forma rápida, visual e contextualizada com o meu animal.

##### Critérios de Aceite (Acceptance Criteria / Definition of Done)
- [ ] Criação da tela dedicada `AiAssistantScreen` integrada à navegação principal do app.
- [ ] Componente de seleção do Pet ativo carregando o perfil correspondente.
- [ ] Interface de chat moderna com balões diferenciados, typing indicator e histórico.
- [ ] Barra de sugestões rápidas (Quick Action Chips): "Plano de Treino", "Alimentos Permitidos", "Checar Peso", "Sintomas de Emergência".
- [ ] Cards visuais de resposta e conexão HTTP real com a API Python.

##### Tarefas Técnicas (Child Tasks)
* **Task 7.1:** [TASK-14] Construir a interface visual da tela dedicada de IA com chat e componentes de UI. *(Activity: Design, Est: 3.0h)*
  * *Descrição:* Implementar layout responsivo, balões de conversa, scroll automático e barra de chips de atalho.
* **Task 7.2:** [TASK-15] Integrar a tela com a API Python e gerenciar o estado da conversa. *(Activity: Development, Est: 3.0h)*
  * *Descrição:* Criar hook de integração HTTP consumindo a rota `/api/v1/ai/chat` com tratamento de loading e erros.

---

#### 🔹 [PBI-08] Módulo de Treinamento com Gamificação do Pet e Triagem de Emergência 24h
* **Work Item Type:** `Product Backlog Item`
* **Parent Feature:** `[FEATURE 04] Integração Frontend: Página Dedicada da IA & Gamificação do Pet`
* **State:** `Approved`
* **Priority:** `2 - High`
* **Effort (Story Points):** `1`
* **Tags:** `Sprint3, DisruptiveArchitectures, Gamification, PetTraining, Triage24h`

##### Descrição (História de Usuário)
> **Como** tutor de pet,  
> **Eu quero** que o assistente gere treinos gamificados que concedam pontos ao meu pet e identifique sinais de emergência direcionando para clínicas 24h,  
> **Para que** meu pet se desenvolva de forma saudável e eu tenha suporte imediato em situações críticas.

##### Critérios de Aceite (Acceptance Criteria / Definition of Done)
- [ ] Sistema de gamificação: pontos de experiência (XP) atribuídos **ao perfil do pet** no banco de dados após a conclusão de exercícios de adestramento.
- [ ] Níveis de progressão canina/felina ("Filhote Curioso" ➔ "Pet Aprendiz" ➔ "Mestre dos Comandos").
- [ ] Módulo de Triagem Clínica com classificação visual de risco (Verde, Amarelo, Vermelho).
- [ ] Botão de rota e discagem rápida para pronto-socorro 24h em emergências.

##### Tarefas Técnicas (Child Tasks)
* **Task 8.1:** [TASK-16] Implementar a lógica de cálculo e persistência de XP do pet por treino concluído. *(Activity: Development, Est: 2.5h)*
  * *Descrição:* Criar rotinas para atualizar o score do pet e desbloquear novos níveis de treino.
* **Task 8.2:** [TASK-17] Construir o componente visual de triagem de emergência com botão 24h. *(Activity: Design, Est: 2.5h)*
  * *Descrição:* Desenvolver card de alerta com ação para discador telefônico ou mapa de clínicas 24h.

---

### 🏆 [FEATURE 05] Repositório Técnico, Documentação README e Vídeo Pitch Oficial
* **Work Item Type:** `Feature`
* **Parent:** `[EPIC] Sprint 3 - Disruptive Architectures: Aplicação Python com IA Generativa, RAG e Integração Frontend`
* **Title:** `[FEATURE 05] Repositório Técnico, Documentação README e Vídeo Pitch Oficial`
* **Tags:** `Sprint3, DisruptiveArchitectures, Documentation, README, VideoPitch, YouTube`
* **Start Date:** `2026-09-04`
* **Target Date:** `2026-09-05`
* **Priority:** `1 - Critical`
* **Effort (Story Points):** `2`
* **Description:** Estruturação do repositório no GitHub com README.md completo e gravação do vídeo pitch de 5 minutos demonstrando o funcionamento integrado.

#### 🔹 [PBI-09] Estruturação do Repositório GitHub e README.md Completo com Instruções
* **Work Item Type:** `Product Backlog Item`
* **Parent Feature:** `[FEATURE 05] Repositório Técnico, Documentação README e Vídeo Pitch Oficial`
* **State:** `Approved`
* **Priority:** `1 - Critical`
* **Effort (Story Points):** `1`
* **Tags:** `Sprint3, DisruptiveArchitectures, Documentation, GitHub, README`

##### Descrição (História de Usuário)
> **Como** Desenvolvedor e Integrante do Grupo,  
> **Eu quero** estruturar o repositório GitHub da aplicação Python com README.md técnico, instruções de setup e exemplos de uso,  
> **Para que** o professor avaliador consiga clonar, executar a API e validar o funcionamento da IA com facilidade.

##### Critérios de Aceite (Acceptance Criteria / Definition of Done)
- [ ] Organização das pastas do projeto (`src/`, `data/`, `docs/`).
- [ ] `README.md` contendo:
  - Identificação completa dos integrantes em ordem alfabética.
  - Descrição do problema e justificativa técnica da IA Generativa + RAG.
  - Diagrama de arquitetura e fluxo de integração.
  - Passo a passo de instalação e execução (`uvicorn src.main:app --reload`).
  - Exemplos de requisições cURL/JSON para todos os endpoints.
  - Link do vídeo no YouTube (Não Listado).

##### Tarefas Técnicas (Child Tasks)
* **Task 9.1:** [TASK-18] Configurar estrutura de pastas, `.gitignore` e `requirements.txt`. *(Activity: Development, Est: 1.5h)*
  * *Descrição:* Padronizar arquivos de configuração do ambiente Python e `.env.example`.
* **Task 9.2:** [TASK-19] Redigir o README.md técnico completo com guia de execução e exemplos. *(Activity: Documentation, Est: 1.5h)*
  * *Descrição:* Elaborar documentação técnica com tabelas de rotas e exemplos de payload.

---

#### 🔹 [PBI-10] Roteiro, Demonstração Funcional e Vídeo Pitch de 5 Minutos (YouTube)
* **Work Item Type:** `Product Backlog Item`
* **Parent Feature:** `[FEATURE 05] Repositório Técnico, Documentação README e Vídeo Pitch Oficial`
* **State:** `Approved`
* **Priority:** `1 - Critical`
* **Effort (Story Points):** `1`
* **Tags:** `Sprint3, DisruptiveArchitectures, VideoPitch, YouTube, Demonstration`

##### Descrição (História de Usuário)
> **Como** equipe do projeto Challenge Clyvo,  
> **Eu quero** gravar e publicar um vídeo pitch narrado de até 5 minutos no YouTube apresentando a proposta da solução, a integração com o banco de dados e a demonstração funcional na tela dedicada do app,  
> **Para que** a banca avalie a clareza didática, a maturidade técnica e o valor prático da inteligência artificial entregue.

##### Critérios de Aceite (Acceptance Criteria / Definition of Done)
- [ ] Roteiro estruturado cobrindo até 5 minutos (problema, arquitetura, demo funcional integrada, benefícios e conclusão).
- [ ] Gravação em alta definição (1080p/720p) com áudio claro narrado pelos integrantes.
- [ ] Demonstração do frontend React Native consumindo a API Python e dados do banco.
- [ ] Link do YouTube Não Listado adicionado no README.

##### Tarefas Técnicas (Child Tasks)
* **Task 10.1:** [TASK-20] Elaborar roteiro e preparar ambiente para gravação com dados reais de teste. *(Activity: Documentation, Est: 2.5h)*
  * *Descrição:* Criar script de apresentação e configurar massa de dados de pets no banco.
* **Task 10.2:** [TASK-21] Gravar, revisar e publicar o vídeo pitch no YouTube. *(Activity: Documentation, Est: 3.5h)*
  * *Descrição:* Gravar apresentação em equipe, validar limite de 5 minutos e anexar link no README.

---

## 👥 5. Integrantes do Grupo e Responsabilidades (Ordem Alfabética Estrita)

| Integrante | RM | Turma | Responsabilidade Principal na Sprint 3 |
| :--- | :---: | :---: | :--- |
| **Enzo Okuizumi** | **561432** | 2TDSPG | Mobile Development (React Native), Integração TanStack Query & Coordenação Geral |
| **Gustavo Okada** | **563428** | 2TDSPG | Java Advanced (Spring Security JWT, Flyway e SOLID) & .NET Observabilidade |
| **Lucas Barros Gouveia** | **566422** | 2TDSPG | Database Advanced (PL/SQL, Funções, Procedures e Triggers DML) |
| **Luna de Carvalho Guimarães** | **562290** | 2TDSPG | Disruptive Architectures (FastAPI, IA Generativa, RAG e Chat) & Compliance |
| **Milton Marcelino** | **564836** | 2TDSPG | DevOps Tools & Cloud Computing (Azure CLI, ACR, ACI e Containers) |
