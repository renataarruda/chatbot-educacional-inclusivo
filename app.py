from flask import Flask,render_template, request, Response
import google.generativeai as genai
from dotenv import load_dotenv
import os
from time import sleep
from analisador_sentimentos import carrega, salva
from selecionar_persona import personas

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
            personalidade = personas["responsavel"]

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
            
            # PERSONALIDADE
            {personalidade}
            """

            # configuracao_modelo = {
            #     "temperature" : 0.1,
            #     "max_output_tokens" : 8192
            # }

            llm = genai.GenerativeModel(
                model_name=MODELO_ESCOLHIDO,
                system_instruction=prompt_do_sistema,
                # generation_config=configuracao_modelo
            )

            resposta = llm.generate_content(prompt)
            return resposta.text
        except Exception as erro:
            repeticao += 1
            if repeticao >= maximo_tentativas:
                return "Erro no Gemini: %s" % erro
            
            sleep(50)


@app.route("/chat", methods=["POST"])
def chat():
    prompt  = request.json["msg"]
    resposta = bot(prompt)
    return resposta

@app.route("/")
def home():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug = True)



