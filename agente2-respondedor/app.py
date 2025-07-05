from fastapi import FastAPI, Query
import requests
from transformers import pipeline

app = FastAPI()
gerador = pipeline("text-generation", model="distilgpt2")

AGENTE1_URL = "http://localhost:8001/buscar-contexto/"

@app.get("/perguntar/")
def perguntar(pergunta: str = Query(...)):
    resposta_agente1 = requests.get(AGENTE1_URL, params={"pergunta": pergunta})
    contextos = resposta_agente1.json().get("contextos", [])
    contexto = "\n".join(contextos)
    resposta = gerador(f"{contexto}\nPergunta: {pergunta}\nResposta:", max_length=150, num_return_sequences=1)[0]['generated_text']
    return {"resposta": resposta}
