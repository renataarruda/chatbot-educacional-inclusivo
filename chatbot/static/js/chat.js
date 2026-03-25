document.addEventListener('DOMContentLoaded', () => {

let personaSelecionada  = null;
let satisfacaoEscolhida = null;
let aguardandoEncerramento = false; 

const chat           = document.querySelector('#chat');
const input          = document.querySelector('#input');
const botaoEnviar    = document.querySelector('#botao-enviar');
const botaoPaperclip = document.querySelector('#mais_arquivo');

const abrirFeedbackBtn    = document.querySelector('#abrir-feedback');
const modalFeedback       = document.querySelector('#modal-feedback');
const fecharFeedbackBtn   = document.querySelector('#fechar-feedback');
const enviarFeedbackBtn   = document.querySelector('#enviar-feedback');
const comentarioFeedback  = document.querySelector('#comentario-feedback');
const confirmacaoFeedback = document.querySelector('#confirmacao-feedback');
const satisfacaoOpcoes    = document.querySelector('#satisfacao-opcoes');

const labels = {
    pai:         "Pai",
    mae:         "Mãe",
    responsavel: "Responsável",
    gestor:      "Gestor",
    professor:   "Professor",
    outro:       "Outro",
};

document.querySelector('#persona-opcoes').querySelectorAll('.persona-btn').forEach(btn => {
    btn.addEventListener('click', () => selecionarPersona(btn.dataset.persona));
});

function selecionarPersona(persona) {
    personaSelecionada = persona;
    const opcoes = document.querySelector('#persona-opcoes');

    const escolhaLabel = labels[persona] || persona;
    const userBubble = criaBolha("usuario");
    userBubble.textContent = escolhaLabel;
    chat.insertBefore(userBubble, opcoes);

    opcoes.remove();

    const botBubble = criaBolha("bot");
    botBubble.innerHTML = mensagemBoasVindas(persona);
    chat.appendChild(botBubble);

    input.disabled          = false;
    botaoEnviar.disabled    = false;
    botaoPaperclip.disabled = false;
    input.placeholder       = "Enviar uma mensagem";
    input.focus();

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

async function enviarMensagem() {
    if (!input.value.trim() || !personaSelecionada) return;

    const mensagem = input.value.trim();
    input.value = "";

    if (aguardandoEncerramento) {
        aguardandoEncerramento = false;

        const userBubble = criaBolha("usuario");
        userBubble.textContent = mensagem;
        chat.appendChild(userBubble);
        vaiParaFinal();

        const botBubble = criaBolha("bot");
        chat.appendChild(botBubble);

        const respostaPositiva = ["sim", "s", "yes", "y", "claro", "com certeza",
                                  "ótimo", "otimo", "ajudou", "foi", "ok", "okay"].some(
            p => mensagem.toLowerCase().includes(p)
        );

        if (respostaPositiva) {
            botBubble.innerHTML = "Fico feliz em ter ajudado! 😊 Antes de encerrar, que tal deixar uma avaliação?";
        } else {
            botBubble.innerHTML = "Entendo, sinto muito por não ter conseguido ajudar melhor. Sua opinião é muito importante para melhorarmos. Pode deixar um feedback?";
        }

        vaiParaFinal();
        setTimeout(() => abrirModal(), 1500);
        return;
    }
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
    perguntarEncerramento();
}

function perguntarEncerramento() {
    aguardandoEncerramento = true;

    setTimeout(() => {
        const botBubble = criaBolha("bot");
        botBubble.innerHTML = "Sua dúvida foi respondida? <em>(responda sim ou não)</em>";
        chat.appendChild(botBubble);
        vaiParaFinal();
    }, 600);
}

function abrirModal() {
    satisfacaoEscolhida = null;
    comentarioFeedback.value = "";
    confirmacaoFeedback.hidden = true;
    enviarFeedbackBtn.hidden   = false;
    enviarFeedbackBtn.disabled = false;
    enviarFeedbackBtn.textContent = "Enviar avaliação";
    satisfacaoOpcoes.querySelectorAll('.satisfacao-btn').forEach(b => b.classList.remove('ativo'));

    modalFeedback.hidden = false;
}

abrirFeedbackBtn.addEventListener('click', abrirModal);

fecharFeedbackBtn.addEventListener('click', () => {
    modalFeedback.hidden = true;
});

modalFeedback.addEventListener('click', (e) => {
    if (e.target === modalFeedback) modalFeedback.hidden = true;
});

satisfacaoOpcoes.querySelectorAll('.satisfacao-btn').forEach(btn => {
    btn.addEventListener('click', () => {
        satisfacaoOpcoes.querySelectorAll('.satisfacao-btn').forEach(b => b.classList.remove('ativo'));
        btn.classList.add('ativo');
        satisfacaoEscolhida = btn.dataset.valor;
    });
});

enviarFeedbackBtn.addEventListener('click', async () => {
    if (!satisfacaoEscolhida) {
        satisfacaoOpcoes.style.outline      = "2px solid var(--primary)";
        satisfacaoOpcoes.style.borderRadius = "var(--radius)";
        setTimeout(() => { satisfacaoOpcoes.style.outline = "none"; }, 1500);
        return;
    }

    enviarFeedbackBtn.disabled     = true;
    enviarFeedbackBtn.textContent  = "Enviando...";

    try {
        await fetch("/feedback", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                persona:    personaSelecionada || "desconhecido",
                satisfacao: satisfacaoEscolhida,
                comentario: comentarioFeedback.value.trim(),
            }),
        });
    } catch (err) {
        console.error("Erro ao enviar feedback:", err);
    }

    enviarFeedbackBtn.hidden   = true;
    confirmacaoFeedback.hidden = false;

    setTimeout(() => {
        modalFeedback.hidden = true;
        reiniciarChat();
    }, 2500);
});

