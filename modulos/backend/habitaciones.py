from modulos.utils.excel import guardar_en_excel, crear_archivo_si_no_existe

ARCHIVO = "habitaciones.xlsx"
ENCABEZADOS = ["Número", "Paciente Asignado", "Estado"]

crear_archivo_si_no_existe(ARCHIVO, ENCABEZADOS)

def asignar_habitacion(numero, paciente, estado="Ocupada"):
    datos = [numero, paciente, estado]
    guardar_en_excel(datos, ARCHIVO)