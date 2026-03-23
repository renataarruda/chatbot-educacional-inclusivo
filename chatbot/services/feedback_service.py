import os

def salvar_feedback(data):
    os.makedirs("dados", exist_ok=True)
    with open("dados/feedbacks.txt", "a", encoding="utf-8") as f:
        f.write(str(data) + "\n")