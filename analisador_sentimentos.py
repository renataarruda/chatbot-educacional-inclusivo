import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

CHAVE_API_GEMINI = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=CHAVE_API_GEMINI)
MODELO = "gemini-3-flash-preview"

def carrega(nome_do_arquivo):
    try:
        with open(nome_do_arquivo, "rb") as arquivo:
            dados = arquivo.read()
            return dados
    except IOError as e:
        print(f"Erro: {e}")

def salva(nome_do_arquivo, conteudo):
    try:
        with open(nome_do_arquivo, "w", encoding="utf-8") as arquivo:
            arquivo.write(conteudo)
    except IOError as e:
        print(f"Erro ao salvar arquivo: {e}")

prompt_sistema = f"""
        Você é um analisador de sentimentos de feedbacks de respostas às perguntas dos usuários.
        Escreva um parágrafo com até 50 palavras resumindo a satisfação e os comentários sobre a qualidade de respostas e
        depois atribua qual o sentimento geral para a experiência no chatbot.
        Identifique também 3 pontos fortes e 3 pontos fracos identificados a partir das avaliações.

        # Formato de Saída

        Perfil de usuário:
        Resumo dos comentários:
        Satisfação Geral: [utilize aqui apenas Positivo, Negativo ou Neutro]
        Ponto fortes: lista com três bullets
        Pontos fracos: lista com três bullets
    """

llm = genai.GenerativeModel(
    model_name=MODELO,
    system_instruction=prompt_sistema
)

# model = genai.GenerativeModel(MODELO)
avaliacoes = carrega("dados/avaliacoes_chatbot.txt")

prompt_usuario = f"""
{prompt_sistema}

Avaliações dos usuários:

{avaliacoes}
"""

resposta = llm.generate_content(prompt_usuario)
analise = resposta.text
salva("dados/analise_sentimentos.txt", analise)

print("Análise concluída. Resultado salvo em dados/analise_sentimentos.txt")