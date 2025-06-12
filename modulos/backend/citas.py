from modulos.utils.excel import guardar_en_excel, crear_archivo_si_no_existe

ARCHIVO = "citas.xlsx"
ENCABEZADOS = ["Fecha", "Hora", "Paciente", "Médico"]

crear_archivo_si_no_existe(ARCHIVO, ENCABEZADOS)

def programar_cita(datos):
    """Programa cita usando diccionario"""
    datos_lista = [
        datos["fecha"],
        datos["hora"],
        datos["paciente"],
        datos["medico"]
    ]
    guardar_en_excel(datos_lista, ARCHIVO)