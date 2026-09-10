# 🎬 Roteiro Oficial do Vídeo Pitch (5 Minutos) — Guardian AI (PetGuardian / Clyvo Vet)

> **Disciplina:** Disruptive Architectures: IoT, IoB & Generative IA (FIAP — 2TDSPG)  
> **Challenge:** Clyvo Vet 2026 — 2º Semestre (Sprint 3)  
> **Apresentador Único:** **Enzo Okuizumi (RM 561432 — Turma 2TDSPG)**  
> **Duração Alvo:** 04:30 a 05:00 (Teto Máximo: 5 minutos)  
> **Modo de Publicação:** YouTube (Não Listado / Unlisted)  
> **Arquivo Demonstrado:** [`challenge-petguardian.ipynb`](./challenge-petguardian.ipynb)  
> **Microserviço Complementar:** [`deploy_guardianai_render/api.py`](./deploy_guardianai_render/api.py)  

---

## 👤 Identificação do Apresentador & Projeto

| Apresentador | RM | Turma | Papel no Pitch / Arquitetura |
| :--- | :---: | :---: | :--- |
| **Enzo Okuizumi** | **561432** | 2TDSPG | Apresentador Único, Arquitetura de IA, Tool Calling & Pydantic |

---

## 🎯 As 4 Seções Oficiais do Pitch (Edital do Challenge)

A apresentação está dividida em **4 seções equilibradas de aproximadamente 1 minuto e 15 segundos**, com falas diretas e sem enrolação:

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

## 🎬 Roteiro Resumido Seção a Seção (Teleprompter de Enzo Okuizumi)

---

### 🟢 SEÇÃO 1: Proposta da Solução & Problema de Negócio
- **Tempo:** `00:00` a `01:15` (75 segundos)
- **O que mostrar na tela:**
  - Repositório GitHub aberto no topo com seu nome, RM 561432 e título da solução.
  - Webcam de Enzo no canto ou em tela cheia com postura confiante.

#### 🎙️ Fala de Enzo (Resumida & Direta):
> *"Olá, professores da FIAP! Eu sou o Enzo Okuizumi, da turma 2TDSPG, RM 561432.*
>
> *Hoje apresento a **Guardian AI**, assistente de triagem preventiva e orientação pet integrada à plataforma **Clyvo Vet** para o Challenge 2026.*
>
> *O problema que atacamos é a insegurança e o pânico dos tutores diante de sintomas inesperados ou dúvidas alimentares do pet. Sem orientação especializada, eles recorrem à internet e caem em dois riscos gravíssimos:*
>
> *1. **Automedicação caseira fatal**: administrar medicamentos humanos como o Paracetamol — que é mortal para gatos —, ou tentar induzir vômito caseiro com água oxigenada e sal.*  
> *2. **Atraso no socorro**: perda da janela crítica de atendimento em intoxicações agudas por chocolate ou uvas.*
>
> *A **Guardian AI** resolve essa dor atuando como um copiloto inteligente: acolhe o tutor com empatia, orienta com embasamento científico determinístico e gera uma triagem estruturada para a equipe veterinária."*

---

### 🔵 SEÇÃO 2: O Papel da IA no Sistema & Abordagem Técnica Adotada
- **Tempo:** `01:15` a `02:30` (75 segundos)
- **O que mostrar na tela:**
  - Tabela comparativa do `README.md` (Seção 2).
  - Destaque no cursor para as tecnologias: **Gemini 3.5 Flash Lite**, **SDK oficial google-genai**, **Tool Calling** e **Pydantic**.

#### 🎙️ Fala de Enzo (Resumida & Direta):
> *"Na saúde animal, **uma alucinação da IA pode custar uma vida**. Por isso, descartei três abordagens tradicionais:*
>
> *• **Chatbots de regras rígidas**: não compreendem a linguagem natural e emocional do tutor.*  
> *• **Modelos preditivos tabulares**: apenas classificam dados, sem capacidade de acolher ou dialogar.*  
> *• **LLM generativo puro sem ferramentas**: risco inaceitável de alucinar dosagens e tolerâncias toxicológicas.*
>
> *A minha escolha técnica foi a **Abordagem Híbrida**: utilizo o **Gemini 3.5 Flash Lite** através da biblioteca oficial `google-genai` para compreensão contextual e raciocínio clínico, integrado a **Tool Calling determinístico em Python** para consultas toxicológicas de ground-truth absoluto, **System Instructions com guardrails inegociáveis** e extração estruturada de dados via schemas **Pydantic**.*
>
> *O papel da IA é personalizar a rotina preventiva por porte e idade, priorizar a gravidade clínica e bloquear categoricamente condutas perigosas."*

---

