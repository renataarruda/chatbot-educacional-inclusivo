import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

MODELO_FLASH = "gemini-3-flash-preview"
MODELO_PRO = "gemini-3.1-pro-preview"

CUSTO_ENTRADA_FLASH = 0.50
CUSTO_SAIDA_FLASH = 3.00

CUSTO_ENTRADA_PRO = 2.00
CUSTO_SAIDA_PRO = 4.00

model_flash = genai.get_model(f"models/{MODELO_FLASH}")
limites_modelo_flash = {
    "tokens_entrada": model_flash.input_token_limit,
    "tokens_saida": model_flash.output_token_limit,
}

model_pro = genai.get_model(f"models/{MODELO_PRO}")
limites_modelo_pro = {
    "tokens_entrada": model_pro.input_token_limit,
    "tokens_saida": model_pro.output_token_limit,
}

print(f"Limites do modelo flash são: {limites_modelo_flash}")
print(f"Limites do modelo pro são: {limites_modelo_pro}")

llm_flash = genai.GenerativeModel(
    f"models/{MODELO_FLASH}"
)

quantidade_tokens = llm_flash.count_tokens("Como a escola pode integrar um aluno com altas habilidades?")
print(f"A quantidade de tokens é: {quantidade_tokens}")

resposta = llm_flash.generate_content("Como a escola pode integrar um aluno com altas habilidades?")
tokens_prompt = resposta.usage_metadata.prompt_token_count
tokens_resposta = resposta.usage_metadata.candidates_token_count

custo_total = (tokens_prompt * CUSTO_ENTRADA_FLASH) / 1000000 + (tokens_resposta * CUSTO_SAIDA_FLASH) / 1000000
print(f"Custo Total U$ Flash: ", custo_total)

custo_total = (tokens_prompt * CUSTO_ENTRADA_PRO) / 1000000 + (tokens_resposta * CUSTO_SAIDA_PRO) / 100.000
print(f"Custo Total U$ Pro: ", custo_total)