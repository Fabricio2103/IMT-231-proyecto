import spacy
import re
from datetime import datetime
from .transcripcion_audio import transcribir_audio

nlp = spacy.load("es_core_news_md")
def extraer_personas(texto):
    doc = nlp(texto)
    for ent in doc.ents:
        if ent.label_ == "PER":
            return ent.text
    return None


def extraer_numeros(texto):
    doc = nlp(texto)
    numeros = []
    for token in doc:
        if token.like_num and len(token.text) > 0:
            numeros.append(token.text)
    return numeros


def extraer_fechas_horas(texto):
    patron_fecha = re.search(r"\d{1,2} de \w+ de \d{4}", texto)
    patron_hora = re.search(r"\d{1,2}:\d{2} (AM|PM)", texto, re.IGNORECASE)
    fecha = patron_fecha.group() if patron_fecha else None
    hora = patron_hora.group() if patron_hora else None
    return fecha, hora


def inferir_genero(texto):
    texto = texto.lower()
    if "la paciente" in texto or "doctora" in texto or "señora" in texto or "doña" in texto:
        return "Femenino"
    elif "el paciente" in texto or "doctor" in texto or "señor" in texto or "don" in texto:
        return "Masculino"
    else:
        return "No especificado"


def procesar_registro(texto):
    persona = extraer_personas(texto)
    numeros = extraer_numeros(texto)
    edad = numeros[0] if len(numeros) > 0 else None
    genero = inferir_genero(texto)
    return {
        "nombre": persona,
        "edad": edad,
        "genero": genero,
    }


def procesar_habitacion(texto):
    persona = extraer_personas(texto)
    numeros = extraer_numeros(texto)
    habitacion = numeros[1] if len(numeros) > 1 else None  # evita confundir con edad
    estado = "Ocupada"
    return {
        "habitacion": habitacion,
        "paciente": persona,
        "estado": estado
    }


def procesar_cita(texto):
    fecha, hora = extraer_fechas_horas(texto)
    doc = nlp(texto)
    personas = [ent.text for ent in doc.ents if ent.label_ == "PER"]
    medico = None
    paciente = None
    for p in personas:
        p_lower = p.lower()
        if 'dr.' in p_lower or 'dra.' in p_lower or "doctora" in texto.lower() or "doctor" in texto.lower():
            medico = p
        else:
            paciente = p
    return {
        "fecha": fecha,
        "hora": hora,
        "paciente": paciente,
        "medico": medico
    }
