from fastapi import FastAPI, UploadFile, File
from sentence_transformers import SentenceTransformer
import fitz  # PyMuPDF
import faiss
import numpy as np

app = FastAPI()
model = SentenceTransformer('all-MiniLM-L6-v2')
index = faiss.IndexFlatL2(384)
docs = []

@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    content = await file.read()
    doc = fitz.open(stream=content, filetype="pdf")
    full_text = ""
    for page in doc:
        full_text += page.get_text()

    chunks = [full_text[i:i+500] for i in range(0, len(full_text), 500)]
    embeddings = model.encode(chunks)
    global docs
    docs = chunks
    index.add(np.array(embeddings))
    return {"message": "Arquivo processado", "chunks": len(chunks)}

@app.get("/buscar-contexto/")
def buscar_contexto(pergunta: str):
    pergunta_vec = model.encode([pergunta])
    D, I = index.search(np.array(pergunta_vec), k=3)
    resultados = [docs[i] for i in I[0]]
    return {"contextos": resultados}
