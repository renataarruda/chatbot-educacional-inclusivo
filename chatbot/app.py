from flask import Flask, render_template, request, jsonify
import time
from services.llm_service import gerar_resposta, PERFIS
from services.feedback_service import salvar_feedback
from services.tempos import salvar_tempo

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    dados    = request.get_json()
    mensagem = dados.get("msg", "").strip()
    persona  = dados.get("persona", "outro")

    if not mensagem:
        return jsonify({"resposta": "Por favor, envie uma mensagem."}), 400

    if persona not in PERFIS:
        return jsonify({"resposta": "Perfil inválido."}), 400

    inicio = time.time()
    resposta = gerar_resposta(mensagem, persona)
    tempo_resposta = round(time.time() - inicio, 2)

    salvar_tempo({
        "persona":        persona,
        "tempo_segundos": tempo_resposta,
    })

    print(f"Tempo de resposta: {tempo_resposta:.2f}s")

    return jsonify({"resposta": resposta})


@app.route("/feedback", methods=["POST"])
def feedback():
    dados = request.get_json(silent=True) or {}

    salvar_feedback({
        "persona":    dados.get("persona", "desconhecido"),
        "satisfacao": dados.get("satisfacao", "não informado"),
        "comentario": dados.get("comentario", ""),
    })

    return jsonify({"ok": True})


if __name__ == "__main__":
    app.run(debug=True)