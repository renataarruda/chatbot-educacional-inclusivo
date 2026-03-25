# SuperChat: Chatbot Educacional para Inclusão e Superdotação

Este projeto tem como objetivo desenvolver um **chatbot educacional baseado em Inteligência Artificial** para o [**Instituto Criativo**](https://institutocriativo.com.br/), capaz de fornecer **orientações iniciais sobre educação inclusiva, altas habilidades e superdotação**.

A solução busca apoiar **pais, professores e gestores escolares** no esclarecimento de dúvidas frequentes relacionadas à inclusão educacional, oferecendo respostas acessíveis, informativas e contextualizadas.

O projeto foi desenvolvido como **Projeto Aplicado** do curso de Sistemas de Informação da **Faculdade XP Educação**, utilizando conceitos de **Design Thinking, Inteligência Artificial e desenvolvimento de software com Python**.

Como apoio, este projeto segue algumas instruções sugeridas no curso [**Formação Gemini e Python**](https://www.alura.com.br/formacao-gemini-python), da Alura.

---

# 🚀 MVP – Versão Final

O projeto evoluiu para um **MVP funcional com interface web**, permitindo interação mais próxima de um produto real.

### 🔹 Interface do Chat (SuperChat)

<img width="959" height="473" alt="image" src="https://github.com/user-attachments/assets/3ac5c0eb-e68e-423f-98c8-71a3a0069c86" />

O chatbot foi nomeado **SuperChat**, com identidade visual baseada nas cores do Instituto Criativo e foco em uma experiência simples e acessível.

---

# Objetivo do Projeto

Desenvolver, em 3 semanas, um **MVP (Minimum Viable Product)** de um chatbot capaz de:

- esclarecer dúvidas iniciais sobre inclusão educacional;
- orientar pais, professores e gestores escolares;
- centralizar informações confiáveis sobre altas habilidades e superdotação;
- oferecer orientação inicial de forma acessível e disponível sob demanda.

**Importante:**  
O chatbot **não realiza diagnósticos** e não substitui avaliação profissional especializada.

---

# Público-Alvo

O chatbot foi projetado para quatro perfis principais de usuários:

- **Pais e responsáveis**
- **Professores**
- **Gestores escolares**
- **Público geral (outros)**

Cada perfil recebe respostas adaptadas em linguagem, nível de detalhe e abordagem.

---

# Tecnologias Utilizadas

- Python  
- Flask (interface web)  
- API de IA generativa (Google Gemini)  
- Biblioteca `google-generativeai`  
- `python-dotenv`  

---
# ▶️ Como rodar o projeto localmente

Siga os passos abaixo para executar o projeto em sua máquina:

## 1. Clonar o repositório

```bash
git clone https://github.com/renataarruda/chatbot-educacional-inclusivo.git
cd chatbot-educacional-inclusivo
```
## 2. Criar e ativar o ambiente virtual
### Windows
```bash
python -m venv venv
venv\Scripts\activate
```
### Linux/Mac
```bash
python3 -m venv venv
source venv/bin/activate
```
## 3. Instalar as dependências
```bash
pip install -r requirements.txt
```
## 4. Configurar variáveis de ambiente

Crie um arquivo .env na raiz do projeto com o seguinte conteúdo:
```bash
GOOGLE_API_KEY=sua_chave_aqui
```
Você pode obter uma chave de API no Google AI Studio.

## 5. Executar a aplicação
```bash
python app.py
```

## 6. Acessar no navegador

Abra o navegador e acesse:
```bash
http://localhost:5000
```

# 🧪 Modo Debug (opcional)

O projeto possui um modo de depuração que utiliza respostas simuladas (mock responses), permitindo testar o fluxo do chatbot sem consumir a API.

Para ativar, ajuste a configuração no código conforme indicado no arquivo principal.

# ⚠️ Possíveis problemas
- **Erro de dependências:**
Execute novamente pip install -r requirements.txt
- **Erro de chave da API:**
Verifique se o arquivo .env foi criado corretamente
- **Problemas ao rodar no Windows:**
Certifique-se de que o ambiente virtual está ativado

# Funcionalidades do MVP

- Seleção de persona diretamente no chat;  
- Respostas personalizadas por perfil de usuário;  
- Geração de respostas com IA (LLM);  
- Sugestão de materiais complementares; 
- Reset do chat após encerramento;  
- Nova escolha de persona sem recarregar a aplicação;  
- Coleta de feedback do usuário;  
- Registro de tempo de resposta;  
- Armazenamento de interações em arquivo.

---

# Fluxo de Interação

1. Apresentação do chatbot;
2. Escolha da persona diretamente no chat;
3. Envio da pergunta pelo usuário;
4. Geração da resposta (LLM ou modo debug);
5. Sugestão de material complementar;
6. Encerramento da conversa;
7. Coleta de feedback.

---

# 📊 Resultados do MVP

## Tempo médio de resposta

O tempo médio geral obtido foi de:

**➡️ 8,74 segundos por resposta**

- Respostas simples (ex: saudação): ~5 segundos  
- Respostas com IA: entre 8 e 12 segundos  

Esse desempenho foi considerado adequado para um MVP baseado em modelo generativo.

---

## Testes piloto

Foram realizados testes com usuários simulando diferentes perfis.

### ✔️ Satisfação geral
**100% dos usuários indicaram satisfação com as respostas**

### 💬 Principais feedbacks

- “Resposta clara e objetiva.”  
- “Respondeu corretamente e enviou material complementar.”  
- “Resposta adequada ao público.”  
- “Detalhada e bem estruturada.”  

### 🔍 Insights

- Boa adaptação da linguagem por persona;  
- Material complementar como diferencial;  
- Oportunidade de melhoria na formatação das respostas. 

---

# 🧪 Monitoramento de Tokens e Custos

Foi desenvolvido um script para:

- análise de consumo de tokens;  
- comparação entre modelos;  
- estimativa de custo por requisição .

Modelos analisados:

- `gemini-3-flash-preview`  
- `gemini-3.1-pro-preview`  

---

# 📊 Avaliação das Respostas

Foi implementado um **analisador de sentimentos** para interpretar feedbacks dos usuários, incluindo:

- classificação de sentimento;  
- identificação de pontos fortes;  
- identificação de melhorias. 

---

# 🧩 Sprints do Projeto

## Sprint 1 — Base técnica
- Integração com API Gemini  
- Prompt inicial  
- Interface em terminal  
- Modo debug  

## Sprint 2 — Personalização
- Personas  
- Ajuste de linguagem  
- Feedback do usuário  
- Análise de sentimentos  

## Sprint 3 — MVP Web
- Interface com Flask    
- Testes piloto  
- Medição de tempo de resposta  
- Persistência de dados
- Refatoração do código 

---

# ⚠️ Limitações

- Formatação das respostas da LLM ainda limitada; 
- Tempo de resposta pode ser otimizado;  
- Ausência de memória de conversa;  
- Dependência de modelo generativo;  
- Base de conhecimento não especializada.  

---

# 🔮 Melhorias Futuras

- Chat híbrido (respostas pré-definidas + IA);  
- Melhor formatação das respostas;  
- Redução do tempo de resposta; 
- Acessibilidade (leitor de tela, envio de perguntas por áudio);  
- Deploy estável e escalável.

---

# 💡 Considerações Finais

O projeto demonstrou que a utilização de um chatbot com adaptação por personas é uma solução viável para apoiar a comunicação em contextos educacionais.

Os resultados indicaram boa aceitação pelos usuários, com respostas consideradas claras, úteis e adequadas aos diferentes perfis. O MVP desenvolvido conseguiu validar os principais requisitos propostos, consolidando uma base funcional para evolução do sistema.

Apesar das limitações técnicas identificadas, especialmente relacionadas à formatação das respostas e ao tempo de processamento, a solução apresenta potencial de expansão, tanto em termos de usabilidade quanto de impacto educacional.

---

# 📂 Repositório

🔗 https://github.com/renataarruda/chatbot-educacional-inclusivo

---

# Licença

Projeto com finalidade **educacional e acadêmica**.
