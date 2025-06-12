import spacy
import re
from datetime import datetime
from .transcripcion_audio import transcribir_audio

nlp = spacy.load("es_core_news_md")

def extraer_personas(texto):
    doc = nlp(texto)
    personas = [ent.text for ent in doc.ents if ent.label_ == "PER"]
    return personas

def extraer_numeros(texto):
    doc = nlp(texto)
    return [token.text for token in doc if token.like_num]

def extraer_fechas_horas(texto):
    fecha = None
    hora = None

    # Extraer fecha en formato "12 de junio de 2025"
    match_fecha = re.search(r"\d{1,2} de \w+ de \d{4}", texto, re.IGNORECASE)
    if match_fecha:
        fecha = match_fecha.group()

    # Extraer hora como "14:30 PM" o "14:30"
    match_hora = re.search(r"\d{1,2}:\d{2}(?:\s?(AM|PM))?", texto, re.IGNORECASE)
    if match_hora:
        hora = match_hora.group()

    return fecha, hora

def inferir_genero(texto):
    texto = texto.lower()
    if any(p in texto for p in ["la paciente", "doctora", "señora", "doña", "femenino"]):
        return "Femenino"
    elif any(p in texto for p in ["el paciente", "doctor", "señor", "don", "masculino"]):
        return "Masculino"
    return "No especificado"

def procesar_registro(texto):
    personas = extraer_personas(texto)
    numeros = extraer_numeros(texto)
    nombre = personas[0] if personas else ""
    edad = numeros[0] if numeros else ""
    genero = inferir_genero(texto)

    return {
        "nombre": nombre,
        "edad": edad,
        "genero": genero
    }

def procesar_cita(texto):
    """
    Procesa el texto de voz y extrae los datos de cita:
    paciente, medico, fecha y hora.
    Ejemplo de entrada: "agendar cita para maria con el doctor lopez el lunes a las 10"
    """
    texto = texto.lower()

    paciente = ""
    medico = ""
    fecha = ""
    hora = ""

    # Extraer paciente (después de "para")
    match_paciente = re.search(r'para (\w+)', texto)
    if match_paciente:
        paciente = match_paciente.group(1)

    # Extraer médico (después de "con el doctor" o "con la doctora")
    match_medico = re.search(r'con (?:el|la)? ?doctor(?:a)? (\w+)', texto)
    if match_medico:
        medico = match_medico.group(1)

    # Extraer fecha (puede ser una palabra como "lunes")
    dias = ['lunes', 'martes', 'miércoles', 'jueves', 'viernes', 'sábado', 'domingo']
    for dia in dias:
        if dia in texto:
            fecha = dia
            break

    # Extraer hora (número después de "a las")
    match_hora = re.search(r'a las (\d+)', texto)
    if match_hora:
        hora = match_hora.group(1) + ":00"

    return {
        "paciente": paciente,
        "medico": medico,
        "fecha": fecha,
        "hora": hora
    }

def procesar_habitacion(texto):
    persona = extraer_personas(texto)
    numeros = extraer_numeros(texto)
    habitacion = None

    # Detectar el número que probablemente sea la habitación (último número mencionado)
    if numeros:
        habitacion = numeros[-1]

    return {
        "habitacion": habitacion,
        "paciente": persona,
        "estado": "Ocupada"
    }