function reiniciarChat() {
    personaSelecionada     = null;
    satisfacaoEscolhida    = null;
    aguardandoEncerramento = false;

    chat.innerHTML = "";

    const boasVindas = document.createElement('p');
    boasVindas.className = "chat__bolha chat__bolha--bot";
    boasVindas.innerHTML = `Olá! Seja muito bem-vindo(a)! <br/><br/>
        Sou o seu assistente educacional especializado em educação inclusiva, com foco em Altas Habilidades e Superdotação.<br/><br/>
        Meu papel é oferecer orientações, esclarecer dúvidas e ajudar você a entender melhor como apoiar a inclusão de crianças e jovens com esse perfil.<br/><br/>
        Antes de começar, me diga: <strong>quem é você?</strong>`;
    chat.appendChild(boasVindas);

    const novaPersonaOpcoes = document.createElement('div');
    novaPersonaOpcoes.className = "persona-opcoes";
    novaPersonaOpcoes.id = "persona-opcoes";
    novaPersonaOpcoes.innerHTML = `
        <button class="persona-btn" data-persona="pai"> Pai</button>
        <button class="persona-btn" data-persona="mae"> Mãe</button>
        <button class="persona-btn" data-persona="responsavel"> Responsável</button>
        <button class="persona-btn" data-persona="gestor"> Gestor(a)</button>
        <button class="persona-btn" data-persona="professor"> Professor(a)</button>
        <button class="persona-btn" data-persona="outro"> Outro</button>
    `;
    chat.appendChild(novaPersonaOpcoes);

    novaPersonaOpcoes.querySelectorAll('.persona-btn').forEach(btn => {
        btn.addEventListener('click', () => selecionarPersona(btn.dataset.persona));
    });

    input.disabled          = true;
    botaoEnviar.disabled    = true;
    botaoPaperclip.disabled = true;
    input.placeholder       = "Primeiro, escolha seu perfil acima...";
    input.value             = "";
    abrirFeedbackBtn.hidden = true;

    vaiParaFinal();
}

function criaBolha(tipo) {
    const div = document.createElement('div');
    div.className = `chat__bolha chat__bolha--${tipo}`;
    return div;
}

function vaiParaFinal() {
    chat.scrollTop = chat.scrollHeight;
}

botaoEnviar.addEventListener('click', enviarMensagem);
input.addEventListener('keyup', e => {
    if (e.key === "Enter") enviarMensagem();
});

});