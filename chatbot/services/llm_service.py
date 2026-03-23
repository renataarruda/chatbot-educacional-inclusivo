import os
import time
import json
import google.generativeai as genai
from google.api_core.exceptions import ResourceExhausted, NotFound
from dotenv import load_dotenv

load_dotenv()

# ─── Configuração ────────────────────────────────────────────────
CHAVE_API_GOOGLE = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=CHAVE_API_GOOGLE)

MODELO_ESCOLHIDO = "gemini-3-flash-preview"
MODO_DEBUG = os.getenv("MODO_DEBUG", "false").lower() == "true"

# ─── Prompt do sistema ───────────────────────────────────────────
PROMPT_SISTEMA = """Você é um assistente educacional especializado em educação inclusiva e superdotação.

Seu objetivo é ajudar pais, professores e gestores escolares a compreender melhor questões relacionadas a altas habilidades, superdotação e inclusão educacional.

Regras de resposta:

1. Utilize linguagem clara e acessível.
2. Evite termos excessivamente técnicos.
3. Explique conceitos de forma educativa e acolhedora.
4. Sempre que possível, sugira próximos passos ou caminhos de orientação.
5. Não forneça diagnósticos clínicos ou pedagógicos.
6. Reforce que suas respostas são informativas e não substituem avaliação profissional.
7. Não responda perguntas sobre assuntos que não estejam relacionados à educação inclusiva, altas habilidades e superdotação.

Quando responder:
Sempre considere o perfil do usuário informado no início da pergunta.

- Se a pergunta for de um pai, mãe ou responsável, utilize linguagem simples e acolhedora. Utilize emojis nas respostas.
- Se a pergunta for de um professor, ofereça sugestões pedagógicas práticas.
- Se a pergunta for de um gestor, foque em estratégias institucionais ou organizacionais.
- Se a pergunta for de outro usuário, utilize linguagem simples e foque em respostas de conhecimento geral.

Adapte o tom conforme o sentimento detectado na mensagem:
- Se a mensagem transmitir ansiedade ou preocupação, seja especialmente acolhedor e tranquilizador.
- Se a mensagem for objetiva e direta, seja conciso e prático.
- Se a mensagem demonstrar frustração, valide o sentimento antes de responder.

Não repita respostas, seções e títulos.

Sempre que apropriado, sugira que a pessoa procure profissionais especializados ou apoio pedagógico.

Seu papel é oferecer orientação inicial, esclarecer dúvidas e ajudar o usuário a entender melhor a situação apresentada."""

# ─── Materiais recomendados ──────────────────────────────────────
MATERIAIS_RECOMENDADOS = {
    "superdotação": "📚 Saiba mais no portal do MEC: https://www.gov.br/mec/pt-br/pneei",
    "inclusão":     "📚 Referência sobre educação inclusiva — Instituto Rodrigo Mendes: https://institutorodrigomendes.org.br",
    "legislação":   "📚 Veja o que diz a lei — LDB, Capítulo V: https://www.planalto.gov.br/ccivil_03/leis/l9394.htm",
    "superdotado":  "📚 Guia para Superdotados no EduCAPES: https://educapes.capes.gov.br/",
    "diversidade":  "📚 Portal DIVERSA — gestão escolar inclusiva: https://diversa.org.br/",
}

# ─── Respostas mock para debug ───────────────────────────────────
RESPOSTAS_DEBUG = {
    "superdot": "**[DEBUG]** Alunos superdotados se beneficiam de atividades abertas e investigativas.\n\nAlguma outra dúvida?",
    "inclusão": "**[DEBUG]** A inclusão escolar envolve adaptar práticas pedagógicas para atender diferentes necessidades.\n\nAlguma outra dúvida?",
    "padrão":   "**[DEBUG]** Resposta genérica do assistente educacional.",
}

# ─── Perfis de usuário ───────────────────────────────────────────
PERFIS = {
    "pai":        "pai",
    "mae":        "mãe",
    "responsavel":"responsável familiar",
    "gestor":     "gestor(a) escolar",
    "professor":  "professor(a)",
    "outro":      "outro usuário",
}

# ─── Funções auxiliares ──────────────────────────────────────────
def sugestao_material_complementar(pergunta: str) -> str | None:
    """Retorna um link de material complementar com base em palavras-chave da pergunta."""
    p = pergunta.lower()
    if "superdot" in p:
        return MATERIAIS_RECOMENDADOS["superdotação"]
    if "inclusiv" in p or "inclusão" in p:
        return MATERIAIS_RECOMENDADOS["inclusão"]
    if " lei " in p or p.startswith("lei") or "legislação" in p:
        return MATERIAIS_RECOMENDADOS["legislação"]
    if "diversidade" in p:
        return MATERIAIS_RECOMENDADOS["diversidade"]
    return None


def analisar_sentimento(pergunta: str) -> str:
    """
    Análise heurística simples de sentimento.
    Retorna: 'ansioso', 'frustrado', 'neutro'
    """
    p = pergunta.lower()

    palavras_ansiedade = ["preocupado", "preocupada", "ansioso", "ansiosa", "medo",
                          "assustado", "não sei", "não consigo", "ajuda", "socorro",
                          "desesperado", "desesperada"]
    palavras_frustracao = ["cansado", "cansada", "frustrado", "frustrada", "irritado",
                           "irritada", "impossível", "não funciona", "ninguém ajuda",
                           "não adianta", "odeio"]

    if any(palavra in p for palavra in palavras_ansiedade):
        return "ansioso"
    if any(palavra in p for palavra in palavras_frustracao):
        return "frustrado"
    return "neutro"


def criar_modelo():
    """Instancia e retorna o modelo Gemini."""
    try:
        return genai.GenerativeModel(
            model_name=MODELO_ESCOLHIDO,
            system_instruction=PROMPT_SISTEMA,
        )
    except NotFound as e:
        print(f"[ERRO] Modelo não encontrado: {e}")
        return None


def gerar_resposta(pergunta: str, persona: str) -> str:
    """
    Gera a resposta do assistente.
    Em MODO_DEBUG retorna respostas simuladas sem chamar a API.
    """
    perfil = PERFIS.get(persona, "usuário")
    sentimento = analisar_sentimento(pergunta)

    # ── Modo debug ──────────────────────────────────────────────
    if MODO_DEBUG:
        p = pergunta.lower()
        if "superdot" in p:
            resposta = RESPOSTAS_DEBUG["superdot"]
        elif "inclusão" in p or "inclusiv" in p:
            resposta = RESPOSTAS_DEBUG["inclusão"]
        else:
            resposta = RESPOSTAS_DEBUG["padrão"]

        resposta += f"\n\n*Sentimento detectado: {sentimento} | Perfil: {perfil}*"

        material = sugestao_material_complementar(pergunta)
        if material:
            resposta += "\n\n" + material

        return resposta

    # ── Modo real ────────────────────────────────────────────────
    llm = criar_modelo()
    if not llm:
        return "Desculpe, ocorreu um erro ao conectar com o assistente. Tente novamente."

    try:
        pergunta_com_contexto = f"""Perfil do usuário: {perfil}
Sentimento detectado: {sentimento}

Pergunta do usuário:
{pergunta}"""

        resposta = llm.generate_content(pergunta_com_contexto).text
        time.sleep(1)

        material = sugestao_material_complementar(pergunta)
        if material:
            resposta += "\n\n" + material

        return resposta

    except ResourceExhausted:
        return "⚠️ Limite da API atingido. Aguarde alguns instantes e tente novamente."
    except Exception as e:
        print(f"[ERRO] {e}")
        return "Ocorreu um erro inesperado. Por favor, tente novamente."