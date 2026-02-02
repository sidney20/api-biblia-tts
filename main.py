import os
import uuid
from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel
from TTS.api import TTS

app = FastAPI(
    title="API Bíblia Falada",
    description="Gera áudio da Bíblia em português usando TTS",
    version="1.0.0"
)

# 🔐 API KEY VEM DO AMBIENTE (Railway / Render)
API_KEY = os.getenv("API_KEY")

# ❗ Segurança: se esquecer de configurar no servidor
if not API_KEY:
    raise RuntimeError("API_KEY não configurada nas variáveis de ambiente")

# 📘 Modelo do texto recebido
class TextoBiblia(BaseModel):
    texto: str

# 🔊 Carrega o modelo TTS UMA ÚNICA VEZ
tts = TTS(
    model_name="tts_models/multilingual/multi-dataset/xtts_v2",
    gpu=False
)

@app.post("/gerar-audio")
def gerar_audio(
    dados: TextoBiblia,
    x_api_key: str = Header(None)
):
    # 🔐 Validação da API Key
    if x_api_key != API_KEY:
        raise HTTPException(
            status_code=401,
            detail="API Key inválida"
        )

    # 🧾 Nome único do arquivo
    nome_arquivo = f"audio_{uuid.uuid4().hex}.wav"

    # 🔊 Gera o áudio
    tts.tts_to_file(
        text=dados.texto,
        language="pt",
        file_path=nome_arquivo
    )

    return {
        "status": "ok",
        "arquivo": nome_arquivo,
        "mensagem": "Áudio gerado com sucesso"
    }
