from modulos.utils.excel import guardar_en_excel, crear_archivo_si_no_existe

ARCHIVO = "citas.xlsx"
ENCABEZADOS = ["Fecha", "Hora", "Paciente", "Médico"]

crear_archivo_si_no_existe(ARCHIVO, ENCABEZADOS)

def programar_cita(fecha, hora, paciente, medico):
    datos = [fecha, hora, paciente, medico]
    guardar_en_excel(datos, ARCHIVO)