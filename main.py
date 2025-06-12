import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import threading
import os

# Importaciones de tus módulos (asegúrate que existan)
from reconocimiento_de_voz import transcribir_audio, procesar_registro, procesar_habitacion, procesar_cita
from modulos.backend import programar_cita, asignar_habitacion, guardar_paciente

# --- Configuración inicial ---
root = tk.Tk()
root.title("Sistema Hospitalario Inteligente")
root.geometry("1200x800")
root.configure(bg='#f8f8f8')
root.resizable(False, False)

# --- Variables globales ---
pacientes = ["Juan Pérez", "María Gómez", "Carlos López"]  # Ejemplo, reemplaza con datos reales

# --- Carga de imágenes ---
def cargar_imagen(ruta_imagen, tamaño=None):
    """Carga y redimensiona una imagen con manejo de errores"""
    try:
        if not os.path.exists(ruta_imagen):
            raise FileNotFoundError(f"Archivo no encontrado: {ruta_imagen}")
        
        img = Image.open(ruta_imagen)
        if tamaño:
            img = img.resize(tamaño, Image.LANCZOS)
        return ImageTk.PhotoImage(img)
    except Exception as e:
        messagebox.showwarning("Advertencia", f"No se pudo cargar la imagen: {str(e)}")
        return None

# Cargar imagen de fondo principal
fondo_img = cargar_imagen("Registro de paciente.png", (1200, 800))

# --- Configuración de fondo ---
if fondo_img:
    fondo_label = tk.Label(root, image=fondo_img)
    fondo_label.image = fondo_img  # Mantener referencia
    fondo_label.place(x=0, y=0, relwidth=1, relheight=1)
else:
    # Fondo alternativo si la imagen falla
    root.configure(bg='#e6f2ff')

# --- Estilo moderno ---
style = ttk.Style()
style.theme_use('default')

# Configuraciones de estilo
style.configure('TFrame', background='#ffffff')
style.configure('TLabel', background='#ffffff', font=('Arial', 11))
style.configure('TButton', font=('Arial', 11), padding=8)
style.map('TButton', 
          background=[('active', '#45a049')],
          foreground=[('active', 'white')])

# --- Funciones para ventanas específicas ---
def configurar_ventana_registro(marco):
    """Interfaz para registro de pacientes"""
    ttk.Label(marco, text="Registro de Pacientes", font=('Arial', 14)).grid(row=0, columnspan=2, pady=10)
    
    campos = [
        ("Nombre:", ttk.Entry(marco, width=30)),
        ("Edad:", ttk.Entry(marco, width=10)),
        ("Género:", ttk.Combobox(marco, values=["Masculino", "Femenino", "Otro"], width=15))
    ]
    
    for i, (texto, widget) in enumerate(campos, start=1):
        ttk.Label(marco, text=texto).grid(row=i, column=0, padx=5, pady=5, sticky='e')
        widget.grid(row=i, column=1, padx=5, pady=5, sticky='w')
    
    ttk.Button(marco, text="🎤 Usar Voz", 
              command=lambda: procesar_comando_voz("registro", campos)).grid(row=4, column=0, pady=10)
    ttk.Button(marco, text="💾 Guardar", 
              command=lambda: guardar_paciente({
                  'nombre': campos[0][1].get(),
                  'edad': campos[1][1].get(),
                  'genero': campos[2][1].get()
              })).grid(row=4, column=1, pady=10)

def configurar_ventana_citas(marco):
    """Interfaz para programación de citas"""
    ttk.Label(marco, text="Programación de Citas", font=('Arial', 14)).grid(row=0, columnspan=2, pady=10)
    
    campos = [
        ("Paciente:", ttk.Combobox(marco, values=pacientes, width=25)),
        ("Médico:", ttk.Combobox(marco, values=["Dr. Pérez", "Dra. Gómez"], width=25)),
        ("Fecha (dd/mm/aaaa):", ttk.Entry(marco, width=15)),
        ("Hora:", ttk.Combobox(marco, values=["09:00", "10:00", "11:00", "14:00", "15:00"], width=10))
    ]
    
    for i, (texto, widget) in enumerate(campos, start=1):
        ttk.Label(marco, text=texto).grid(row=i, column=0, padx=5, pady=5, sticky='e')
        widget.grid(row=i, column=1, padx=5, pady=5, sticky='w')
    
    ttk.Button(marco, text="🎤 Usar Voz", 
              command=lambda: procesar_comando_voz("citas", campos)).grid(row=5, column=0, pady=10)
    ttk.Button(marco, text="📅 Programar", 
              command=lambda: programar_cita({
                  'paciente': campos[0][1].get(),
                  'medico': campos[1][1].get(),
                  'fecha': campos[2][1].get(),
                  'hora': campos[3][1].get()
              })).grid(row=5, column=1, pady=10)

