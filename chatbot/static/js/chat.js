document.addEventListener('DOMContentLoaded', () => {
 
// ─── Estado global ───────────────────────────────────────────────
let personaSelecionada  = null;
let satisfacaoEscolhida = null;
 
// ─── Elementos do DOM ────────────────────────────────────────────
const chat           = document.querySelector('#chat');
const input          = document.querySelector('#input');
const botaoEnviar    = document.querySelector('#botao-enviar');
const botaoPaperclip = document.querySelector('#mais_arquivo');
const personaOpcoes  = document.querySelector('#persona-opcoes');
 
// Feedback
const abrirFeedbackBtn    = document.querySelector('#abrir-feedback');
const modalFeedback       = document.querySelector('#modal-feedback');
const fecharFeedbackBtn   = document.querySelector('#fechar-feedback');
const enviarFeedbackBtn   = document.querySelector('#enviar-feedback');
const comentarioFeedback  = document.querySelector('#comentario-feedback');
const confirmacaoFeedback = document.querySelector('#confirmacao-feedback');
const satisfacaoOpcoes    = document.querySelector('#satisfacao-opcoes');
 
// ─── Labels de persona ───────────────────────────────────────────
const labels = {
    pai:         "Pai",
    mae:         "Mãe",
    responsavel: "Responsável",
    gestor:      "Gestor",
    professor:   "Professor",
    outro:       "Outro",
};
 
// ════════════════════════════════════════════════════════════════
// SELEÇÃO DE PERSONA
// ════════════════════════════════════════════════════════════════
personaOpcoes.querySelectorAll('.persona-btn').forEach(btn => {
    btn.addEventListener('click', () => selecionarPersona(btn.dataset.persona));
});
 
function selecionarPersona(persona) {
    personaSelecionada = persona;
 
    // Bolha com a escolha do usuário
    const escolhaLabel = labels[persona] || persona;
    const userBubble = criaBolha("usuario");
    userBubble.textContent = escolhaLabel;
    chat.insertBefore(userBubble, personaOpcoes);
 
    // Remove os botões de seleção
    personaOpcoes.remove();
 
    // Mensagem de boas-vindas do bot
    const botBubble = criaBolha("bot");
    botBubble.innerHTML = mensagemBoasVindas(persona);
    chat.appendChild(botBubble);
 
    // Libera o campo de entrada
    input.disabled        = false;
    botaoEnviar.disabled  = false;
    botaoPaperclip.disabled = false;
    input.placeholder     = "Enviar uma mensagem";
    input.focus();
 
    // Exibe o botão de avaliação no cabeçalho
    abrirFeedbackBtn.hidden = false;
 
    vaiParaFinal();
}
 
function mensagemBoasVindas(persona) {
    const mensagens = {
        pai:         "Olá, pai! Fico feliz em poder ajudar. Como posso te apoiar hoje?",
        mae:         "Olá, mãe! Fico feliz em poder ajudar. Como posso te apoiar hoje?",
        responsavel: "Olá! Como responsável, você tem um papel fundamental. O que gostaria de saber?",
        gestor:      "Olá, gestor(a)! Posso te ajudar com políticas e práticas de inclusão. Qual é a sua dúvida?",
        professor:   "Olá, professor(a)! Vamos conversar sobre como apoiar seus alunos. O que você precisa?",
        outro:       "Olá! Fico feliz em conversar sobre educação inclusiva. Como posso te ajudar?",
    };
    return mensagens[persona] || "Olá! Como posso te ajudar?";
}
 
// ════════════════════════════════════════════════════════════════
// ENVIO DE MENSAGENS
// ════════════════════════════════════════════════════════════════
async function enviarMensagem() {
    if (!input.value.trim() || !personaSelecionada) return;
 
    const mensagem = input.value.trim();
    input.value = "";
 
    const userBubble = criaBolha("usuario");
    userBubble.textContent = mensagem;
    chat.appendChild(userBubble);
 
    const botBubble = criaBolha("bot");
    botBubble.innerHTML = "Digitando...";
    chat.appendChild(botBubble);
 
    vaiParaFinal();
 
    try {
        const res = await fetch("/chat", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ msg: mensagem, persona: personaSelecionada }),
        });
 
        const data = await res.json();
        botBubble.innerHTML = marked.parse(data.resposta);
    } catch (err) {
        botBubble.innerHTML = "Ops! Ocorreu um erro. Tente novamente.";
        console.error(err);
    }
 
    vaiParaFinal();
}
 
