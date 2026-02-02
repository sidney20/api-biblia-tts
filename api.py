from fastapi import FastAPI
from pydantic import BaseModel
from TTS.api import TTS
import uuid

app = FastAPI()

tts = TTS(
    model_name="tts_models/multilingual/multi-dataset/xtts_v2",
    gpu=False
)

class TextoBiblia(BaseModel):
    texto: str

@app.post("/gerar-audio")
def gerar_audio(dados: TextoBiblia):
    nome_arquivo = f"audio_{uuid.uuid4()}.wav"

    tts.tts_to_file(
        text=dados.texto,
        speaker_wav="minha_voz.wav",
        language="pt",
        file_path=nome_arquivo
    )

    return {
        "status": "ok",
        "audio": nome_arquivo
    }

