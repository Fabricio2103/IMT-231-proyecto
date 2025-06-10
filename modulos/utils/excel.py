import openpyxl
import os

def crear_archivo_si_no_existe(nombre_archivo, encabezados):
    if not os.path.exists(nombre_archivo):
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.append(encabezados)
        wb.save(nombre_archivo)