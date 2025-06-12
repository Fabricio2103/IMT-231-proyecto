import whisper
import subprocess
import os
from pathlib import Path
import time

def transcribir_audio(duracion=20):
    """Grabacion y transcripción en un solo paso"""
    # Cargar modelo una vez
    model = whisper.load_model("small")
    temp_audio = Path(f"temp_{int(time.time())}.wav")
    
    # Grabar audio sin mostrar salida en consola
    print("Grabando audio...")
    subprocess.run(
        ["arecord", "-d", str(duracion), "-f", "cd", str(temp_audio)],
        stderr=subprocess.DEVNULL,
        stdout=subprocess.DEVNULL,
        stdin=subprocess.DEVNULL
    )
    print("Grabación finalizada.")
    
    # Transcribir el audio
    result = model.transcribe(str(temp_audio), language="es", fp16=False, verbose=None)
    texto = result.get('text', '').strip()
    
    # Eliminar archivo temporal
    os.unlink(temp_audio)
    
    return texto
