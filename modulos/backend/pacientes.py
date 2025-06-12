from modulos.utils.excel import guardar_en_excel, crear_archivo_si_no_existe

ARCHIVO = "pacientes.xlsx"
ENCABEZADOS = ["Nombre", "Edad", "Género", "Historial Médico"]

crear_archivo_si_no_existe(ARCHIVO, ENCABEZADOS)

def guardar_paciente(nombre, edad, genero, historial):
    datos = [nombre, edad, genero, historial]
    guardar_en_excel(datos, ARCHIVO)