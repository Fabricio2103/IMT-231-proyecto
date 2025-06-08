import whisper
import subprocess
import os
from pathlib import Path
import time

def transcribir_audio(duracion=10):
    """Grabación y transcripción en un solo paso"""
    # 1. Configuración silenciosa
    model = whisper.load_model("small")
    temp_audio = Path(f"temp_{int(time.time())}.wav")
    
    # 2. Grabar sin output (formato CD quality)
    print("Grabando audio...")
    subprocess.run(
        ["arecord", "-d", str(duracion), "-f", "cd", str(temp_audio)],
        stderr=subprocess.DEVNULL,
        stdout=subprocess.DEVNULL,
        stdin=subprocess.DEVNULL
    )
    print("Grabación finalizada.")
    # 3. Transcribir silenciosamente
    result = model.transcribe(
        str(temp_audio),
        language="es",
        fp16=False,
        verbose=None
    )
    
    # 4. Obtener texto y limpiar
    texto = result.get('text', '')
    os.unlink(temp_audio)
    texto = texto.strip()
    return texto

print(transcribir_audio(15))