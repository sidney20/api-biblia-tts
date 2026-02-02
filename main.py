from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel
from TTS.api import TTS
import uuid

app = FastAPI()

# 🔐 SUA CHAVE SECRETA
API_KEY = "minha_chave_biblia_123"

# 📘 Texto que vem do app
class TextoBiblia(BaseModel):
    texto: str

# 🔊 Carrega o TTS (uma vez só)
tts = TTS(
    model_name="tts_models/multilingual/multi-dataset/xtts_v2",
    gpu=False
)

@app.post("/gerar-audio")
def gerar_audio(
    dados: TextoBiblia,
    x_api_key: str = Header(None)
):
    # 🔐 Confere a chave
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