// ════════════════════════════════════════════════════════════════
// MODAL DE FEEDBACK
// ════════════════════════════════════════════════════════════════
abrirFeedbackBtn.addEventListener('click', () => {
    // Reseta o modal a cada abertura
    satisfacaoEscolhida = null;
    comentarioFeedback.value = "";
    confirmacaoFeedback.hidden = true;
    enviarFeedbackBtn.hidden   = false;
    satisfacaoOpcoes.querySelectorAll('.satisfacao-btn').forEach(b => b.classList.remove('ativo'));
 
    modalFeedback.hidden = false;
});
 
fecharFeedbackBtn.addEventListener('click', () => {
    modalFeedback.hidden = true;
});
 
// Fechar clicando fora do modal
modalFeedback.addEventListener('click', (e) => {
    if (e.target === modalFeedback) modalFeedback.hidden = true;
});
 
// Seleção de satisfação (👍 / 🤔 / 👎)
satisfacaoOpcoes.querySelectorAll('.satisfacao-btn').forEach(btn => {
    btn.addEventListener('click', () => {
        satisfacaoOpcoes.querySelectorAll('.satisfacao-btn').forEach(b => b.classList.remove('ativo'));
        btn.classList.add('ativo');
        satisfacaoEscolhida = btn.dataset.valor;
    });
});
 
// Envio do feedback para o backend
enviarFeedbackBtn.addEventListener('click', async () => {
    if (!satisfacaoEscolhida) {
        // Destaca os botões de satisfação para chamar atenção
        satisfacaoOpcoes.style.outline = "2px solid var(--primary)";
        satisfacaoOpcoes.style.borderRadius = "var(--radius)";
        setTimeout(() => { satisfacaoOpcoes.style.outline = "none"; }, 1500);
        return;
    }
 
    // Desabilita o botão para evitar duplo envio
    enviarFeedbackBtn.disabled = true;
    enviarFeedbackBtn.textContent = "Enviando...";
 
    try {
        const res = await fetch("/feedback", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                persona:    personaSelecionada || "desconhecido",
                satisfacao: satisfacaoEscolhida,
                comentario: comentarioFeedback.value.trim(),
            }),
        });
 
        // Mostra confirmação independente do status HTTP
        enviarFeedbackBtn.hidden   = true;
        confirmacaoFeedback.hidden = false;
        setTimeout(() => { modalFeedback.hidden = true; }, 2000);
 
    } catch (err) {
        // Mesmo com erro de rede, confirma para o usuário
        console.error("Erro ao enviar feedback:", err);
        enviarFeedbackBtn.hidden   = true;
        confirmacaoFeedback.hidden = false;
        setTimeout(() => { modalFeedback.hidden = true; }, 2000);
    }
});
 
// ════════════════════════════════════════════════════════════════
// UTILITÁRIOS
// ════════════════════════════════════════════════════════════════
function criaBolha(tipo) {
    const div = document.createElement('div');
    div.className = `chat__bolha chat__bolha--${tipo}`;
    return div;
}
 
function vaiParaFinal() {
    chat.scrollTop = chat.scrollHeight;
}
 
// ─── Eventos de envio ────────────────────────────────────────────
botaoEnviar.addEventListener('click', enviarMensagem);
input.addEventListener('keyup', e => {
    if (e.key === "Enter") enviarMensagem();
});
 
}); 