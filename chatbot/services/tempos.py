import os
 
def salvar_tempo(data):
    os.makedirs("dados", exist_ok=True)
    with open("dados/tempos.txt", "a", encoding="utf-8") as f:
        f.write(str(data) + "\n")