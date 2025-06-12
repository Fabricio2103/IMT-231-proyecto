from modulos.utils.excel import guardar_en_excel, crear_archivo_si_no_existe

ARCHIVO = "pacientes.xlsx"
ENCABEZADOS = ["Nombre", "Edad", "Género", "Historial Médico"]

crear_archivo_si_no_existe(ARCHIVO, ENCABEZADOS)

def guardar_paciente(datos):
    """Guarda paciente usando diccionario"""
    datos_lista = [
        datos["nombre"],
        datos["edad"],
        datos["genero"],
        datos.get("historial", "")  # Usa .get() por si no existe
    ]
    guardar_en_excel(datos_lista, ARCHIVO)