def configurar_ventana_habitaciones(marco):
    """Interfaz para asignación de habitaciones"""
    ttk.Label(marco, text="Asignación de Habitaciones", font=('Arial', 14)).grid(row=0, columnspan=2, pady=10)
    
    campos = [
        ("Paciente:", ttk.Combobox(marco, values=pacientes, width=25)),
        ("Habitación:", ttk.Combobox(marco, values=["101", "102", "201", "202"], width=10))
    ]
    
    for i, (texto, widget) in enumerate(campos, start=1):
        ttk.Label(marco, text=texto).grid(row=i, column=0, padx=5, pady=5, sticky='e')
        widget.grid(row=i, column=1, padx=5, pady=5, sticky='w')
    
    ttk.Button(marco, text="🎤 Usar Voz", 
              command=lambda: procesar_comando_voz("habitaciones", campos)).grid(row=3, column=0, pady=10)
    ttk.Button(marco, text="🛏️ Asignar", 
              command=lambda: asignar_habitacion({
                  'paciente': campos[0][1].get(),
                  'habitacion': campos[1][1].get()
              })).grid(row=3, column=1, pady=10)

# --- Procesamiento de comandos de voz ---
def procesar_comando_voz(accion, campos=None):
    def tarea():
        try:
            texto = transcribir_audio(5)  # Grabar 5 segundos
            
            if accion == "registro" and campos:
                datos = procesar_registro(texto)
                campos[0][1].delete(0, tk.END)
                campos[0][1].insert(0, datos.get('nombre', ''))
                campos[1][1].delete(0, tk.END)
                campos[1][1].insert(0, datos.get('edad', ''))
                
            elif accion == "citas" and campos:
                datos = procesar_cita(texto)
                campos[0][1].delete(0, tk.END)
                campos[0][1].insert(0, datos.get('paciente', ''))
                campos[1][1].delete(0, tk.END)
                campos[1][1].insert(0, datos.get('medico', ''))
                
            elif accion == "habitaciones" and campos:
                datos = procesar_habitacion(texto)
                campos[0][1].delete(0, tk.END)
                campos[0][1].insert(0, datos.get('paciente', ''))
                campos[1][1].delete(0, tk.END)
                campos[1][1].insert(0, datos.get('habitacion', ''))
                
            messagebox.showinfo("Éxito", "Comando de voz procesado")
        except Exception as e:
            messagebox.showerror("Error", f"Error en reconocimiento: {str(e)}")
    
    threading.Thread(target=tarea, daemon=True).start()

# --- Función para abrir ventanas emergentes ---
def abrir_ventana(tipo):
    ventana = tk.Toplevel(root)
    ventana.title(f"Gestor de {tipo.capitalize()}")
    ventana.geometry("800x600")
    ventana.resizable(False, False)
    
    # Marco principal
    marco = ttk.Frame(ventana, padding=20)
    marco.place(relx=0.5, rely=0.5, anchor='center')

    if tipo == "registro":
        configurar_ventana_registro(marco)
    elif tipo == "citas":
        configurar_ventana_citas(marco)
    elif tipo == "habitaciones":
        configurar_ventana_habitaciones(marco)

# --- Interfaz principal ---
marco_principal = ttk.Frame(root, padding=20)
marco_principal.place(relx=0.5, rely=0.5, anchor='center')

ttk.Label(marco_principal, text="Sistema Hospitalario", font=('Arial', 16)).pack(pady=20)

botones_principales = [
    ("Registro de Pacientes", lambda: abrir_ventana("registro")),
    ("Gestión de Citas", lambda: abrir_ventana("citas")),
    ("Asignación de Habitaciones", lambda: abrir_ventana("habitaciones"))
]

for texto, comando in botones_principales:
    ttk.Button(marco_principal, text=texto, command=comando, width=25).pack(pady=10)

# --- Ejecutar aplicación ---
if __name__ == "__main__":
    root.mainloop()