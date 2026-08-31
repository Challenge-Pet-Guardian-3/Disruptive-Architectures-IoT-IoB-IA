import re
from typing import Optional, List, NamedTuple
from app.models.schemas import (
    PetContext,
    ChatResponse,
    CategoryEnum,
    UrgencyEnum,
    InsightsResponse,
    PetInsight,
    TriageResponse,
    TrainingPlanResponse,
)

class PetMetadata(NamedTuple):
    nome: str
    porte: str
    idade: Optional[int]
    castrado: bool

class FallbackService:
    """
    Serviço de fallback com inteligência determinística e regras clínicas curadas.
    Segue os princípios SOLID (SRP e OCP) e DRY, com handlers dedicados por intenção.
    """

    # Padrões de Expressões Regulares compilados para performance
    OFF_TOPIC_REGEX = re.compile(
        r"\b(python|java|javascript|c\#|c\+\+|sql|react|html|css|programação|código|algoritmo|"
        r"matemática|derivada|integral|equação|fórmula|calcular|física|química|"
        r"política|eleição|presidente|senado|governo|partido|"
        r"bitcoin|cripto|ações|investimento|dólar|bolsa|"
        r"receita de bolo|cozinhar humano|filme|futebol|campeonato)\b",
        re.IGNORECASE
    )

    EMERGENCY_REGEX = re.compile(
        r"\b(chocolate|cacau|teobromina|uva|uvas|passas|cebola|alho|alho-poró|xilitol|chumbinho|veneno|inseticida|lírio|"
        r"convuls|sangr|atropel|desmai|inconsciente|afog|engasg|não respira|parada|língua roxa|língua azul|"
        r"torção|barriga inchada e dura|tentando vomitar sem sair nada)\b",
        re.IGNORECASE
    )

    BEHAVIOR_KEYWORDS = {"adestr", "trein", "senta", "fica", "morde", "morder", "latir", "xixi", "ansied", "sozinho", "xp", "ponto"}
    NUTRITION_KEYWORDS = {"racao", "ração", "comida", "aliment", "fruta", "petisco", "peso", "gordo", "magro", "fome"}
    HEALTH_KEYWORDS = {"vacin", "v8", "v10", "raiva", "vermif", "pulga", "carrapato", "castr", "dente", "tartaro"}

    @staticmethod
    def _extract_pet_metadata(pet_ctx: Optional[PetContext]) -> PetMetadata:
        """Helper DRY para extrair e normalizar metadados do animal."""
        return PetMetadata(
            nome=pet_ctx.nome.strip() if pet_ctx and pet_ctx.nome else "seu pet",
            porte=(pet_ctx.porte or "MEDIO").upper() if pet_ctx else "MEDIO",
            idade=pet_ctx.idade if pet_ctx and pet_ctx.idade is not None else None,
            castrado=bool(pet_ctx.castrado) if pet_ctx else False,
        )

    def process_chat(self, pergunta: str, pet_context: Optional[PetContext] = None) -> ChatResponse:
        """Processa a mensagem do usuário e seleciona o handler apropriado."""
        texto = pergunta.lower().strip()
        pet = self._extract_pet_metadata(pet_context)

        # 1. Guardrail de Domínio (Rejeição fora de escopo)
        if self.OFF_TOPIC_REGEX.search(texto):
            return self._handle_off_topic(pet)

        # 2. Guardrail de Emergência e Toxicologia
        if self.EMERGENCY_REGEX.search(texto):
            return self._handle_emergency(pet)

        # 3. Adestramento e Gamificação
        if any(keyword in texto for keyword in self.BEHAVIOR_KEYWORDS):
            return self._handle_behavior(pet)

        # 4. Nutrição e Alimentação
        if any(keyword in texto for keyword in self.NUTRITION_KEYWORDS):
            return self._handle_nutrition(pet)

        # 5. Vacinas e Saúde Preventiva
        if any(keyword in texto for keyword in self.HEALTH_KEYWORDS):
            return self._handle_health(pet)

        # 6. Fallback Preventivo Geral
        return self._handle_general(pet)

    def _handle_off_topic(self, pet: PetMetadata) -> ChatResponse:
        return ChatResponse(
            resposta=(
                f"Olá! Sou a Guardian AI, dedicada exclusivamente "
                f"à saúde preventiva, nutrição e adestramento de animais de estimação. "
                f"Não posso responder sobre outros temas, mas adoraria te ajudar a cuidar de {pet.nome}! 🐾"
            ),
            categoria=CategoryEnum.FORA_DE_ESCOPO,
            urgencia=UrgencyEnum.BAIXA,
            alerta_clinica_24h=False,
            acoes_recomendadas=[
                "Perguntar sobre nutrição e ração do pet",
                "Consultar dicas de adestramento e comandos",
                "Tirar dúvidas sobre vacinação e prevenção",
            ],
            score_xp_sugerido=0,
            origem_resposta="fallback_rules"
        )

    def _handle_emergency(self, pet: PetMetadata) -> ChatResponse:
        return ChatResponse(
            resposta=(
                f"⚠️ **ALERTA DE EMERGÊNCIA CLÍNICA PARA {pet.nome.upper()}!**\n\n"
                f"A situação relatada envolve alto risco de toxicidade ou risco iminente à vida. "
                f"Substâncias como chocolate (teobromina), uvas, cebola, xilitol e venenos causam falência orgânica rápida.\n\n"
                f"**Orientação Imediata:** Dirija-se urgentemente ao pronto-socorro veterinário 24h mais próximo. "
                f"Não induza vômito em casa com sal ou água oxigenada, pois pode causar perfurações gástricas graves."
            ),
            categoria=CategoryEnum.EMERGENCIA,
            urgencia=UrgencyEnum.EMERGENCIA,
            alerta_clinica_24h=True,
            acoes_recomendadas=[
                "Transportar o pet imediatamente a uma clínica veterinária 24h",
                "Levar a embalagem da substância ingerida para cálculo de dosagem tóxica",
                "Manter vias aéreas desobstruídas e o animal calmo no trajeto",
                "Não oferecer leite, azeite ou medicamentos caseiros"
            ],
            score_xp_sugerido=0,
            origem_resposta="fallback_rules"
        )

    def _handle_behavior(self, pet: PetMetadata) -> ChatResponse:
        return ChatResponse(
            resposta=(
                f"Para o adestramento de **{pet.nome}**, o método mais eficiente e seguro é o **Reforço Positivo**:\n\n"
                f"1. **Sessões Curtas:** Faça treinos de 3 a 5 minutos, 2x ao dia.\n"
                f"2. **Marcação Precisa:** No instante exato em que {pet.nome} acertar o comportamento, marque verbalmente com 'Isso!' e recompense imediatamente com petisco.\n"
                f"3. **Sem Punição:** Nunca repreenda fisicamente ou grite. Se o pet errar, apenas ignore e repita o estímulo com calma.\n"
                f"4. **Enriquecimento:** Brinquedos recheáveis congelados ajudam a combater o tédio e a ansiedade de separação."
            ),
            categoria=CategoryEnum.COMPORTAMENTO,
            urgencia=UrgencyEnum.BAIXA,
            alerta_clinica_24h=False,
            acoes_recomendadas=[
                f"Praticar o comando 'Senta' 5 vezes hoje com {pet.nome}",
                "Oferecer brinquedo interativo ao sair de casa",
                "Concluir uma lição na aba de Trilhas para somar +15 XP"
            ],
            score_xp_sugerido=15,
            origem_resposta="fallback_rules"
        )

    def _handle_nutrition(self, pet: PetMetadata) -> ChatResponse:
        refeicoes = "2 a 3 refeições diárias" if pet.porte in ["PEQUENO", "MEDIO"] else "2 refeições divididas (evita torção gástrica)"
        return ChatResponse(
            resposta=(
                f"A nutrição ideal de **{pet.nome}** (porte {pet.porte.lower()}): \n\n"
                f"- **Fracionamento:** Recomendamos {refeicoes} com ração Super Premium balanceada.\n"
                f"- **Petiscos Saudáveis Permitidos:** Cenoura crua ou cozida sem sal (ótima para dentes), maçã sem sementes e abóbora cozida.\n"
                f"- **Hidratação:** Disponibilize água fresca e limpa em múltiplos pontos da casa.\n"
                f"- **Atenção:** Nunca ofereça comida caseira com cebola, alho, gordura em excesso ou ossos cozidos."
            ),
            categoria=CategoryEnum.NUTRICAO,
            urgencia=UrgencyEnum.BAIXA,
            alerta_clinica_24h=False,
            acoes_recomendadas=[
                "Pesar a quantidade diária de ração na balança dosadora",
                "Oferecer cubos de cenoura como recompensa de baixo valor calórico",
                "Trocar a água do bebedouro duas vezes ao dia"
            ],
            score_xp_sugerido=10,
            origem_resposta="fallback_rules"
        )

    def _handle_health(self, pet: PetMetadata) -> ChatResponse:
        idade_info = f" ({pet.idade} anos)" if pet.idade is not None else ""
        return ChatResponse(
            resposta=(
                f"Para garantir a longevidade e proteção de **{pet.nome}**{idade_info}:\n\n"
                f"💉 **Esquema Vacinal:** As vacinas polivalente (V8/V10) e Antirrábica devem receber reforço anual obrigatório. Se houver passeios frequentes, a vacina contra Giárdia e Gripe Canina também é indicada.\n"
                f"🛡️ **Antiparasitários:** Mantenha vermífugo semestral e controle mensal de pulgas e carrapatos.\n"
                f"🦷 **Saúde Bucal:** Escovação 3x na semana previne cálculo tártaro e doenças renais/cardíacas secundárias."
            ),
            categoria=CategoryEnum.SAUDE,
            urgencia=UrgencyEnum.BAIXA,
            alerta_clinica_24h=False,
            acoes_recomendadas=[
                f"Conferir a carteirinha de vacinação de {pet.nome}",
                "Aplicar preventivo de pulgas e carrapatos em dia",
                "Agendar check-up preventivo semestral na Clyvo Care"
            ],
            score_xp_sugerido=10,
            origem_resposta="fallback_rules"
        )

    def _handle_general(self, pet: PetMetadata) -> ChatResponse:
        return ChatResponse(
            resposta=(
                f"Olá! Sou a Guardian AI. "
                f"Com base no perfil de **{pet.nome}** (porte {pet.porte.lower()}), estou aqui para fornecer orientações de "
                f"medicina preventiva, rotinas saudáveis, alimentação equilibrada e reforço positivo. "
                f"Em que posso orientar a rotina de {pet.nome} hoje?"
            ),
            categoria=CategoryEnum.GERAL,
            urgencia=UrgencyEnum.BAIXA,
            alerta_clinica_24h=False,
            acoes_recomendadas=[
                "Perguntar sobre cronograma de vacinas e vermifugação",
                "Consultar plano de treino positivo para comandos",
                "Verificar alimentos permitidos e proibidos"
            ],
            score_xp_sugerido=5,
            origem_resposta="fallback_rules"
        )

    def generate_insights(self, pet_ctx: PetContext) -> InsightsResponse:
        """Gera insights preventivos estruturados baseados no perfil do Pet."""
        pet = self._extract_pet_metadata(pet_ctx)
        idade = pet.idade or 3
        insights: List[PetInsight] = []

        # 1. Insight por Porte
        if pet.porte == "GRANDE":
            insights.append(PetInsight(
                titulo=f"Cuidado Articular Preventivo para {pet.nome}",
                descricao=f"Pets de grande porte como {pet.nome} necessitam de controle rigoroso de peso e passeios em piso macio para proteger as articulações.",
                categoria="saude",
                urgencia="media"
            ))
        elif pet.porte == "PEQUENO":
            insights.append(PetInsight(
                titulo=f"Prevenção de Tártaro e Higiene Bucal",
                descricao="Cães de porte pequeno acumulam placa bacteriana rapidamente. A escovação dentária 3x por semana previne periodontite.",
                categoria="saude",
                urgencia="baixa"
            ))
        else:
            insights.append(PetInsight(
                titulo="Estímulo Mental e Gasto de Energia",
                descricao=f"Garanta 45 minutos diários de caminhada e enriquecimento ambiental olfativo para {pet.nome}.",
                categoria="rotina",
                urgencia="baixa"
            ))

        # 2. Insight por Idade
        if idade >= 7:
            insights.append(PetInsight(
                titulo="Fase Sênior: Check-up Preventivo",
                descricao=f"{pet.nome} tem {idade} anos. Exames de sangue, função renal e ecocardiograma semestrais aumentam a longevidade.",
                categoria="saude",
                urgencia="alta"
            ))
        else:
            insights.append(PetInsight(
                titulo="Hidratação e Nutrição Balanceada",
                descricao="Mantenha água limpa e divida a porção diária de ração de alta qualidade para otimizar a absorção de nutrientes.",
                categoria="nutricao",
                urgencia="baixa"
            ))

        # 3. Insight por Condição de Castração
        if not pet.castrado:
            insights.append(PetInsight(
                titulo="Benefícios da Castração Preventiva",
                descricao="A castração reduz drasticamente tumores de mama e próstata, além de diminuir fugas e marcação de território.",
                categoria="saude",
                urgencia="media"
            ))
        else:
            insights.append(PetInsight(
                titulo="Controle de Peso Pós-Castração",
                descricao="Pets castrados apresentam metabolismo ligeiramente reduzido. Mantenha rotina ativa de exercícios.",
                categoria="nutricao",
                urgencia="baixa"
            ))

        return InsightsResponse(pet_nome=pet.nome, insights=insights)

    def process_triage(self, sintomas: str, pet_ctx: Optional[PetContext] = None) -> TriageResponse:
        """Realiza triagem clínica baseada em regras de gravidade médica."""
        texto = sintomas.lower()
        
        if self.EMERGENCY_REGEX.search(texto):
            return TriageResponse(
                classificacao=UrgencyEnum.EMERGENCIA,
                nivel_cor="VERMELHO",
                diagnostico_provavel_ou_orientacao="Risco iminente de intoxicação aguda ou falência sistêmica. Requer pronto-socorro veterinário 24h imediato.",
                deve_buscar_emergencia_24h=True,
                primeiros_socorros_seguros=[
                    "Manter vias respiratórias desobstruídas",
                    "Proteger o pet contra quedas e ruídos excessivos em caso de convulsão",
                    "Levar embalagem da substância ingerida à clínica"
                ],
                o_que_nao_fazer=[
                    "NÃO dar paracetamol, ibuprofeno ou remédios humanos",
                    "NÃO induzir vômito com sal, óleo ou água oxigenada"
                ]
            )

        if any(k in texto for k in ["vomito", "vômito", "diarreia", "mancando", "febre", "não come"]):
            return TriageResponse(
                classificacao=UrgencyEnum.ALTA,
                nivel_cor="AMARELO",
                diagnostico_provavel_ou_orientacao="Desconforto gástrico, dor osteomuscular ou infecção inicial. Recomenda-se consulta veterinária no mesmo dia.",
                deve_buscar_emergencia_24h=False,
                primeiros_socorros_seguros=[
                    "Oferecer água fresca em pequenos goles",
                    "Manter o animal em repouso em local fresco e acolhedor"
                ],
                o_que_nao_fazer=[
                    "NÃO forçar alimentação sólida durante episódios de vômito ativo",
                    "NÃO administrar antibióticos sem receita"
                ]
            )

        return TriageResponse(
            classificacao=UrgencyEnum.BAIXA,
            nivel_cor="VERDE",
            diagnostico_provavel_ou_orientacao="Sintomas leves de rotina ou comportamento. Monitorar evolução e agendar consulta preventiva.",
            deve_buscar_emergencia_24h=False,
            primeiros_socorros_seguros=[
                "Higienizar a área com soro fisiológico se for secreção leve",
                "Manter rotina normal e observar o apetite"
            ],
            o_que_nao_fazer=[
                "NÃO utilizar pomadas humanas sem autorização médica"
            ]
        )

    def generate_training_plan(self, comando: str, nivel: str, pet_ctx: Optional[PetContext] = None) -> TrainingPlanResponse:
        """Gera plano de reforço positivo gamificado."""
        pet = self._extract_pet_metadata(pet_ctx)
        return TrainingPlanResponse(
            titulo=f"Treino Positivo: {comando.title()} para {pet.nome}",
            duracao_sessao_minutos=5,
            passos_praticos=[
                "1. Fique em local calmo com petiscos de alto valor na mão fechada.",
                f"2. Conduza o petisco suavemente fazendo {pet.nome} seguir o movimento.",
                "3. No instante exato em que executar a ação: marque com a voz 'Isso!' e entregue a recompensa.",
                "4. Repita 5 vezes consecutivas e finalize com festa e carinho."
            ],
            dica_reforco_positivo="Termine sempre a sessão em um acerto para manter a motivação em alta.",
            pontos_xp_recompensa=20
        )

fallback_service = FallbackService()
