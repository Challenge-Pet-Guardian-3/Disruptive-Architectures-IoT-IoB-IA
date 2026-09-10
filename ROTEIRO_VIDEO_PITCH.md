# 🎬 Roteiro Oficial do Vídeo Pitch (5 Minutos) — Guardian AI (PetGuardian / Clyvo Vet)

> **Disciplina:** Disruptive Architectures: IoT, IoB & Generative IA (FIAP — 2TDSPG)  
> **Challenge:** Clyvo Vet 2026 — 2º Semestre (Sprint 3)  
> **Apresentador Único:** **Enzo Okuizumi (RM 561432 — Turma 2TDSPG)**  
> **Duração Total Alvo:** 04:45 a 05:00 (Teto Máximo: 5 minutos)  
> **Modo de Publicação Obrigatório:** YouTube (Não Listado / Unlisted)  
> **Arquivo Executável Demonstrado:** [`challenge-petguardian.ipynb`](./challenge-petguardian.ipynb)  
> **Microserviço Complementar:** [`deploy_guardianai_render/api.py`](./deploy_guardianai_render/api.py)  

---

## 👤 Identificação do Apresentador & Projeto

| Apresentador | RM | Turma | Papel / Responsabilidade Técnica |
| :--- | :---: | :---: | :--- |
| **Enzo Okuizumi** | **561432** | 2TDSPG | Apresentador do Pitch, Arquitetura Técnica de IA, Tool Calling & Pydantic |

> *Projeto desenvolvido para a disciplina Disruptive Architectures da FIAP (Turma 2TDSPG), integrado ao ecossistema Clyvo Vet / PetGuardian.*

---

## 🎯 As 4 Seções Oficiais do Pitch (Edital do Challenge)

Conforme os requisitos formais de entrega da disciplina, a apresentação está estruturada em **4 seções equilibradas de aproximadamente 1 minuto e 15 segundos cada**:

```text
  00:00                01:15                02:30                03:45             05:00
    ┌────────────────────┬────────────────────┬────────────────────┬───────────────────┐
    │     SEÇÃO 1        │     SEÇÃO 2        │     SEÇÃO 3        │     SEÇÃO 4       │
    │  Proposta da       │   O Papel da IA    │  Benefícios para   │  Arquitetura de   │
    │  Solução &         │   no Sistema &     │  Tutor, Clínica    │  Funcionamento &  │
    │  Problema de       │   Abordagem        │  e Pet             │  Demonstração     │
    │  Negócio           │   Técnica          │                    │  Prática (Colab)  │
    └────────────────────┴────────────────────┴────────────────────┴───────────────────┘
          (~1m15s)             (~1m15s)             (~1m15s)            (~1m15s)
```

---

## 🎬 Roteiro Detalhado Seção a Seção (Fala de Enzo Okuizumi)

---

### 🟢 SEÇÃO 1: Proposta da Solução & Problema de Negócio
- **Tempo:** `00:00` a `01:15` (1 min e 15 seg)
- **O que mostrar na tela:**
  1. Tela inicial com o topo do repositório GitHub ou slide de abertura contendo:
     - **Enzo Okuizumi — RM 561432 (Turma 2TDSPG)**.
     - Título: **Guardian AI — Assistente de Triagem Clínica Preventiva e Orientação Pet (Clyvo Vet)**.
  2. Webcam de Enzo visível, com postura firme, dinâmica e segura.
- **Foco do Conteúdo:** Identificação individual, contextualização da dor na jornada contínua do pet e a proposta central da Guardian AI.

#### 🎙️ Fala de Enzo (00:00 - 01:15)
> *"Olá, professores e membros da banca avaliadora da FIAP! Eu sou o Enzo Okuizumi, aluno da turma 2TDSPG, RM 561432.*
>
> *Hoje apresento a **Guardian AI**, a solução de Inteligência Artificial integrada à plataforma **Clyvo Vet** para o nosso Challenge 2026.*
>
> *O problema que resolvo com esse projeto é um dos maiores desafios da jornada contínua de cuidado animal: a insegurança e o pânico de tutores diante de sinais clínicos imprevistos ou dúvidas alimentares do dia a dia. Ao recorrerem a buscas desordenadas na internet, tutores caem em dois extremos perigosos:*
>
> *O primeiro é a **automedicação caseira fatal**, como a administração de Paracetamol — que é mortal para felinos —, anti-inflamatórios humanos que causam úlceras e falência renal em cães, ou a tentativa de forçar vômito com água oxigenada e sal.*
>
> *O segundo é a **demora crítica para buscar atendimento em emergências toxicológicas reais**, como a ingestão de chocolate ou uvas, perdendo a janela de ouro do socorro médico.*
>
> *A proposta da **Guardian AI** é ser o copiloto inteligente de saúde preventiva do ecossistema Clyvo: uma IA que oferece acolhimento imediato, orientação segura ancorada em bases científicas e triagem clínica estruturada para o médico-veterinário presencial."*

