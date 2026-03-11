# Chatbot Educacional para Inclusão e Superdotação

Este projeto tem como objetivo desenvolver um **chatbot educacional baseado em Inteligência Artificial** para o [**Instituto Criativo**](https://institutocriativo.com.br/), capaz de fornecer **orientações iniciais sobre educação inclusiva, altas habilidades e superdotação**.

A solução busca apoiar **pais, professores e gestores escolares** no esclarecimento de dúvidas frequentes relacionadas à inclusão educacional, oferecendo respostas acessíveis, informativas e contextualizadas.

O projeto está sendo desenvolvido como **Projeto Aplicado** do curso de Sistemas de Informação da **Faculdade XP Educação**, utilizando conceitos de **Design Thinking, Inteligência Artificial e desenvolvimento de software com Python**.

Como apoio, este projeto segue algumas instruções sugeridas no curso [**Formação Gemini e Python**](https://www.alura.com.br/formacao-gemini-python), da Alura.

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

O chatbot foi projetado para três perfis principais de usuários:

### Pais e responsáveis
Pessoas que possuem dúvidas sobre comportamentos, desenvolvimento ou possíveis sinais de altas habilidades em crianças.

### Professores
Educadores que buscam estratégias pedagógicas e orientações para lidar com alunos com diferentes necessidades educacionais.

### Gestores escolares
Profissionais responsáveis por decisões institucionais relacionadas à inclusão educacional.

---

# Tecnologias Utilizadas

Este projeto utiliza as seguintes tecnologias:

- Python;
- API de IA generativa (Google Gemini);  
- Biblioteca `google-generativeai`;
- `python-dotenv` para gerenciamento de variáveis de ambiente .

O chatbot atualmente funciona por meio de uma **interface simples no terminal**, permitindo interação direta com o modelo de linguagem. Foi criado um mock inicial simulando respostas para evitar o gasto com tokens da API.

---

# Fluxo de Interação

O chatbot segue o seguinte fluxo:

1. Apresentação do assistente educacional
2. Seleção do perfil do usuário
3. Recebimento da pergunta
4. Geração da resposta pelo modelo de IA
5. Continuação ou encerramento da conversa

---

# Monitoramento de Tokens e Estimativa de Custos

Durante o desenvolvimento do projeto foi implementado um script auxiliar para **monitoramento do consumo de tokens e estimativa de custo de utilização da API de IA**.

Essa etapa é importante para compreender o impacto financeiro do uso de modelos generativos em aplicações reais, especialmente em soluções escaláveis como chatbots.

O script realiza as seguintes funções:

- consulta os **limites de tokens de entrada e saída dos modelos**
- calcula a **quantidade de tokens utilizados em uma pergunta**
- mede os **tokens consumidos na resposta**
- estima o **custo aproximado da requisição**

Atualmente são analisados dois modelos da API Gemini:

- `gemini-3-flash-preview` – modelo mais rápido e econômico
- `gemini-3.1-pro-preview` – modelo mais robusto para respostas complexas

---

# Status do Projeto
🚧 Projeto em desenvolvimento

Atualmente o projeto encontra-se na **Sprint 1 – Estruturação e Base Técnica**, que contempla:

- definição dos fluxos conversacionais;
- criação do prompt base do assistente;
- integração inicial com API de IA;
- interface simples de testes no terminal;
- organização do backlog do projeto.

---

# Licença

Este projeto está sendo desenvolvido para fins acadêmicos e educacionais.
