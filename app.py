from flask import Flask,render_template, request, Response
import google.generativeai as genai
from dotenv import load_dotenv
import os
import time
from time import sleep
from analisador_sentimentos import carrega, salva
from selecionar_persona import personas, selecionar_persona

load_dotenv()

CHAVE_API_GOOGLE = os.getenv("GEMINI_API_KEY")
MODELO_ESCOLHIDO = "gemini-3-flash-preview"   
genai.configure(api_key=CHAVE_API_GOOGLE)

app = Flask(__name__)
app.secret_key = 'chatbot'

contexto = carrega("dados/avaliacoes_chatbot.txt")

def bot(prompt):
    maximo_tentativas = 1
    repeticao = 0

    while True:
        try:
            personalidade = personas[selecionar_persona(prompt)]

            prompt_do_sistema = f"""Você é um assistente educacional especializado em educação inclusiva e superdotação.

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

            - Se a pergunta for de um pai ou mãe, utilize linguagem simples e acolhedora. Utilize emojis nas respostas.
            - Se a pergunta for de um professor, ofereça sugestões pedagógicas práticas.
            - Se a pergunta for de um gestor, foque em estratégias institucionais ou organizacionais.
            - Se a pergunta for de um outro usuário, utilize linguagem simples e foque em respostas de conhecimento geral.

            Não repita respostas, seções e títulos.

            Sempre que apropriado, sugira que a pessoa procure profissionais especializados ou apoio pedagógico.

            Seu papel é oferecer orientação inicial, esclarecer dúvidas e ajudar o usuário a entender melhor a situação apresentada.

            Regras de formatação da resposta:

            8. NÃO utilize títulos com "##" ou "###".
            9. Evite excesso de formatação em Markdown.
            10. Use no máximo:
            - negrito (**texto**) para destacar pontos importantes
            - listas simples com "-" quando necessário
            11. Prefira respostas em formato de conversa, como se estivesse falando diretamente com o usuário.
            12. Evite respostas muito longas. Seja claro e objetivo.
            13. Responda em no máximo 5 a 8 linhas.
            
            # PERSONALIDADE
            {personalidade}
            """

            llm = genai.GenerativeModel(
                model_name=MODELO_ESCOLHIDO,
                system_instruction=prompt_do_sistema,
            )

            resposta = llm.generate_content(prompt)
            return resposta.text
        except Exception as erro:
            repeticao += 1
            if repeticao >= maximo_tentativas:
                return "Erro no Gemini: %s" % erro
            
            sleep(50)

def limpar_formatacao(texto):
    texto = texto.replace("###", "")
    texto = texto.replace("##", "")
    return texto

@app.route("/chat", methods=["POST"])
def chat():
    inicio = time.time()

    prompt = request.json["msg"]
    resposta = bot(prompt)

    fim = time.time()
    tempo_resposta = fim - inicio

    print(f"Tempo de resposta: {tempo_resposta:.2f}s")

    return limpar_formatacao(resposta.text)

    # return {
    #         "resposta": resposta,
    #         "tempo": tempo_resposta
    #     }

@app.route("/")
def home():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug = True)