---

### 🔵 SEÇÃO 2: O Papel da IA no Sistema & Abordagem Técnica Adotada
- **Tempo:** `01:15` a `02:30` (1 min e 15 seg)
- **O que mostrar na tela:**
  1. Tabela comparativa do `README.md` (Seção 2), destacando o porquê do descarte de chatbots de regras, modelos preditivos tabulares e LLMs puros.
  2. Destaque para a stack técnica: **Gemini 3.5 Flash Lite**, **SDK oficial google-genai**, **Tool Calling Determinístico** e **Pydantic**.
- **Foco do Conteúdo:** Justificar a escolha da arquitetura híbrida contra alternativas e detalhar o papel ativo da IA na personalização, priorização de risco e apoio à decisão.

#### 🎙️ Fala de Enzo (01:15 - 02:30)
> *"Ao projetar o papel da Inteligência Artificial no sistema, parti de um princípio inegociável: **na medicina veterinária, uma alucinação pode ser fatal**. Por isso, analisei e descartei três abordagens tradicionais:*
>
> *Primeiro: **chatbots de regras rígidas**, que são incapazes de compreender a linguagem coloquial, ansiosa e contextual do tutor. Segundo: **modelos de Machine Learning preditivos tabulares**, que classificam dados, mas não conseguem dialogar, acolher nem gerar orientações explicativas. E terceiro: um **LLM generativo puro sem grounding**, pois modelos de linguagem isolados alucinam dosagens, tolerâncias químicas e ignoram toxicidades graves.*
>
> *Diante disso, a minha escolha técnica foi a **Abordagem Híbrida**: uni o modelo **Gemini 3.5 Flash Lite** — consumido pela biblioteca oficial `google-genai` — para o processamento de linguagem natural e raciocínio clínico, combinado com **Tool Calling determinístico em Python** para consultas toxicológicas de ground-truth absoluto, **System Instructions especializadas com guardrails éticos e farmacológicos** e extração estruturada de dados via schemas **Pydantic**.*
>
> *O papel da IA aqui não é prescrever nem substituir o veterinário, mas sim atuar na personalização contínua por porte e idade, priorização imediata da gravidade clínica e blindagem ativa contra qualquer conduta que coloque o pet em perigo."*

---

### 🟣 SEÇÃO 3: Os Benefícios para o Tutor, para a Clínica e para o Pet
- **Tempo:** `02:30` a `03:45` (1 min e 15 seg)
- **O que mostrar na tela:**
  1. O diagrama dos **Três Eixos de Valor** (Tutor, Clínica Clyvo, Pet) presente na Seção 1 do `README.md`.
  2. A tabela dos **6 grupos de dados do pet** (Perfil biológico, Histórico clínico, Vacinas, Consultas, Medicamentos e Comportamento) na Seção 3 do README.
- **Foco do Conteúdo:** Demonstrar com clareza o impacto de negócio e o valor tangível gerado nos três vértices da solução.

#### 🎙️ Fala de Enzo (02:30 - 03:45)
> *"Essa abordagem gera valor direto nos três pilares fundamentais do ecossistema Clyvo:*
>
> *Para o **Tutor**, o benefício é o acolhimento imediato com linguagem clara e empática no momento da incerteza, eliminando o pânico e as receitas perigosas da internet. Além disso, o tutor recebe o relatório estruturado da triagem em mãos, sabendo exatamente o que relatar na consulta presencial.*
>
> *Para a **Clínica Veterinária Clyvo**, o ganho operacional é extraordinário: a IA entrega uma pré-anamnese estruturada via JSON validado por schema Pydantic, com a gravidade já classificada entre baixa, média, alta ou emergência. Isso reduz drasticamente o tempo improdutivo de triagem na recepção, filtra dúvidas corriqueiras de manejo e garante que os casos cirúrgicos ou de emergência cheguem prioritariamente à mesa do cirurgião.*
>
> *E para o **Animal (o Pet)**, o benefício é a preservação da sua vida e integridade física. O sistema atua como um escudo protetor contra automedicação tóxica, garante socorro veloz em envenenamentos e promove longevidade por meio de rotinas de saúde preventiva desenhadas sob medida para o seu porte, idade e predisposições de raça."*

