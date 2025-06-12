from modulos.utils.excel import guardar_en_excel, crear_archivo_si_no_existe

ARCHIVO = "habitaciones.xlsx"
ENCABEZADOS = ["Número", "Paciente Asignado", "Estado"]

crear_archivo_si_no_existe(ARCHIVO, ENCABEZADOS)

def asignar_habitacion(datos):
    """Asigna habitación usando diccionario"""
    datos_lista = [
        datos["numero"],
        datos["paciente"],
        datos.get("estado", "Ocupada")  # Valor por defecto
    ]
    guardar_en_excel(datos_lista, ARCHIVO)