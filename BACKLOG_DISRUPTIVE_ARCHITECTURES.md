# 📋 Backlog Master Azure Boards — Sprint 3: Disruptive Architectures (IoT, IoB & IA)

> **Projeto Integrado:** PetGuardian / Clyvo Care (Challenge FIAP 2026 - 2º Ano ADS / 2TDSPG)  
> **Disciplina:** Disruptive Architectures: IoT, IoB & Generative IA (FIAP — 2TDSPG)  
> **Professor:** Arnaldo Jr  
> **Epic Principal:** `[EPIC] Sprint 3 - Disruptive Architectures: Assistente Virtual de Triagem e Cuidado Preventivo Pet (Guardian AI) com Google GenAI e Validação Pydantic`  
> **Start Date:** `2026-08-30`  
> **Target Date:** `2026-09-05`  
> **Arquivo Executável Central:** [`challenge-petguardian.ipynb`](file:///c:/Users/Enzo/new_backup/FIAP/_Projetos/Challenge%20Clyvo%203/Disruptive-Architectures-IoT-IoB-IA/challenge-petguardian.ipynb)  
> **Padrão:** Azure Boards (Scrum Process: Epic ➔ Feature ➔ PBI ➔ Task)  
> **Diretrizes Estratégicas:** Aplicação autônoma em Jupyter Notebook executável no Google Colab, orquestração via SDK oficial `google-genai` (Gemini 2.5 Flash), Tool Calling determinístico, blindagem estrita de guardrails éticos/farmacológicos, extração estruturada Pydantic (`ResumoTriagem`) e integração com o ecossistema Mobile.

---

## 👥 Integrantes do Grupo (Ordem Alfabética Estrita)

| Nome Completo | RM | Turma | Papel / Foco Técnico | GitHub |
| :--- | :---: | :---: | :--- | :--- |
| **Enzo Okuizumi** | **561432** | 2TDSPG | Arquitetura de IA, Tool Calling, Pydantic e Coordenação Geral | [EnzoOkuizumiFiap](https://github.com/EnzoOkuizumiFiap) |
| **Gustavo Okada** | **563428** | 2TDSPG | Java Advanced (Spring Security, Flyway e SOLID) & .NET | [Gdev3356](https://github.com/Gdev3356) |
| **Lucas Barros Gouveia** | **566422** | 2TDSPG | Database Advanced (Oracle PL/SQL, Procedures e Triggers) | [LuzBGouveia](https://github.com/LuzBGouveia) |
| **Luna de Carvalho Guimarães** | **562290** | 2TDSPG | Disruptive Architectures (Engenharia de Prompts e Guardrails) | [lunaguima](https://github.com/lunaguima) |
| **Milton Marcelino** | **564836** | 2TDSPG | DevOps Tools & Cloud Computing (Pipelines, Containers e Git) | [MiltonMarcelino](https://github.com/MiltonMarcelino) |

---

## 🎯 1. Matriz de Requisitos & Critérios de Avaliação Oficiais (Slides 17 a 19)

| Critério Avaliativo | Pontuação | Requisitos Obrigatórios da Banca |
| :--- | :---: | :--- |
| **Aplicação Técnica de Conceitos de IA** | **60 pts** | • Definição clara do problema de negócio e jornada contínua do pet.<br>• Escolha e justificativa técnica da abordagem de IA Generativa (`google-genai` SDK + `gemini-2.5-flash`).<br>• Implementação de **duas ferramentas determinísticas** via Tool Calling (Toxicologia e Cuidados por Porte/Idade).<br>• **Guardrails inegociáveis**: Bloqueio de off-topic anti-pretexto, proibição de receitas caseiras e veto total a medicamentos humanos (Paracetamol letal para felinos).<br>• Saída estruturada tipada com **Pydantic** (`ResumoTriagem`).<br>• Execução de **3 simulações obrigatórias** (Emergência, Prevenção, Guardrails). |
| **Clareza e Didática da Apresentação em Vídeo** | **20 pts** | • Gravação de **Vídeo Pitch de até 5 minutos**.<br>• Publicado no YouTube em modo **Não Listado**.<br>• Demonstração ao vivo da execução no Colab, chamadas de ferramenta e geração do Resumo de Triagem. |
| **Organização do Repositório & Documentação Técnica** | **20 pts** | • Repositório no GitHub organizado com notebook `.ipynb` limpo, testado e com outputs visíveis.<br>• **README.md completo** com tabela de integrantes, problema de negócio, arquitetura de fluxo, justificativa e guia de execução.<br>• Diagrama arquitetural ilustrando a orquestração entre Tutor ➔ LLM ➔ Dispatcher ➔ Pydantic. |

---

## 🌳 2. Estrutura Hierárquica no Azure Boards

```text
[EPIC] Sprint 3 - Disruptive Architectures: Assistente Virtual de Triagem e Cuidado Preventivo Pet (Guardian AI)
│
├── 🏆 [FEATURE 01] Modelagem do Problema, Engenharia de Prompts e Guardrails Éticos
│   ├── 📄 [PBI-01] Definição do Problema de Negócio e Jornada Contínua de Cuidado do Pet com IA (1 pt)
│   │   ├── 🔹 Task 1.1: Documentar proposta de valor e jornada contínua do tutor e da clínica (1.5h)
│   │   └── 🔹 Task 1.2: Mapear cenários de intervenção proativa e riscos clínicos críticos (1.5h)
│   └── 📄 [PBI-02] System Instruction Especializada e Guardrails Clínicos Inegociáveis (1 pt)
│       ├── 🔹 Task 2.1: Construir System Instruction da "Guardian AI" com persona acolhedora (1.5h)
│       └── 🔹 Task 2.2: Implementar guardrails anti-pretexto e bloqueio farmacológico absoluto (1.5h)
│
├── 🏆 [FEATURE 02] Base de Conhecimento Determinística & Tool Calling (Function Calling)
│   ├── 📄 [PBI-03] Modelagem e Teste Unitário das Regras de Negócio em Python Puro (1 pt)
│   │   ├── 🔹 Task 3.1: Estruturar bases de toxicologia, alimentos permitidos e matriz por porte/idade (2.0h)
│   │   └── 🔹 Task 3.2: Implementar funções determinísticas com normalização e testes com assert (2.0h)
│   └── 📄 [PBI-04] Declaração de Schemas de Ferramentas e Dispatcher via SDK google-genai (2 pts)
│       ├── 🔹 Task 4.1: Mapear schemas JSON das tools para a Interactions API do Gemini (2.5h)
│       └── 🔹 Task 4.2: Construir dispatcher seguro de execução de ferramentas (2.5h)
│
├── 🏆 [FEATURE 03] Orquestração da Interactions API, Memória e Saída Estruturada Pydantic
│   ├── 📄 [PBI-05] Encadeamento de Diálogo Multi-turnos via Interactions API (1 pt)
│   │   ├── 🔹 Task 5.1: Configurar cliente GenAI seguro com Colab Secrets e fallback .env (1.5h)
│   │   └── 🔹 Task 5.2: Implementar loop conversacional multi-turnos com previous_interaction_id (2.5h)
│   └── 📄 [PBI-06] Schema e Validação Estruturada com Pydantic (ResumoTriagem) (2 pts)
│       ├── 🔹 Task 6.1: Criar classe Pydantic ResumoTriagem com tipagem estrita (1.5h)
│       └── 🔹 Task 6.2: Implementar extrator de resumo clínico estruturado para consultas (2.5h)
│
├── 🏆 [FEATURE 04] Bateria de Simulações Práticas Obrigatórias e Modo Interativo
│   ├── 📄 [PBI-07] Execução das 3 Simulações Clínicas Obrigatórias com Logs Detalhados (2 pts)
│   │   ├── 🔹 Task 7.1: Implementar Simulação 1 (Emergência Toxicológica por Chocolate) (2.0h)
│   │   ├── 🔹 Task 7.2: Implementar Simulação 2 (Cuidados Preventivos com Golden Sênior) (2.0h)
│   │   └── 🔹 Task 7.3: Implementar Simulação 3 (Guardrails Anti-Pretexto e Veto ao Paracetamol) (2.0h)
│   └── 📄 [PBI-08] Interface Interativa Conversacional em Tempo Real no Notebook (1 pt)
│       └── 🔹 Task 8.1: Construir loop interativo com input() e comando de saída elegante (2.0h)
│
└── 🏆 [FEATURE 05] Repositório Técnico, Documentação README e Vídeo Pitch Oficial
    ├── 📄 [PBI-09] Estruturação do Repositório GitHub e README.md Técnico Completo (1 pt)
    │   ├── 🔹 Task 9.1: Organizar repositório com notebook, .gitignore e AGENT.md (1.5h)
    │   └── 🔹 Task 9.2: Redigir README.md completo com diagrama de arquitetura e tabela de integrantes (2.0h)
    └── 📄 [PBI-10] Roteiro, Demonstração Funcional e Vídeo Pitch de 5 Minutos (YouTube) (1 pt)
        ├── 🔹 Task 10.1: Elaborar roteiro focado nos critérios da banca (problema, demo, guardrails) (2.0h)
        └── 🔹 Task 10.2: Gravar, revisar e publicar vídeo pitch no YouTube em modo Não Listado (3.5h)
```

---

## 📊 3. Tabela Resumo do Backlog

| Feature Pai | ID do PBI | Título do Item de Backlog (PBI) | Story Points | Prioridade | Horas Estimadas |
| :--- | :--- | :--- | :---: | :---: | :---: |
| **[FEATURE 01] Modelagem & Guardrails** | **PBI-01** | Definição do Problema de Negócio e Jornada do Pet com IA | 1 pt | 1 - Critical | 3.0h |
| | **PBI-02** | System Instruction Especializada e Guardrails Clínicos | 1 pt | 1 - Critical | 3.0h |
| **[FEATURE 02] Regras & Tool Calling** | **PBI-03** | Modelagem e Teste Unitário das Regras em Python Puro | 1 pt | 1 - Critical | 4.0h |
| | **PBI-04** | Declaração de Schemas e Dispatcher via SDK google-genai | 2 pts | 1 - Critical | 5.0h |
| **[FEATURE 03] Interactions & Pydantic** | **PBI-05** | Encadeamento Multi-turnos via Interactions API | 1 pt | 1 - Critical | 4.0h |
| | **PBI-06** | Schema e Validação Estruturada com Pydantic | 2 pts | 1 - Critical | 4.0h |
| **[FEATURE 04] Simulações & Chat** | **PBI-07** | Execução das 3 Simulações Clínicas Obrigatórias | 2 pts | 1 - Critical | 6.0h |
| | **PBI-08** | Interface Interativa Conversacional no Notebook | 1 pt | 2 - High | 2.0h |
| **[FEATURE 05] Docs & Vídeo Pitch** | **PBI-09** | README.md Técnico e Organização do Repositório GitHub | 1 pt | 1 - Critical | 3.5h |
| | **PBI-10** | Roteiro, Demonstração e Vídeo Pitch de 5 Minutos | 1 pt | 1 - Critical | 5.5h |
| **TOTAL CONSOLIDADO** | **5 Features** | **10 PBIs / 20 Child Tasks Técnicas** | **13 pts** | — | **40.0h** |

---

## 📦 4. Detalhamento dos Itens de Trabalho (Épico, Features, PBIs e Tasks)

---

### 🏛️ ÉPICO
* **Work Item Type:** `Epic`
* **Title:** `[EPIC] Sprint 3 - Disruptive Architectures: Assistente Virtual de Triagem e Cuidado Preventivo Pet (Guardian AI) com Google GenAI e Validação Pydantic`
* **Tags:** `Sprint3, DisruptiveArchitectures, GoogleGenAI, Gemini2.5Flash, ToolCalling, Pydantic, Guardrails, Colab, Jupyter`
* **Start Date:** `2026-08-30`
* **Target Date:** `2026-09-05`
* **Priority:** `1 - Critical`
* **Effort (Story Points):** `13`
* **Business Value:** `100`
* **Description:** Desenvolvimento de uma aplicação autônoma de IA Generativa consolidada em Jupyter Notebook ([`challenge-petguardian.ipynb`](file:///c:/Users/Enzo/new_backup/FIAP/_Projetos/Challenge%20Clyvo%203/Disruptive-Architectures-IoT-IoB-IA/challenge-petguardian.ipynb)) para triagem clínica preventiva e orientação personalizada pet, utilizando a biblioteca oficial `google-genai` (Gemini 2.5 Flash), Tool Calling determinístico, guardrails anti-pretexto e farmacológicos, e extração tipada com Pydantic (`ResumoTriagem`).

---

### 🏆 [FEATURE 01] Modelagem do Problema, Engenharia de Prompts e Guardrails Éticos
* **Work Item Type:** `Feature`
* **Parent:** `[EPIC] Sprint 3 - Disruptive Architectures`
* **Title:** `[FEATURE 01] Modelagem do Problema, Engenharia de Prompts e Guardrails Éticos`
* **Tags:** `Sprint3, DisruptiveArchitectures, PromptEngineering, BusinessProblem, Guardrails`
* **Start Date:** `2026-08-30`
* **Target Date:** `2026-08-31`
* **Priority:** `1 - Critical`
* **Effort (Story Points):** `2`
* **Description:** Definição do problema de negócio da jornada do tutor/clínica e elaboração de System Prompt especializado com blindagem inegociável contra off-topic e automedicação perigosa.

#### 🔹 [PBI-01] Definição do Problema de Negócio e Jornada Contínua de Cuidado do Pet com IA
* **Work Item Type:** `Product Backlog Item`
* **Parent Feature:** `[FEATURE 01]`
* **State:** `Approved`
* **Priority:** `1 - Critical`
* **Effort (Story Points):** `1`
* **Tags:** `Sprint3, DisruptiveArchitectures, BusinessProblem, PetCareJourney`

##### Descrição (História de Usuário)
> **Como** Product Owner e Especialista em Arquitetura Disruptiva,  
> **Eu quero** mapear as falhas críticas na rotina do tutor (automedicação humana letal, demora em identificar emergências e desinformação),  
> **Para que** a Guardian AI atue como copiloto seguro de suporte à decisão e triagem pré-clínica na plataforma Clyvo Care.

##### Critérios de Aceite (Definition of Done)
- [ ] Mapeamento claro das dores: automedicação com Paracetamol/anti-inflamatórios, receitas caseiras para induzir vômito e falta de prevenção por porte/idade.
- [ ] Definição do papel da IA como assistente preventiva que **nunca substitui** o médico-veterinário presencial.
- [ ] Documentação da proposta de valor no notebook e no README.md.

##### Tarefas Técnicas (Child Tasks)
* **Task 1.1:** [TASK-01] Documentar proposta de valor e jornada contínua do tutor e da clínica. *(Activity: Requirements, Est: 1.5h)*
* **Task 1.2:** [TASK-02] Mapear cenários de intervenção proativa e riscos clínicos críticos. *(Activity: Requirements, Est: 1.5h)*

---

#### 🔹 [PBI-02] System Instruction Especializada e Guardrails Clínicos Inegociáveis
* **Work Item Type:** `Product Backlog Item`
* **Parent Feature:** `[FEATURE 01]`
* **State:** `Approved`
* **Priority:** `1 - Critical`
* **Effort (Story Points):** `1`
* **Tags:** `Sprint3, DisruptiveArchitectures, SystemPrompt, Guardrails, Safety`

##### Descrição (História de Usuário)
> **Como** Engenheiro de Prompts e Especialista em Segurança de IA,  
> **Eu quero** criar uma System Instruction com regras estritas de conduta clínica e blindagem anti-pretexto,  
> **Para que** a IA recuse categoricamente solicitações desconexas (ex: código em Python) e bloqueie qualquer prescrição de medicamentos alopáticos humanos.

##### Critérios de Aceite (Definition of Done)
- [ ] Persona "Guardian AI" definida com tom acolhedor, empático e cientificamente rigoroso.
- [ ] **Blindagem Anti-Pretexto**: Recusa de off-topic mesmo quando o usuário usa o pet como pretexto (ex: "meu cachorro quer aprender Python").
- [ ] **Segurança Farmacológica**: Proibição estrita de receitar Paracetamol (alerta explícito de letalidade para gatos e hepatotoxicidade para cães), Dipirona e Ibuprofeno.
- [ ] **Proibição de Indução de Vômito Caseira**: Veto a água oxigenada ou sal, orientando socorro 24h imediato.

##### Tarefas Técnicas (Child Tasks)
* **Task 2.1:** [TASK-03] Construir System Instruction da "Guardian AI" com persona acolhedora. *(Activity: Design, Est: 1.5h)*
* **Task 2.2:** [TASK-04] Implementar guardrails anti-pretexto e bloqueio farmacológico absoluto. *(Activity: Development, Est: 1.5h)*

---

### 🏆 [FEATURE 02] Base de Conhecimento Determinística & Tool Calling (Function Calling)
* **Work Item Type:** `Feature`
* **Parent:** `[EPIC] Sprint 3 - Disruptive Architectures`
* **Title:** `[FEATURE 02] Base de Conhecimento Determinística & Tool Calling (Function Calling)`
* **Tags:** `Sprint3, DisruptiveArchitectures, ToolCalling, FunctionCalling, PythonPure`
* **Start Date:** `2026-08-31`
* **Target Date:** `2026-09-01`
* **Priority:** `1 - Critical`
* **Effort (Story Points):** `3`
* **Description:** Modelagem de dicionários de regras clínicas em memória e integração determinística com a LLM via Tool Calling do SDK `google-genai`.

#### 🔹 [PBI-03] Modelagem e Teste Unitário das Regras de Negócio em Python Puro
* **Work Item Type:** `Product Backlog Item`
* **Parent Feature:** `[FEATURE 02]`
* **State:** `Approved`
* **Priority:** `1 - Critical`
* **Effort (Story Points):** `1`
* **Tags:** `Sprint3, DisruptiveArchitectures, BusinessRules, Testing, PurePython`

##### Descrição (História de Usuário)
> **Como** Desenvolvedor Python,  
> **Eu quero** criar bases estruturadas de toxicologia, petiscos seguros e matriz de cuidados por porte/faixa etária,  
> **Para que** a aplicação execute consultas determinísticas sem alucinações e valide seu funcionamento via testes de asserção.

##### Critérios de Aceite (Definition of Done)
- [ ] Dicionário `BASE_ALIMENTOS_TOXICOS` com chocolate, uva/passa, cebola, alho, xilitol e macadâmia (com mecanismo, sintomas e conduta).
- [ ] Dicionário `BASE_ALIMENTOS_PERMITIDOS` com cenoura, maçã, abóbora, banana e melancia.
- [ ] Matriz `BASE_CUIDADOS_PORTE_IDADE` e `BASE_FAIXA_ETARIA` cobrindo pequenos, médios, grandes e filhotes, adultos, seniores.
- [ ] Funções `verificar_alimento_toxico` e `consultar_cuidados_porte_idade` validadas por bloco de `assert`.

##### Tarefas Técnicas (Child Tasks)
* **Task 3.1:** [TASK-05] Estruturar bases de toxicologia, alimentos permitidos e matriz por porte/idade. *(Activity: Development, Est: 2.0h)*
* **Task 3.2:** [TASK-06] Implementar funções determinísticas com normalização de texto e testes com assert. *(Activity: Testing, Est: 2.0h)*

---

#### 🔹 [PBI-04] Declaração de Schemas de Ferramentas e Dispatcher via SDK google-genai
* **Work Item Type:** `Product Backlog Item`
* **Parent Feature:** `[FEATURE 02]`
* **State:** `Approved`
* **Priority:** `1 - Critical`
* **Effort (Story Points):** `2`
* **Tags:** `Sprint3, DisruptiveArchitectures, GoogleGenAI, Tools, Dispatcher`

##### Descrição (História de Usuário)
> **Como** Engenheiro de IA,  
> **Eu quero** declarar os schemas de Function Calling e o dispatcher `executar_ferramenta`,  
> **Para que** o modelo Gemini decida autonomamente quando invocar as regras determinísticas e injetar os resultados no raciocínio.

##### Critérios de Aceite (Definition of Done)
- [ ] Declaração da lista `FERRAMENTAS` com schemas JSON válidos para `verificar_alimento_toxico` e `consultar_cuidados_porte_idade`.
- [ ] Implementação da função `executar_ferramenta(nome_funcao, argumentos)` com logs detalhados e tratamento de erros.

##### Tarefas Técnicas (Child Tasks)
* **Task 4.1:** [TASK-07] Mapear schemas JSON das tools para a Interactions API do Gemini. *(Activity: Development, Est: 2.5h)*
* **Task 4.2:** [TASK-08] Construir dispatcher seguro de execução de ferramentas com logging. *(Activity: Development, Est: 2.5h)*

---

### 🏆 [FEATURE 03] Orquestração da Interactions API, Memória e Saída Estruturada Pydantic
* **Work Item Type:** `Feature`
* **Parent:** `[EPIC] Sprint 3 - Disruptive Architectures`
* **Title:** `[FEATURE 03] Orquestração da Interactions API, Memória e Saída Estruturada Pydantic`
* **Tags:** `Sprint3, DisruptiveArchitectures, InteractionsAPI, MultiTurn, Pydantic`
* **Start Date:** `2026-09-01`
* **Target Date:** `2026-09-02`
* **Priority:** `1 - Critical`
* **Effort (Story Points):** `3`
* **Description:** Configuração do cliente `google-genai`, gerenciamento de histórico multi-turnos via `previous_interaction_id` e extração de schemas Pydantic tipados.

#### 🔹 [PBI-05] Encadeamento de Diálogo Multi-turnos via Interactions API
* **Work Item Type:** `Product Backlog Item`
* **Parent Feature:** `[FEATURE 03]`
* **State:** `Approved`
* **Priority:** `1 - Critical`
* **Effort (Story Points):** `1`
* **Tags:** `Sprint3, DisruptiveArchitectures, InteractionsAPI, Memory, Gemini2.5Flash`

##### Descrição (História de Usuário)
> **Como** Desenvolvedor de IA,  
> **Eu quero** configurar o cliente GenAI e a função `executar_rodada_chat`,  
> **Para que** o assistente mantenha a memória dos turnos anteriores através do `previous_interaction_id` da Interactions API.

##### Critérios de Aceite (Definition of Done)
- [ ] Inicialização segura do cliente `genai.Client` com suporte a Colab Secrets (`userdata`) e `.env`.
- [ ] Loop de resolução de tool calls (receber chamada do modelo, executar função localmente e devolver o resultado).
- [ ] Retorno da resposta textual, novo `interaction_id` e lista de ferramentas executadas.

##### Tarefas Técnicas (Child Tasks)
* **Task 5.1:** [TASK-09] Configurar cliente GenAI seguro com Colab Secrets e fallback .env. *(Activity: Development, Est: 1.5h)*
* **Task 5.2:** [TASK-10] Implementar loop conversacional multi-turnos com previous_interaction_id. *(Activity: Development, Est: 2.5h)*

---

#### 🔹 [PBI-06] Schema e Validação Estruturada com Pydantic (ResumoTriagem)
* **Work Item Type:** `Product Backlog Item`
* **Parent Feature:** `[FEATURE 03]`
* **State:** `Approved`
* **Priority:** `1 - Critical`
* **Effort (Story Points):** `2`
* **Tags:** `Sprint3, DisruptiveArchitectures, Pydantic, StructuredOutput, ClinicalSummary`

##### Descrição (História de Usuário)
> **Como** Médico-Veterinário e Tutor da Clínica Clyvo,  
> **Eu quero** que a IA extraia da conversa um `ResumoTriagem` estruturado e validado por schema Pydantic,  
> **Para que** eu tenha um relatório padronizado contendo identificação do pet, gravidade, hipótese de risco e conduta recomendada.

##### Critérios de Aceite (Definition of Done)
- [ ] Modelo `ResumoTriagem` em Pydantic V2 com campos: `pet`, `relato_tutor`, `gravidade` (`Literal["baixa", "media", "alta", "emergencia"]`), `hipotese_risco` e `recomendacao_clinica`.
- [ ] Função `extrair_resumo_triagem(conversa_completa)` gerando JSON válido e instanciando o modelo com `model_validate_json()`.

##### Tarefas Técnicas (Child Tasks)
* **Task 6.1:** [TASK-11] Criar classe Pydantic ResumoTriagem com tipagem estrita e validação. *(Activity: Development, Est: 1.5h)*
* **Task 6.2:** [TASK-12] Implementar extrator de resumo clínico estruturado para consultas. *(Activity: Development, Est: 2.5h)*

---

### 🏆 [FEATURE 04] Bateria de Simulações Práticas Obrigatórias e Modo Interativo
* **Work Item Type:** `Feature`
* **Parent:** `[EPIC] Sprint 3 - Disruptive Architectures`
* **Title:** `[FEATURE 04] Bateria de Simulações Práticas Obrigatórias e Modo Interativo`
* **Tags:** `Sprint3, DisruptiveArchitectures, Simulations, ColabExecution, InteractiveChat`
* **Start Date:** `2026-09-02`
* **Target Date:** `2026-09-03`
* **Priority:** `1 - Critical`
* **Effort (Story Points):** `3`
* **Description:** Execução das 3 simulações de teste exigidas pelos critérios pedagógicos da disciplina, com logs detalhados e disponibilização de chat interativo.

#### 🔹 [PBI-07] Execução das 3 Simulações Clínicas Obrigatórias com Logs Detalhados
* **Work Item Type:** `Product Backlog Item`
* **Parent Feature:** `[FEATURE 04]`
* **State:** `Approved`
* **Priority:** `1 - Critical`
* **Effort (Story Points):** `2`
* **Tags:** `Sprint3, DisruptiveArchitectures, Simulations, GoldenCases, GuardrailTests`

##### Descrição (História de Usuário)
> **Como** Professor Avaliador da Disciplina,  
> **Eu quero** visualizar a execução documentada de 3 cenários clínicos completos (Emergência, Prevenção e Guardrail),  
> **Para que** eu comprove o correto acionamento das ferramentas, aderência ao System Prompt e geração do JSON Pydantic.

##### Critérios de Aceite (Definition of Done)
- [ ] **Simulação 1 (Emergência Toxicológica)**: Ingestão de chocolate amargo por cão ➔ Tool `verificar_alimento_toxico` acionada ➔ Veto a água oxigenada ➔ Resumo de Triagem de Emergência gerado.
- [ ] **Simulação 2 (Cuidados Preventivos)**: Golden Retriever sênior (Luna, 7 anos) ➔ Tool `consultar_cuidados_porte_idade` e `verificar_alimento_toxico(cenoura)` acionadas ➔ Orientações de DTG e articulações ➔ Resumo Pydantic preventivo gerado.
- [ ] **Simulação 3 (Guardrails & Farmacologia)**: Solicitação de código em Python + dose de Paracetamol para gato com febre ➔ Recusa cordial de off-topic ➔ Alerta de toxicidade letal do Paracetamol em felinos.

##### Tarefas Técnicas (Child Tasks)
* **Task 7.1:** [TASK-13] Implementar Simulação 1 (Emergência Toxicológica por Chocolate). *(Activity: Development, Est: 2.0h)*
* **Task 7.2:** [TASK-14] Implementar Simulação 2 (Cuidados Preventivos com Golden Sênior). *(Activity: Development, Est: 2.0h)*
* **Task 7.3:** [TASK-15] Implementar Simulação 3 (Guardrails Anti-Pretexto e Veto ao Paracetamol). *(Activity: Development, Est: 2.0h)*

---

#### 🔹 [PBI-08] Interface Interativa Conversacional em Tempo Real no Notebook
* **Work Item Type:** `Product Backlog Item`
* **Parent Feature:** `[FEATURE 04]`
* **State:** `Approved`
* **Priority:** `2 - High`
* **Effort (Story Points):** `1`
* **Tags:** `Sprint3, DisruptiveArchitectures, InteractiveChat, ColabLive`

##### Descrição (História de Usuário)
> **Como** Avaliador ou Tutor,  
> **Eu quero** conversar livremente com a Guardian AI em uma célula interativa via terminal/notebook,  
> **Para que** eu possa realizar testes customizados em tempo real e encerrar com comando `sair`.

##### Critérios de Aceite (Definition of Done)
- [ ] Loop `while True` com prompt `input("Tutor: ")`.
- [ ] Reconhecimento de comandos de saída (`sair`, `fim`, `exit`).
- [ ] Exibição de logs de tool calling quando ativados.

##### Tarefas Técnicas (Child Tasks)
* **Task 8.1:** [TASK-16] Construir loop interativo com input() e comando de saída elegante. *(Activity: Development, Est: 2.0h)*

---

### 🏆 [FEATURE 05] Repositório Técnico, Documentação README e Vídeo Pitch Oficial
* **Work Item Type:** `Feature`
* **Parent:** `[EPIC] Sprint 3 - Disruptive Architectures`
* **Title:** `[FEATURE 05] Repositório Técnico, Documentação README e Vídeo Pitch Oficial`
* **Tags:** `Sprint3, DisruptiveArchitectures, Documentation, README, VideoPitch, YouTube`
* **Start Date:** `2026-09-04`
* **Target Date:** `2026-09-05`
* **Priority:** `1 - Critical`
* **Effort (Story Points):** `2`
* **Description:** Estruturação do repositório no GitHub com README.md técnico completo, diagramação arquitetural e gravação do vídeo pitch de 5 minutos no YouTube.

#### 🔹 [PBI-09] Estruturação do Repositório GitHub e README.md Técnico Completo
* **Work Item Type:** `Product Backlog Item`
* **Parent Feature:** `[FEATURE 05]`
* **State:** `Approved`
* **Priority:** `1 - Critical`
* **Effort (Story Points):** `1`
* **Tags:** `Sprint3, DisruptiveArchitectures, Documentation, GitHub, README`

##### Descrição (História de Usuário)
> **Como** Integrante da Equipe e Desenvolvedor,  
> **Eu quero** formatar o repositório GitHub com documentação técnica de excelência,  
> **Para que** o professor consiga avaliar a maturidade arquitetural e executar o notebook no Colab com um clique.

##### Critérios de Aceite (Definition of Done)
- [ ] Tabela com os 5 integrantes em ordem alfabética estrita com RM, Turma e Links.
- [ ] Seções no `README.md`: Problema de Negócio, Justificativa Técnica, Diagrama de Arquitetura em ASCII/Mermaid, Guia de Execução no Google Colab e Tabela de Toxicologia.
- [ ] Arquivo `AGENT.md` detalhando decisões técnicas e `BACKLOG_DISRUPTIVE_ARCHITECTURES.md` com o padrão Azure Boards.

##### Tarefas Técnicas (Child Tasks)
* **Task 9.1:** [TASK-17] Organizar repositório com notebook, .gitignore e AGENT.md. *(Activity: Development, Est: 1.5h)*
* **Task 9.2:** [TASK-18] Redigir README.md completo com diagrama de arquitetura e tabela de integrantes. *(Activity: Documentation, Est: 2.0h)*

---

#### 🔹 [PBI-10] Roteiro, Demonstração Funcional e Vídeo Pitch de 5 Minutos (YouTube)
* **Work Item Type:** `Product Backlog Item`
* **Parent Feature:** `[FEATURE 05]`
* **State:** `Approved`
* **Priority:** `1 - Critical`
* **Effort (Story Points):** `1`
* **Tags:** `Sprint3, DisruptiveArchitectures, VideoPitch, YouTube, Demonstration`

##### Descrição (História de Usuário)
> **Como** Equipe do Challenge Clyvo,  
> **Eu quero** gravar e publicar um vídeo pitch narrado de até 5 minutos no YouTube (Não Listado),  
> **Para que** a banca comprove a didática da apresentação, a proposta de valor e a execução ao vivo das funcionalidades inteligentes.

##### Critérios de Aceite (Definition of Done)
- [ ] Roteiro estruturado respeitando o teto de 5 minutos (Abertura ➔ Problema & Proposta ➔ Arquitetura & Stack ➔ Demonstração ao Vivo no Colab ➔ Conclusão & Impacto).
- [ ] Demonstração prática do acionamento de tools, guardrail do Paracetamol e geração do objeto Pydantic.
- [ ] Vídeo publicado em 1080p/720p no YouTube em modo **Não Listado** com link inserido no `README.md`.

##### Tarefas Técnicas (Child Tasks)
* **Task 10.1:** [TASK-19] Elaborar roteiro focado nos critérios da banca (problema, demo, guardrails). *(Activity: Documentation, Est: 2.0h)*
* **Task 10.2:** [TASK-20] Gravar, revisar e publicar vídeo pitch no YouTube em modo Não Listado. *(Activity: Documentation, Est: 3.5h)*
