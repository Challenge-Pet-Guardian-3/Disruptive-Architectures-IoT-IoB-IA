from typing import Optional, List
from app.models.schemas import PetContext

SYSTEM_INSTRUCTION_CLYVO_AI = """
Você é a "Guardian AI", uma inteligência artificial especializada em medicina veterinária preventiva, nutrição animal, adestramento positivo e bem-estar de animais de estimação (cães, gatos e pets domésticos) desenvolvida para a plataforma PetGuardian / Clyvo Care.

### 🛡️ GUARDRAILS E DIRETRIZES ÉTICAS CRÍTICAS (OBRIGATÓRIAS):
1. **FOCO ESTRITO EM CUIDADO ANIMAL (DOMÍNIO EXCLUSIVO):**
   - Você DEVE responder SOMENTE sobre cuidados com animais de estimação (saúde preventiva, alimentação, adestramento, vacinas, rotina, primeiros socorros e higiene).
   - Se o usuário fizer qualquer pergunta fora desse contexto (ex: programação, matemática, política, receitas para humanos, fofocas, finanças, piadas genéricas, tarefas acadêmicas alheias a pets), você DEVE recusar gentilmente com uma mensagem padrão como:
     "Sou a Guardian AI, dedicada exclusivamente à saúde, bem-estar e adestramento de animais de estimação. Como posso ajudar com os cuidados do seu pet hoje?"
   - Defina a categoria como "FORA_DE_ESCOPO" e urgência "BAIXA".

2. **SEGURANÇA CLÍNICA E PRESCRIÇÃO MÉDICA:**
   - NUNCA prescreva doses de medicamentos alopáticos humanos (Paracetamol, Dipirona, Ibuprofeno, etc.) ou antibióticos/anti-inflamatórios sem prescrição veterinária presencial.
   - Paracetamol é altamente letal para felinos e tóxico para caninos.
   - Sempre oriente a consulta presencial com um médico-veterinário para diagnósticos definitivos.

3. **DETECÇÃO DE EMERGÊNCIAS (NÍVEL VERMELHO / 24H):**
   - Se a pergunta relatar ingestão de chocolate amargo, uvas/uvas-passas, cebola/alho, venenos (chumbinho), plantas tóxicas (lírios para gatos), torção gástrica, sangramentos graves, convulsões prolongadas ou dispneia/asfixia:
     - Classifique a urgência como "EMERGENCIA".

     - Instrua com clareza a NÃO tentar receitas caseiras perigosas (como sal ou água oxigenada para induzir vômito) e ir imediatamente a uma clínica veterinária 24h.

4. **PERSONALIZAÇÃO PELO PERFIL DO PET:**
   - Quando dados do Pet forem fornecidos (nome, raça, porte, idade, castrado, histórico de saúde), cite o nome do animal, adapte o tom e leve em consideração suas características específicas (ex: cães idosos, raças braquicefálicas, predisposição a displasia em cães grandes, tártaro em pequenos).

5. **FORMATO DE RESPOSTA (JSON ESTRUTURADO):**
   - Você SEMPRE deve responder em formato JSON válido com as seguintes chaves:
   {
     "resposta": "Texto completo, acolhedor e formatado da sua resposta ao tutor.",
     "categoria": "SAUDE" | "NUTRICAO" | "COMPORTAMENTO" | "ROTINA" | "EMERGENCIA" | "GERAL" | "FORA_DE_ESCOPO",
     "urgencia": "BAIXA" | "MEDIA" | "ALTA" | "EMERGENCIA",
     "acoes_recomendadas": ["Ação prática 1", "Ação prática 2"]
   }
"""

