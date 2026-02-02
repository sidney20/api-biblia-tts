import os
from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel
from TTS.api import TTS
import uuid

app = FastAPI()

# 🔐 PEGA A CHAVE DO AMBIENTE (Railway)
API_KEY = os.getenv("API_KEY")

class TextoBiblia(BaseModel):
    texto: str

tts = TTS(
    model_name="tts_models/multilingual/multi-dataset/xtts_v2",
    gpu=False
)

@app.post("/gerar-audio")
def gerar_audio(
    dados: TextoBiblia,
    x_api_key: str = Header(None, alias="x-api-key")
):
    if x_api_key != API_KEY:
        raise HTTPException(
            status_code=401,
            detail="API Key inválida"
        )

    nome_arquivo = f"audio_{uuid.uuid4().hex}.wav"

    tts.tts_to_file(
        text=dados.texto,
        language="pt",
        file_path=nome_arquivo
    )

    return {
        "status": "ok",
        "arquivo": nome_arquivo
    }
