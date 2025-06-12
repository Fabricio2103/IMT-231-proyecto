import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import threading
import os

from reconocimiento_de_voz import transcribir_audio, procesar_registro, procesar_habitacion, procesar_cita
from modulos.backend import programar_cita, asignar_habitacion, guardar_paciente

def cargar_imagen(ruta, size=None):
    try:
        img = Image.open(ruta)
        if size:
            img = img.resize(size, Image.LANCZOS)
        return ImageTk.PhotoImage(img)
    except Exception as e:
        messagebox.showwarning("Advertencia", f"No se pudo cargar la imagen: {str(e)}")
        return None

def procesar_comando_voz(accion, campos, frame):
    def tarea():
        try:
            grabando_label.config(text="Grabando...")
            texto = transcribir_audio(5)

            if accion == "registro":
                datos = procesar_registro(texto)
            elif accion == "citas":
                datos = procesar_cita(texto)
            elif accion == "habitaciones":
                datos = procesar_habitacion(texto)
            else:
                datos = {}

            for clave, (etiqueta, widget) in campos.items():
                valor = datos.get(clave, "")
                if isinstance(widget, ttk.Combobox):
                    widget.set(valor)
                else:
                    widget.delete(0, tk.END)
                    widget.insert(0, valor)

            grabando_label.config(text=" Comando procesado correctamente.")
            frame.after(3000, lambda: grabando_label.config(text=""))

        except Exception as e:
            grabando_label.config(text=f" Error: {str(e)}")
            frame.after(4000, lambda: grabando_label.config(text=""))

    grabando_label = ttk.Label(frame, text="", font=('Arial', 10, 'italic'), foreground='blue')
    grabando_label.grid(row=99, column=0, columnspan=2, pady=5)
    threading.Thread(target=tarea, daemon=True).start()

def crear_ventana(titulo, fondo_img_path, construir_funcion):
    ventana = tk.Toplevel(root)
    ventana.title(titulo)
    ventana.geometry("800x600")
    ventana.resizable(False, False)

    ruta_fondo = os.path.join("imagenes", fondo_img_path)
    fondo = cargar_imagen(ruta_fondo, (800, 600))
    if fondo:
        fondo_label = tk.Label(ventana, image=fondo)
        fondo_label.image = fondo
        fondo_label.place(x=0, y=0, relwidth=1, relheight=1)

    marco = ttk.Frame(ventana, padding=20, style='Card.TFrame')
    marco.place(relx=0.5, rely=0.5, anchor='center')

    construir_funcion(marco, ventana)

def construir_registro(frame, ventana):
    campos = {}
    ttk.Label(frame, text="Registro de Pacientes", font=('Arial', 14, 'bold')).grid(row=0, column=0, columnspan=2, pady=10)
    ttk.Label(frame, text="Ejemplo: registrar paciente Juan Pérez, 34 años, masculino", font=('Arial', 9, 'italic')).grid(row=1, column=0, columnspan=2)

    etiquetas = ["nombre", "edad", "genero"]
    textos = ["Nombre:", "Edad:", "Género:"]
    widgets = [tk.Entry(frame, width=30), tk.Entry(frame, width=10), ttk.Combobox(frame, values=["Masculino", "Femenino", "Otro"], width=15)]

    for i, (etq, texto, widget) in enumerate(zip(etiquetas, textos, widgets)):
        ttk.Label(frame, text=texto).grid(row=i+2, column=0, sticky='e', padx=5, pady=5)
        widget.grid(row=i+2, column=1, sticky='w', padx=5, pady=5)
        campos[etq] = (texto, widget)

    def guardar_y_limpiar():
        guardar_paciente({k: w[1].get() for k, w in campos.items()})
        for _, widget in campos.values():
            widget.delete(0, tk.END) if isinstance(widget, tk.Entry) else widget.set("")

    ttk.Button(frame, text=" Voz", command=lambda: procesar_comando_voz("registro", campos, frame)).grid(row=5, column=0, pady=10)
    ttk.Button(frame, text=" Guardar", command=guardar_y_limpiar).grid(row=5, column=1, pady=10)
    ttk.Button(frame, text=" Volver", command=ventana.destroy).grid(row=6, column=0, columnspan=2, pady=10)

def construir_citas(frame, ventana):
    campos = {}
    ttk.Label(frame, text="Programación de Citas", font=('Arial', 14, 'bold')).grid(row=0, column=0, columnspan=2, pady=10)
    ttk.Label(frame, text="Ejemplo: agendar cita para María con el doctor López el lunes a las 10", font=('Arial', 9, 'italic')).grid(row=1, column=0, columnspan=2)

    etiquetas = ["paciente", "medico", "fecha", "hora"]
    textos = ["Paciente:", "Médico:", "Fecha:", "Hora:"]
    entradas = [tk.Entry(frame, width=30) for _ in etiquetas]

    for i, (etq, texto, widget) in enumerate(zip(etiquetas, textos, entradas)):
        ttk.Label(frame, text=texto).grid(row=i+2, column=0, sticky='e', padx=5, pady=5)
        widget.grid(row=i+2, column=1, sticky='w', padx=5, pady=5)
        campos[etq] = (texto, widget)

    def programar_y_limpiar():
        programar_cita({k: w[1].get() for k, w in campos.items()})
        for _, widget in campos.values():
            widget.delete(0, tk.END)

    ttk.Button(frame, text=" Voz", command=lambda: procesar_comando_voz("citas", campos, frame)).grid(row=6, column=0, pady=10)
    ttk.Button(frame, text=" Programar", command=programar_y_limpiar).grid(row=6, column=1, pady=10)
    ttk.Button(frame, text=" Volver", command=ventana.destroy).grid(row=7, column=0, columnspan=2, pady=10)

