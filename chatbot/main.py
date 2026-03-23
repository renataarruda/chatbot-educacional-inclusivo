import os
import time
import google.generativeai as genai
from google.api_core.exceptions import ResourceExhausted, NotFound
from dotenv import load_dotenv

load_dotenv()

CHAVE_API_GOOGLE = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=CHAVE_API_GOOGLE)
MODELO_ESCOLHIDO = "gemini-3-flash-preview"
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
Sempre considere o perfil do usuário informado no início da pergunta.

- Se a pergunta for de um pai ou mãe, utilize linguagem simples e acolhedora. Utilize emojis nas respostas.
- Se a pergunta for de um professor, ofereça sugestões pedagógicas práticas.
- Se a pergunta for de um gestor, foque em estratégias institucionais ou organizacionais.
- Se a pergunta for de um outro usuário, utilize linguagem simples e foque em respostas de conhecimento geral.

Não repita respostas, seções e títulos.

Sempre que apropriado, sugira que a pessoa procure profissionais especializados ou apoio pedagógico.

Seu papel é oferecer orientação inicial, esclarecer dúvidas e ajudar o usuário a entender melhor a situação apresentada."""

configuracao_modelo = {
    "temperature" : 2.0,
    "top_p": 0.9,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain"
}

materiais_recomendados = {
    "superdotação": "Você pode saber mais sobre altas habilidades no portal do MEC: https://www.gov.br/mec/pt-br/pneei",
    "inclusão": "Uma boa referência sobre educação inclusiva é o material do Instituto Rodrigo Mendes: https://institutorodrigomendes.org.br",
    "legislação": "Para conhecer o que diz a lei, acesse o Capítulo V da Lei de Diretrizes e Bases: https://www.planalto.gov.br/ccivil_03/leis/l9394.htm",
    "superdotado": "Consulte o Guia para Superdotados, Famílias e Profissionais no EduCAPES para mais orientações: https://educapes.capes.gov.br/",
    "diversidade": "O Portal DIVERSA oferece excelentes materiais sobre gestão escolar inclusiva: https://diversa.org.br/"
}

def sugestao_material_complementar(pergunta):
        
        pergunta = pergunta.lower()

        if "superdot" in pergunta:
            return materiais_recomendados["superdotação"]
        if "inclusiv" in pergunta or "inclusão" in pergunta:
            return materiais_recomendados["inclusão"]
        if "lei" in pergunta:
            return materiais_recomendados["legislação"]
        if "diversidade" in pergunta:
            return materiais_recomendados["diversidade"]
        return None

def criar_modelo():
    try:
        MODELO_ESCOLHIDO = "gemini-3-flash-preview"
        return genai.GenerativeModel(
        model_name=MODELO_ESCOLHIDO,
        system_instruction=prompt_sistema,
        # generation_config=configuracao_modelo
    )
    except NotFound as e:
        MODELO_ESCOLHIDO = "gemini-3-flash-preview"
        print(f"Erro no nome do modelo: {e}")

def coletar_feedback(perfil):
    print("\nAntes de encerrar, sua opinião é muito importante.")

    feedback = input("As respostas do chatbot foram úteis para você? (sim/não): ")

    comentario = input("Se quiser, deixe um comentário ou sugestão: ")

    with open("dados/feedback_chatbot.txt", "a", encoding="utf-8") as f:
        f.write(f"Perfil: {perfil}\n")
        f.write(f"Satisfação: {feedback}\n")
        f.write(f"Comentário: {comentario}\n")
        f.write("-" * 40 + "\n")

    print("\nAgradecemos pelo seu feedback! Ele ajuda a melhorar o nosso serviço.")

def gerar_resposta(llm, pergunta, perfil):
    if MODO_DEBUG:
        print("[DEBUG] Usando resposta simulada")
        if "superdot" in pergunta.lower():
            resposta = "Mock: Alunos superdotados se beneficiam de atividades abertas e investigativas. Gostaria de fazer outra pergunta?"

        elif "inclusão" in pergunta.lower():
            resposta = "Mock: A inclusão escolar envolve adaptar práticas pedagógicas para atender diferentes necessidades. Gostaria de fazer outra pergunta?"

        else: 
            resposta ="Mock: resposta genérica do assistente educacional."
        
        material = sugestao_material_complementar(pergunta)

        if material:
            resposta += "\n\n" + material
        return resposta
    
    try:
        pergunta_com_contexto = f"""
Perfil do usuário: {perfil}

Pergunta do usuário:
{pergunta}
"""
        if pergunta:
            resposta = llm.generate_content(pergunta_com_contexto).text
            time.sleep(2)

            material = sugestao_material_complementar(pergunta)

            if material:
                resposta += "\n\n" + material
            return resposta
        else:
            finalizar_chatbot()
            exit()
    
    except ResourceExhausted:
        print("Limite da API atingido. Tente novamente mais tarde.")

def iniciar_chat(llm, mensagem_inicial, perfil):
    print(mensagem_inicial)

    while True:
        pergunta = input("\nVocê: ")

        if pergunta.lower() in ["sair", "nao", "não"]:
            coletar_feedback(perfil)
            finalizar_chatbot()
            break

        resposta = gerar_resposta(llm, pergunta, perfil)

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
""", "mãe, pai ou responsável")
    elif opcao_escolhida == "2":
        iniciar_chat(llm, """
Olá professor(a)!
Qual é sua dúvida pedagógica hoje?
""", "professor(a)")
    elif opcao_escolhida == "3":
        iniciar_chat(llm,"""
Olá gestor(a)!
Como posso ajudar na inclusão escolar?
""", "gestor(a) escolar")
    elif opcao_escolhida == "4":
        iniciar_chat(llm,"""
Olá! Qual é sua dúvida sobre inclusão ou altas habilidades?
""", "outro usuário")
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