def build_user_prompt_with_context(
    pergunta: str,
    pet_context: Optional[PetContext] = None,
    rag_chunks: Optional[List[str]] = None
) -> str:
    """Monta o prompt enriquecido com os dados do animal e os trechos recuperados pelo RAG."""
    
    pet_info_str = "Nenhum pet específico selecionado (orientação geral)."
    if pet_context:
        detalhes = []
        if pet_context.nome:
            detalhes.append(f"Nome: {pet_context.nome}")
        if pet_context.raca:
            detalhes.append(f"Raça: {pet_context.raca}")
        if pet_context.porte:
            detalhes.append(f"Porte: {pet_context.porte}")
        if pet_context.idade is not None:
            detalhes.append(f"Idade: {pet_context.idade} anos")
        if pet_context.sexo:
            detalhes.append(f"Sexo: {pet_context.sexo}")
        if pet_context.castrado is not None:
            detalhes.append(f"Castrado: {'Sim' if pet_context.castrado else 'Não'}")
        if pet_context.peso:
            detalhes.append(f"Peso atual: {pet_context.peso}")
        if pet_context.alergias:
            detalhes.append(f"Alergias conhecidas: {pet_context.alergias}")
        if pet_context.medicamentos:
            detalhes.append(f"Medicamentos em uso: {pet_context.medicamentos}")
        if pet_context.ultimaVacina:
            detalhes.append(f"Última Vacina: {pet_context.ultimaVacina}")
            
        pet_info_str = "\n".join([f"- {d}" for d in detalhes])

    rag_info_str = "Nenhum documento específico encontrado na base vetorial."
    if rag_chunks and len(rag_chunks) > 0:
        rag_info_str = "\n---\n".join(rag_chunks)

    return f"""
=== CONTEXTO DO ANIMAL ATIVO ===
{pet_info_str}

=== BASE DE CONHECIMENTO VETERINÁRIO (RAG CHROMA-DB) ===
{rag_info_str}

=== PERGUNTA DO TUTOR ===
"{pergunta}"

Por favor, responda exclusivamente em formato JSON conforme as instruções do sistema, aplicando os Guardrails de segurança, personalizando para o pet e gerando a resposta clínica e preventiva adequada.
"""

def build_insights_prompt(pet_context: PetContext) -> str:
    """Gera o prompt para o gerador de insights preventivos automáticos."""
    return f"""
Gere 3 recomendações preventivas de saúde, nutrição e bem-estar altamente personalizadas para o seguinte animal:
- Nome: {pet_context.nome}
- Raça: {pet_context.raca}
- Porte: {pet_context.porte}
- Idade: {pet_context.idade or 'Não informada'} anos
- Castrado: {'Sim' if pet_context.castrado else 'Não'}
- Peso: {pet_context.peso or 'Padrão'}
- Alergias: {pet_context.alergias or 'Nenhuma'}

Responda em formato JSON com a seguinte estrutura:
{{
  "pet_nome": "{pet_context.nome}",
  "insights": [
    {{
      "titulo": "Título curto e claro",
      "descricao": "Explicação e recomendação preventiva",
      "categoria": "saude" | "nutricao" | "comportamento" | "rotina",
      "urgencia": "baixa" | "media" | "alta"
    }}
  ]
}}
"""

def build_triage_prompt(sintomas: str, pet_context: Optional[PetContext] = None) -> str:
    """Gera o prompt para a triagem de sintomas de emergência."""
    nome = pet_context.nome if pet_context and pet_context.nome else "o pet"
    porte = pet_context.porte if pet_context and pet_context.porte else "não especificado"
    
    return f"""
Realize a triagem clínica dos seguintes sintomas relatados para {nome} (porte: {porte}):
"{sintomas}"

Responda em formato JSON válido:
{{
  "classificacao": "BAIXA" | "MEDIA" | "ALTA" | "EMERGENCIA",
  "nivel_cor": "VERDE" | "AMARELO" | "VERMELHO",
  "diagnostico_provavel_ou_orientacao": "Explicação clara do risco e prováveis causas sem prescrever remédios caseiros perigosos",
  "deve_buscar_emergencia_24h": boolean,
  "primeiros_socorros_seguros": ["passo 1 seguro", "passo 2 seguro"],
  "o_que_nao_fazer": ["proibição 1 (ex: não dar paracetamol)", "proibição 2"]
}}
"""

def build_training_prompt(comando: str, nivel: str, pet_context: Optional[PetContext] = None) -> str:
    """Gera o prompt para o plano de treino positivo gamificado."""
    nome = pet_context.nome if pet_context and pet_context.nome else "o cão"
    return f"""
Crie um plano prático de adestramento positivo e gamificado para ensinar o comando/hábito "{comando}" para {nome}, nível {nivel}.

Responda em JSON:
{{
  "titulo": "Título do Treino",
  "duracao_sessao_minutos": 5,
  "passos_praticos": ["Passo 1 detalhado", "Passo 2 com marcação 'Isso!'", "Passo 3 recompensa"],
  "dica_reforco_positivo": "Como recompensar sem punição",
  "pontos_xp_recompensa": 20
}}
"""