### 🟣 SEÇÃO 3: Os Benefícios para o Tutor, para a Clínica e para o Pet
- **Tempo:** `02:30` a `03:45` (75 segundos)
- **O que mostrar na tela:**
  - Diagrama dos **Três Eixos de Valor** (Tutor, Clínica Clyvo, Pet) na Seção 1 do `README.md`.
  - Tabela dos **6 grupos de dados do pet** na Seção 3 do README.

#### 🎙️ Fala de Enzo (Resumida & Direta):
> *"Essa arquitetura gera impacto direto nos três eixos da solução:*
>
> *• **Para o Tutor**: resposta imediata e clara no momento da dúvida, eliminando o pânico e o risco de receitas caseiras. O tutor ainda recebe o relatório `ResumoTriagem` em mãos, chegando mais seguro na consulta.*  
> *• **Para a Clínica Clyvo**: recebe previamente a anamnese em JSON validada por schema Pydantic, com gravidade já classificada entre baixa, média, alta ou emergência. Isso otimiza o fluxo de triagem na recepção e garante prioridade máxima para casos cirúrgicos ou intoxicações.*  
> *• **Para o Pet**: preservação da vida pelo socorro ágil em emergências toxicológicas, proteção contra intoxicações por fármacos humanos e longevidade através de prevenção contínua adaptada a porte e idade."*

---

### 🟠 SEÇÃO 4: Arquitetura de Funcionamento & Demonstração Prática no Colab
- **Tempo:** `03:45` a `05:00` (75 segundos)
- **O que mostrar na tela:**
  - Diagrama de arquitetura do README (Mobile/Colab ➔ Interactions API ➔ Dispatcher Python ➔ Pydantic).
  - Transição para o **Google Colab** com o notebook já executado:
    - Rolar até a **Simulação 1** (Chocolate amargo no Thor, chamada de tool e JSON de emergência).
    - Rolar até a **Simulação 2** (Golden Luna sênior, prevenção de torção gástrica e petiscos seguros).
    - Rolar até a **Simulação 3** (Recusa anti-pretexto a código Python e alerta letal de Paracetamol para gatos).

#### 🎙️ Fala de Enzo (Resumida & Direta):
> *"A arquitetura opera sob o padrão **100% Stateless**: o app mobile ou o notebook envia o contexto do pet para a **Interactions API do Gemini**, preservando a memória via `previous_interaction_id`.*
>
> *Quando qualquer alimento ou sintoma é citado, a IA emite uma `function_call`. O meu **Dispatcher em Python** executa a função determinística localmente e devolve o resultado para validação com Pydantic.*
>
> *Aqui no Google Colab vemos as 3 simulações na prática:*
>
> *• **Simulação 1 (Emergência)**: o cão Thor comeu chocolate. A tool detecta risco máximo, a IA proíbe expressamente água oxigenada ou sal e gera o `ResumoTriagem` de emergência.*  
> *• **Simulação 2 (Prevenção)**: a Golden Luna sênior aciona orientações determinísticas contra torção gástrica, displasia e valida a cenoura como petisco seguro.*  
> *• **Simulação 3 (Guardrails)**: o tutor pede código em Python e Paracetamol para gato febril. A IA aplica a **regra anti-pretexto**, recusa a programação e alerta que o **Paracetamol causa colapso por meta-hemoglobinemia e óbito em felinos**.*
>
> *Com isso, cobrimos com rigor 100% dos requisitos da disciplina Disruptive Architectures da FIAP. Muito obrigado!"*

---

## 📋 Quadro Resumo de Controle (Teleprompter)

| Seção | Tema Principal (Edital) | Minutagem | Palavras | Ritmo de Fala |
| :---: | :--- | :---: | :---: | :---: |
| **Seção 1** | **Proposta da Solução & Problema de Negócio** | `00:00 - 01:15` | ~115 palavras | Natural e acolhedor |
| **Seção 2** | **O Papel da IA no Sistema & Abordagem Técnica** | `01:15 - 02:30` | ~115 palavras | Técnico e assertivo |
| **Seção 3** | **Benefícios para o Tutor, Clínica e Pet** | `02:30 - 03:45` | ~110 palavras | Focado em valor |
| **Seção 4** | **Arquitetura & Demonstração Prática (Colab)** | `03:45 - 05:00` | ~130 palavras | Dinâmico e conclusivo |
| **TOTAL** | **Pitch Completo Guardian AI** | **04:30 a 05:00** | **~470 palavras** | **Ritmo perfeito (100 palavras/min)** |

---

## 💡 Dicas de Gravação para Enzo

1. **Ritmo Confortável:** Com ~470 palavras no total, você fala com calma em torno de 100 palavras por minuto, sem precisar correr ou ficar sem ar.
2. **Células Executadas no Colab:** Mantenha o notebook no Colab já com os outputs abertos na tela, rolando o mouse diretamente para os logs nas simulações 1, 2 e 3.
3. **Cronômetro:** Troque de seção a cada 1 minuto e 10 a 15 segundos para fechar o vídeo com segurança entre 04:30 e 04:55.
