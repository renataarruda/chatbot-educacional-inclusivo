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

- Python
- API de IA generativa (Google Gemini)
- Biblioteca `google-generativeai`
- `python-dotenv` para gerenciamento de variáveis de ambiente

O chatbot atualmente funciona por meio de uma **interface simples no terminal**, permitindo interação direta com o modelo de linguagem.

Durante o desenvolvimento foi implementado também um **modo de depuração (debug)** com respostas simuladas (*mock responses*), permitindo testar a lógica do chatbot sem consumir tokens da API.

---

# Fluxo de Interação

O chatbot segue o seguinte fluxo:

1. Apresentação do assistente educacional
2. Seleção do perfil do usuário (pais, professores ou gestores)
3. Recebimento da pergunta
4. Geração da resposta pelo modelo de IA ou pelo modo debug
5. Sugestão de materiais complementares relacionados ao tema
6. Continuação da conversa ou encerramento
7. Coleta de feedback do usuário ao final da interação

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

# Avaliação das Respostas

Para apoiar a análise da qualidade das respostas do chatbot foi desenvolvido um **script auxiliar de análise de sentimentos**.

Esse script lê um arquivo contendo **feedbacks de usuários** e utiliza um modelo de linguagem para gerar um resumo qualitativo das avaliações.

A análise inclui:

- resumo geral das avaliações;
- classificação do sentimento geral (positivo, neutro ou negativo);
- identificação de **pontos fortes** das respostas do chatbot;
- identificação de **pontos de melhoria**.

Como o chatbot ainda não possui usuários reais, foi criado também um **arquivo de feedbacks simulados**, utilizado para testar o funcionamento do analisador.

---

# Status do Projeto

🚧 Projeto em desenvolvimento

O desenvolvimento está organizado em **sprints semanais**, com foco na construção incremental de um MVP.

---

# Sprint 1 — Estruturação e Base Técnica

Objetivo: construir a base funcional do chatbot.

Atividades realizadas:

- definição dos fluxos conversacionais principais;
- criação do **prompt base do assistente educacional**;
- integração inicial com a **API de IA do Google Gemini**;
- implementação de **interface simples de interação via terminal**;
- criação de **modo debug com respostas simuladas** para testes;
- organização do backlog do projeto.

---

# Sprint 2 — Personalização e Avaliação das Respostas

Objetivo: melhorar a contextualização das respostas e implementar mecanismos iniciais de avaliação da qualidade do chatbot.

Atividades realizadas:

- implementação de **identificação de perfil do usuário** (pais, professores ou gestores);
- **personalização contextual do prompt** com base no perfil selecionado;
- inclusão de **recomendações de materiais complementares** nas respostas;
- implementação de **coleta de feedback ao final da interação** com o usuário;
- desenvolvimento de **script de análise de sentimentos para avaliações**;
- criação de **arquivo de feedbacks simulados** para testes do analisador;
- realização de **testes de qualidade das respostas do chatbot**.

Durante os testes foi identificado um comportamento ocasional de **repetição de seções e trechos nas respostas geradas pela LLM**, mesmo após ajustes no prompt. Esse comportamento foi registrado como uma limitação observada durante o desenvolvimento.

---

# Próximos Passos

Sprint 3 – Finalização do MVP:

- Criar interface web simples;
- Aplicar testes piloto;
- Medir tempo médio de resposta;
- Documentar MVP.

---

# Limitações Conhecidas

Por se tratar de um **MVP (Minimum Viable Product)** desenvolvido para fins acadêmicos, o chatbot apresenta algumas limitações conhecidas:

### Comportamento ocasional de repetição nas respostas
Durante os testes com o modelo de linguagem foi observado que, em alguns casos, a LLM pode repetir títulos, seções ou trechos da resposta. Ajustes no prompt foram realizados para reduzir esse comportamento, mas ele ainda pode ocorrer eventualmente.

### Dependência de modelo generativo
As respostas do chatbot são geradas por um modelo de linguagem. Apesar de utilizar instruções para priorizar clareza e responsabilidade informacional, o sistema pode produzir respostas incompletas ou imprecisas em determinados contextos.

### Ausência de memória de conversação
Nesta versão do projeto, o chatbot responde a cada pergunta de forma isolada, sem manter histórico completo de contexto entre interações.

### Base de conhecimento não especializada
O chatbot utiliza conhecimento geral do modelo de linguagem e não possui uma base de dados própria ou curadoria especializada integrada ao sistema.

### Uso em ambiente de testes
Atualmente o chatbot opera em **interface de terminal**, sendo utilizado principalmente para testes e validação do comportamento do sistema durante o desenvolvimento do MVP.

---

# Contribuições

Este projeto foi desenvolvido como parte de um **Projeto Aplicado acadêmico**, mas sugestões de melhorias e discussões sobre o tema são bem-vindas.

---

# Licença

Este projeto possui finalidade **educacional e acadêmica**, sendo desenvolvido como parte de um Projeto Aplicado do curso de Sistemas de Informação.
