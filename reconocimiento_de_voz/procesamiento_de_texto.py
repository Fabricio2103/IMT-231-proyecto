import spacy
from datetime import datetime
from transcripcion_audio import transcribir_audio
# cargar el modelo de lenguaje para español
nlp = spacy.load("es_core_news_md")
texto= transcribir_audio(15)
def extraer_personas(texto):
    # esta funcion saca nombres de personas pero a veces puede fallar si el texto esta muy raro
    doc = nlp(texto)
    persona = None
    for ent in doc.ents:
        if ent.label_ == "PER":
            persona = ent.text
            break
    return persona

def extraer_numeros(texto):
    # esta funcion busca numeros en el texto como edad documento o habitacion pero no sabe que tipo es cada uno
    doc = nlp(texto)
    numeros = []
    for token in doc:
        if token.like_num and len(token.text) > 2:
            numeros.append(token.text)
    return numeros

def extraer_fechas_horas(texto):
    # aqui se buscan las fechas y horas si hay sino se retorna None
    doc = nlp(texto)
    fecha = None
    hora = None
    for ent in doc.ents:
        if ent.label_ == "DATE" and not fecha:
            fecha = ent.text
        elif ent.label_ == "TIME" and not hora:
            hora = ent.text
    return fecha, hora
def inferir_genero(texto):
    # esta funcion trata de ver si el genero es masculino o femenino segun palabras clave
    texto_lower = texto.lower()
    if "la paciente" in texto_lower or "señora" in texto_lower or "doña" in texto_lower:
        return "Femenino"
    elif "el paciente" in texto_lower or "señor" in texto_lower or "don" in texto_lower:
        return "Masculino"
    else:
        return "No especificado"

def procesar_registro(texto):
    # procesa el registro del paciente sacando nombre edad y genero pero no documento
    persona = extraer_personas(texto)
    numeros = extraer_numeros(texto)
    edad = numeros[0] if len(numeros) > 0 else None
    genero = inferir_genero(texto)
    historial = ""  # se deja vacio para completar luego
    return [persona, edad, genero, historial]  # orden ajustado

def procesar_habitacion(texto):
    # busca numero de habitacion y nombre del paciente para asignar
    persona = extraer_personas(texto)
    numeros = extraer_numeros(texto)
    habitacion = numeros[0] if numeros else None
    estado = "Ocupada"
    return [habitacion, persona, estado]  # orden ajustado

def procesar_cita(texto):
    # obtiene fecha hora medico y paciente si hay sino deja vacio
    fecha, hora = extraer_fechas_horas(texto)
    doc = nlp(texto)
    personas = [ent.text for ent in doc.ents if ent.label_ == "PER"]
    medico = None
    paciente = None
    for p in personas:
        p_lower = p.lower()
        if 'dr.' in p_lower or 'dra.' in p_lower:
            medico = p
        else:
            paciente = p
    return [fecha, hora, paciente, medico]  # orden ajustado
