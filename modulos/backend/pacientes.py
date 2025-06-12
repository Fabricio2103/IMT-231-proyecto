from modulos.utils.excel import guardar_en_excel, crear_archivo_si_no_existe

ARCHIVO = "pacientes.xlsx"
ENCABEZADOS = ["Nombre", "Edad", "Género"]

crear_archivo_si_no_existe(ARCHIVO, ENCABEZADOS)

def guardar_paciente(datos):
    """Guarda paciente usando diccionario"""
    datos_lista = [
        datos["nombre"],
        datos["edad"],
        datos["genero"],
    ]
    guardar_en_excel(datos_lista, ARCHIVO)