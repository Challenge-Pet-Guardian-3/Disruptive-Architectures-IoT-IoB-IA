"""
Serviço Orquestrador do Chat Clínico PetGuardian
"""
from typing import Optional, List, Dict, Any
from src.core.config import MODEL_NAME
from src.schemas.chat import ChatRequest, ChatResponse
from src.services.knowledge_service import KnowledgeService
from src.services.gemini_service import GeminiService
from src.utils.text import limpar_texto_mobile, normalizar_texto
from src.utils.guardrails import detectar_pedido_programacao, sanitizar_resposta_anti_codigo

class ChatService:
    """
    Orquestra o pipeline de triagem e conversação:
    1. Guardrail farmacológico emergencial (Paracetamol em felinos)
    2. Guardrail toxicológico determinístico (Alimentos proibidos)
    3. Inferência generativa contextual (Gemini) com histórico deslizante
    4. Fallback semântico (FAQ cotidiana)
    5. Blindagem contra evasão de domínio (Prompt injection de código)
    6. Fallback clínico contextual por porte e idade
    """

    @classmethod
    def processar_chat(cls, request: ChatRequest) -> ChatResponse:
        pergunta_norm = normalizar_texto(request.pergunta)

        # 1. Guardrail de Segurança Farmacológica / Paracetamol em Gatos (apenas pergunta atual)
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
        dados_tox = KnowledgeService.verificar_alimento_toxico(request.pergunta)
        if dados_tox:
            chave = dados_tox["alimento"]
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

        # 3. Tentativa de Inferência via Gemini com Memória Multi-turnos
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

        eh_pedido_programacao = detectar_pedido_programacao(request.pergunta)
        prompt_atual = f"{contexto_pet_str}\n\nPergunta do Tutor: {request.pergunta}" if contexto_pet_str else request.pergunta

        resposta_ia = GeminiService.gerar_resposta(prompt_atual, request.historico)
        if resposta_ia:
            texto_sem_codigo = sanitizar_resposta_anti_codigo(resposta_ia, eh_pedido_programacao)
            texto_limpo = limpar_texto_mobile(texto_sem_codigo)
            return ChatResponse(
                resposta=texto_limpo,
                categoria="saude",
                urgencia="baixa",
                acoes_recomendadas=["Acompanhar o bem-estar", "Manter hidratação regular"],
                score_xp_sugerido=10,
                origem_resposta=f"Guardian AI ({MODEL_NAME})"
            )

        # 4. Fallback Semântico Inteligente para Perguntas Cotidianas
        dados_tema = KnowledgeService.consultar_faq_cotidiana(request.pergunta)
        if dados_tema:
            texto_base = dados_tema["resposta"]
            if eh_pedido_programacao:
                texto_base = sanitizar_resposta_anti_codigo(texto_base, True)
            return ChatResponse(
                resposta=limpar_texto_mobile(texto_base),
                categoria=dados_tema["categoria"],
                urgencia=dados_tema["urgencia"],
                acoes_recomendadas=["Manter rotina equilibrada", "Consultar veterinário em caso de dúvidas"],
                score_xp_sugerido=10,
                origem_resposta="Guardian AI (Base Semântica Especializada)"
            )

        # Se for puramente pergunta de programação fora de escopo sem tema pet correspondente
        if eh_pedido_programacao:
            return ChatResponse(
                resposta=limpar_texto_mobile(
                    "Como Guardian AI, sou dedicada exclusivamente à saúde, nutrição e bem-estar de cães e gatos. "
                    "Por isso, não forneço códigos, programação em Python ou instruções de desenvolvimento de software, "
                    "mesmo quando solicitados com o pet como pretexto!\n\n"
                    "Posso te ajudar com alguma orientação sobre alimentação, vacinas ou rotina de cuidados do seu pet?"
                ),
                categoria="saude",
                urgencia="baixa",
                acoes_recomendadas=["Dúvidas sobre nutrição animal", "Consultar rotina preventiva"],
                score_xp_sugerido=5,
                origem_resposta="Guardrail Anti-Pretexto e Blindagem de Domínio"
            )

        # 5. Fallback Contextual por Porte e Idade
        porte_req = request.petContext.porte if request.petContext and request.petContext.porte else "medio"
        idade_num = request.petContext.idade if request.petContext and request.petContext.idade is not None else 3
        faixa_calc = "senior" if idade_num >= 7 else ("filhote" if idade_num <= 1 else "adulto")
        dados_cuidado = KnowledgeService.consultar_cuidados_porte_idade(porte_req, faixa_calc)

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