---

### 🟠 SEÇÃO 4: Arquitetura de Funcionamento & Demonstração Prática no Colab
- **Tempo:** `03:45` a `05:00` (1 min e 15 seg)
- **O que mostrar na tela:**
  1. Transição rápida para o **Diagrama de Arquitetura de Fluxo** (Mobile/Colab ➔ FastAPI Stateless ➔ Interactions API ➔ Dispatcher Local Python ➔ Extrator Pydantic).
  2. Transição para o **Google Colab** ([`challenge-petguardian.ipynb`](./challenge-petguardian.ipynb)), demonstrando em tempo real:
     - **Simulação 1:** Ingestão de chocolate amargo pelo cão Thor, log da tool `verificar_alimento_toxico('chocolate')`, veto categórico a água oxigenada/sal e JSON Pydantic gerado com `gravidade: "emergencia"`.
     - **Simulação 2 & 3:** Cuidados preventivos da Golden Luna sênior (`consultar_cuidados_porte_idade`) e o teste de guardrail com recusa anti-pretexto a código Python e alerta mortal ao Paracetamol em felinos.
  3. Volta para a câmera com encerramento.
- **Foco do Conteúdo:** Comprovação técnica da integração arquitetural, exibição das tools e encerramento cravado em 5 minutos.

#### 🎙️ Fala de Enzo (03:45 - 05:00)
> *"Para finalizar, apresento a arquitetura de funcionamento e a demonstração prática.*
>
> *O fluxo opera sob o padrão **100% Stateless**: o aplicativo mobile ou o notebook autônomo envia o payload com o contexto do pet para a **Interactions API do Gemini**, mantendo a memória conversacional através do `previous_interaction_id`.*
>
> *Quando qualquer alimento ou necessidade preventiva é mencionada, o modelo emite uma `function_call`. O meu **Dispatcher em Python** executa a consulta determinística e devolve o `function_result`, finalizando com o extrator estruturado Pydantic.*
>
> *Aqui no Google Colab, vemos a **Simulação 1**: o Labrador Thor ingeriu chocolate meio amargo. O log mostra a chamada da ferramenta `verificar_alimento_toxico`. A IA proíbe expressamente água oxigenada ou sal, direciona ao hospital 24 horas e gera o objeto `ResumoTriagem` com gravidade **emergência**.*
>
> *Na **Simulação 2**, a Golden Luna sênior aciona `consultar_cuidados_porte_idade`, orientando sobre prevenção de torção gástrica, displasia e petiscos seguros com cenoura.*
>
> *E na **Simulação 3**, testamos a segurança máxima: o usuário tentou burlar a IA pedindo código em Python e dosagem de Paracetamol para um gato com febre. A Guardian AI aplica a **regra anti-pretexto**, recusa a programação e emite o alerta vital de que o **Paracetamol causa colapso por meta-hemoglobinemia e óbito em felinos**.*
>
> *Todo o código, testes com assert e documentação estão disponíveis no nosso GitHub. Muito obrigado a todos!"*

---

## 📋 Quadro de Controle de Tempo para Gravação (Teleprompter)

| Seção | Tema Principal | Início | Fim | Duração |
| :---: | :--- | :---: | :---: | :---: |
| **Seção 1** | **Proposta da Solução & Problema de Negócio** | `00:00` | `01:15` | **75 seg** |
| **Seção 2** | **O Papel da IA no Sistema & Abordagem Técnica** | `01:15` | `02:30` | **75 seg** |
| **Seção 3** | **Benefícios para o Tutor, Clínica e Pet** | `02:30` | `03:45` | **75 seg** |
| **Seção 4** | **Arquitetura de Funcionamento & Demonstração Prática** | `03:45` | `05:00` | **75 seg** |
| **TOTAL** | **Pitch Completo Guardian AI** | `00:00` | `05:00` | **300 seg (5 min)** |

---

## 💡 Dicas de Gravação para Enzo Okuizumi

1. **Abas Pré-carregadas:** Deixe o Colab com o notebook `challenge-petguardian.ipynb` **já rodado** (células com saídas visíveis), permitindo que você role a tela diretamente para os logs sem depender da velocidade da internet ao vivo.
2. **Postura & Voz:** Fale com ritmo seguro e articulado; cada seção tem em média 180 a 200 palavras, o que dá uma cadência de leitura confortável de 140 a 150 palavras por minuto.
3. **Cronômetro:** Deixe o cronômetro do celular ligado na mesa ao lado da tela para virar de seção a cada 1m15s.