def construir_habitaciones(frame, ventana):
    campos = {}
    ttk.Label(frame, text="Asignación de Habitaciones", font=('Arial', 14, 'bold')).grid(row=0, column=0, columnspan=2, pady=10)
    ttk.Label(frame, text="Ejemplo: asignar habitación 204 a Carlos", font=('Arial', 9, 'italic')).grid(row=1, column=0, columnspan=2)

    etiquetas = ["paciente", "habitacion"]
    textos = ["Paciente:", "Habitación:"]
    entradas = [tk.Entry(frame, width=30) for _ in etiquetas]

    for i, (etq, texto, widget) in enumerate(zip(etiquetas, textos, entradas)):
        ttk.Label(frame, text=texto).grid(row=i+2, column=0, sticky='e', padx=5, pady=5)
        widget.grid(row=i+2, column=1, sticky='w', padx=5, pady=5)
        campos[etq] = (texto, widget)

    def asignar_y_limpiar():
        asignar_habitacion({k: w[1].get() for k, w in campos.items()})
        for _, widget in campos.values():
            widget.delete(0, tk.END)

    ttk.Button(frame, text=" Voz", command=lambda: procesar_comando_voz("habitaciones", campos, frame)).grid(row=4, column=0, pady=10)
    ttk.Button(frame, text=" Asignar", command=asignar_y_limpiar).grid(row=4, column=1, pady=10)
    ttk.Button(frame, text=" Volver", command=ventana.destroy).grid(row=5, column=0, columnspan=2, pady=10)

root = tk.Tk()
root.title("Sistema Hospitalario Inteligente")
root.geometry("1200x800")
root.resizable(False, False)

ruta_fondo_principal = os.path.join("imagenes", "fondo_principal.png")
fondo_principal = cargar_imagen(ruta_fondo_principal, (1200, 800))
if fondo_principal:
    fondo_label = tk.Label(root, image=fondo_principal)
    fondo_label.place(x=0, y=0, relwidth=1, relheight=1)

style = ttk.Style()
style.configure('TFrame', background='#ffffff')
style.configure('TLabel', background='#ffffff', font=('Arial', 11, 'bold'))
style.configure('TButton', font=('Arial', 11, 'bold'), padding=6)
style.configure('Card.TFrame', background='#ffffff', relief='raised', borderwidth=1)

frame_main = ttk.Frame(root, padding=20, style='Card.TFrame')
frame_main.place(relx=0.5, rely=0.5, anchor='center')

ttk.Label(frame_main, text="Sistema Hospitalario Inteligente", font=('Arial', 16, 'bold')).pack(pady=20)

botones = [
    ("Registro de Pacientes", lambda: crear_ventana("Registro de Pacientes", "fondo_registro.png", construir_registro)),
    ("Gestión de Citas", lambda: crear_ventana("Programar Cita", "fondo_citas.png", construir_citas)),
    ("Asignación de Habitaciones", lambda: crear_ventana("Asignar Habitación", "fondo_habitaciones.png", construir_habitaciones))
]

for texto, comando in botones:
    ttk.Button(frame_main, text=texto, command=comando, width=30).pack(pady=10)

# ➕ Botón adicional para comando por voz
ttk.Button(frame_main, text="🎤 Comando por Voz", command=lambda: comando_por_voz_desde_principal(frame_main), width=30).pack(pady=20)

def comando_por_voz_desde_principal(frame):
    def tarea():
        try:
            mensaje_label.config(text="🎙️ Escuchando comando...")
            texto = transcribir_audio(5).lower()

            if any(p in texto for p in ["registrar", "registro", "paciente"]):
                crear_ventana("Registro de Pacientes", "fondo_registro.png", construir_registro)
            elif any(p in texto for p in ["cita", "doctor", "médico"]):
                crear_ventana("Programar Cita", "fondo_citas.png", construir_citas)
            elif any(p in texto for p in ["habitación", "asignar"]):
                crear_ventana("Asignar Habitación", "fondo_habitaciones.png", construir_habitaciones)
            else:
                mensaje_label.config(text="❌ No se reconoció la acción. Intenta de nuevo.")
                frame.after(4000, lambda: mensaje_label.config(text=""))
                return

            mensaje_label.config(text="✅ Comando procesado correctamente.")
            frame.after(3000, lambda: mensaje_label.config(text=""))

        except Exception as e:
            mensaje_label.config(text=f"❌ Error: {str(e)}")
            frame.after(4000, lambda: mensaje_label.config(text=""))

    mensaje_label = ttk.Label(frame, text="", font=('Arial', 10, 'italic'), foreground='blue')
    mensaje_label.pack()
    threading.Thread(target=tarea, daemon=True).start()

root.mainloop()
