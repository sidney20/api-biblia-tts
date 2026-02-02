from TTS.api import TTS

tts = TTS(
    model_name="tts_models/multilingual/multi-dataset/xtts_v2",
    gpu=False
)

tts.tts_to_file(
    text="Olá, esta é minha própria voz falando em português do Brasil.",
    speaker_wav="minha_voz.wav",
    language="pt",
    file_path="saida_ptbr.wav"
)

print("Áudio PT-BR gerado com sucesso 🇧🇷🔥")
