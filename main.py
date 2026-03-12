import os
import time
import google.generativeai as genai
from google.api_core.exceptions import ResourceExhausted, NotFound
from dotenv import load_dotenv

load_dotenv()

CHAVE_API_GOOGLE = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=CHAVE_API_GOOGLE)
MODELO_ESCOLHIDO = "gemini-3-flash-previewzzzzzz"
MODO_DEBUG = False

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

def criar_modelo():
    try:
        return genai.GenerativeModel(
        model_name=MODELO_ESCOLHIDO,
        system_instruction=prompt_sistema,
        # generation_config=configuracao_modelo
    )
    except NotFound as e:
        MODELO_ESCOLHIDO = "gemini-3-flash-preview"
        print(f"Erro no nome do modelo: {e}")

def gerar_resposta(llm, pergunta):
    if MODO_DEBUG:
        print("[DEBUG] Usando resposta simulada")
        if "superdotado" in pergunta.lower():
            return "Mock: Alunos superdotados se beneficiam de atividades abertas e investigativas. Gostaria de fazer outra pergunta?"

        if "inclusão" in pergunta.lower():
            return "Mock: A inclusão escolar envolve adaptar práticas pedagógicas para atender diferentes necessidades. Gostaria de fazer outra pergunta?"

        return "Mock: resposta genérica do assistente educacional."
    try:
        resposta = llm.generate_content(pergunta)
        time.sleep(2)
        return resposta.text
    except ResourceExhausted:
        print("Limite da API atingido. Tente novamente mais tarde.")

def iniciar_chat(llm, mensagem_inicial):

    print(mensagem_inicial)

    while True:

        pergunta = input("\nVocê: ")

        if pergunta.lower() == "sair":
            finalizar_chatbot()
            break

        resposta = gerar_resposta(llm, pergunta)

        print("-" * 50)
        print("Assistente:", resposta)
        print("-" * 50)

def finalizar_chatbot():
    print("Encerrando o chatbot. Até mais!")
    # exit()

def opcao_invalida():
    print('Opção inválida\n')

def retornar_menu_principal():
    input('\nDigite enter para voltar para o menu principal ')
    main()

def exibir_apresentacao_chatbot():
    print("""
Olá! Seja muito bem-vindo(a)! 
Sou o seu assistente educacional especializado em educação inclusiva, com foco em Altas Habilidades e Superdotação.
Meu papel é oferecer orientações, esclarecer dúvidas e ajudar você a entender melhor como apoiar a inclusão de crianças e jovens com esse perfil. 
        """)

def exibir_opcoes():
    llm = criar_modelo()
    opcao_escolhida = input("""
Para que eu possa oferecer a melhor orientação, informe o seu perfil:
1 - Mãe, pai ou responsável familiar
2 - Professor(a)
3 - Gestor(a) escolar
4 - Outro 
5 - Sair

Digite aqui: """)

    if opcao_escolhida == "1":
        iniciar_chat(llm, """
Que alegria ter você aqui!
Fique à vontade para contar sua dúvida.
""")
    elif opcao_escolhida == "2":
        iniciar_chat(llm, """
Olá professor(a)!
Qual é sua dúvida pedagógica hoje?
""")
    elif opcao_escolhida == "3":
        iniciar_chat(llm,"""
Olá gestor(a)!
Como posso ajudar na inclusão escolar?
""")
    elif opcao_escolhida == "4":
        iniciar_chat(llm,"""
Olá! Qual é sua dúvida sobre inclusão ou altas habilidades?
""")
    elif opcao_escolhida == "5":
        finalizar_chatbot()
        return
    else:
        opcao_invalida()
        retornar_menu_principal()
        
def main():
    os.system('cls')
    exibir_apresentacao_chatbot()
    exibir_opcoes()

if __name__ == "__main__":
    main()