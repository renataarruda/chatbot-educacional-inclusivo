import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

CHAVE_API_GOOGLE = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=CHAVE_API_GOOGLE)
MODELO_ESCOLHIDO = "gemini-3-flash-preview"
MODO_DEBUG = True

prompt_sistema = """Você é um assistente educacional especializado em educação inclusiva e superdotação.

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
- Se a pergunta for de um pai ou mãe, utilize linguagem simples e acolhedora. Utilize emojis nas respostas.
- Se a pergunta for de um professor, ofereça sugestões pedagógicas práticas.
- Se a pergunta for de um gestor, foque em estratégias institucionais ou organizacionais.

Sempre que apropriado, sugira que a pessoa procure profissionais especializados ou apoio pedagógico.

Seu papel é oferecer orientação inicial, esclarecer dúvidas e ajudar o usuário a entender melhor a situação apresentada."""

# configuracao_modelo = {
#     "temperature" : 2.0,
#     "top_p": 0.9,
#     "top_k": 64,
#     "max_output_tokens": 8192,
#     "response_mime_type": "text/plain"
# }

llm = genai.GenerativeModel(
    model_name=MODELO_ESCOLHIDO,
    system_instruction=prompt_sistema,
    # generation_config=configuracao_modelo
)

def gerar_resposta(pergunta):
    if MODO_DEBUG:
        print("Modo debug ativado")
        if "superdotado" in pergunta.lower():
            return "Mock: Alunos superdotados se beneficiam de atividades abertas e investigativas."

        if "inclusão" in pergunta.lower():
            return "Mock: A inclusão escolar envolve adaptar práticas pedagógicas para atender diferentes necessidades."

        return "Mock: resposta genérica do assistente educacional."
    
    resposta = llm.generate_content(pergunta)
    return resposta.text

print("Enviando pergunta para o modelo...")

pergunta = "Como adaptar atividades para um aluno superdotado?"

resposta = gerar_resposta(pergunta)

print("Resposta recebida!")
print(f"A resposta gerada para a pergunta é: {resposta}")