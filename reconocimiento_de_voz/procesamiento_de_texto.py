import spacy
from datetime import datetime

# cargar el modelo de lenguaje para español
nlp = spacy.load("es_core_news_md")

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

def procesar_registro(texto):
    # procesa los datos basicos del paciente como nombre edad y documento
    persona = extraer_personas(texto)
    numeros = extraer_numeros(texto)
    edad = numeros[0] if len(numeros) > 0 else None
    documento = numeros[1] if len(numeros) > 1 else None
    return [persona, edad, documento]

def procesar_habitacion(texto):
    # saca el numero de la habitacion y el nombre del paciente si se puede
    persona = extraer_personas(texto)
    numeros = extraer_numeros(texto)
    habitacion = numeros[0] if numeros else None
    return [habitacion, persona]

def procesar_cita(texto):
    # busca quien es el medico y el paciente y cuando es la cita
    fecha, hora = extraer_fechas_horas(texto)
    doc = nlp(texto)
    personas = [ent.text for ent in doc.ents if ent.label_ == "PER"]
    medico = None
    paciente = None
    for p in personas:
        if 'dr.' in p.lower() or 'dra.' in p.lower():
            medico = p
        else:
            paciente = p
    return [fecha, hora, medico, paciente]

def procesar_modificacion(texto):
    # aqui se revisa si la cita se va cancelar o modificar y quien es el doctor y el paciente
    accion = "cancelar" if "cancelar" in texto.lower() else "modificar"
    doc = nlp(texto)
    personas = [ent.text for ent in doc.ents if ent.label_ == "PER"]
    medico = None
    paciente = None
    for p in personas:
        if 'dr.' in p.lower() or 'dra.' in p.lower():
            medico = p
        else:
            paciente = p
    return [accion, medico, paciente]

