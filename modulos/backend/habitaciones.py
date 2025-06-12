from modulos.utils.excel import guardar_en_excel, crear_archivo_si_no_existe

ARCHIVO = "habitaciones.xlsx"
ENCABEZADOS = ["Paciente", "Habitacion"]

crear_archivo_si_no_existe(ARCHIVO, ENCABEZADOS)

def asignar_habitacion(datos):
    """Asigna habitación usando diccionario"""
    datos_lista = [
        datos["paciente"],
        datos["habitacion"],
    ]
    guardar_en_excel(datos_lista, ARCHIVO)