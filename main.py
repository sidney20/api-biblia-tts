import os
from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel
from gtts import gTTS
import uuid

app = FastAPI()

# 🔐 API KEY vem do Railway
API_KEY = os.getenv("API_KEY")

class TextoBiblia(BaseModel):
    texto: str

@app.get("/")
def home():
    return {"status": "API Bíblia TTS rodando 🙏"}

@app.post("/gerar-audio")
def gerar_audio(
    dados: TextoBiblia,
    x_api_key: str = Header(None)
):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="API Key inválida")

    nome_arquivo = f"audio_{uuid.uuid4().hex}.mp3"

    tts = gTTS(text=dados.texto, lang="pt")
    tts.save(nome_arquivo)

    return {
        "status": "ok",
        "arquivo": nome_arquivo
    }
