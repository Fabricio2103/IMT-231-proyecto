# Proyecto Programacion superior 

## 🏥 Descripción del Proyecto: Sistema de Gestión Hospitalaria con Integración de Whisper

Este proyecto consiste en el desarrollo de un **Sistema de Gestión Hospitalaria** en lenguaje **Python**, que incorpora una funcionalidad avanzada de reconocimiento de voz utilizando el modelo **Whisper** de OpenAI. El objetivo principal es brindar una solución moderna y accesible para la administración eficiente de recursos hospitalarios, permitiendo a los usuarios interactuar con el sistema tanto mediante entrada por teclado como por comandos de voz.

### 🎯 Objetivos

* Automatizar tareas comunes dentro de un hospital, como el **registro de pacientes, doctores y citas médicas**.
* **Reducir el uso del teclado** mediante el reconocimiento de voz para facilitar la accesibilidad, especialmente para personal médico con movilidad limitada o manos ocupadas.

### 🧠 ¿Qué es Whisper?

[Whisper](https://github.com/openai/whisper) es un modelo de reconocimiento automático de voz de código abierto creado por OpenAI. Permite transcribir audio a texto en múltiples idiomas con alta precisión. En este proyecto, se utiliza Whisper para **convertir instrucciones habladas en comandos de texto** que el sistema hospitalario puede interpretar.

### 🔧 Funcionalidades del sistema
* **Registro de pacientes**:datos personales, historial médico
* **Asignación de habitaciones o camas**
* **Asignación de pacientes a médicos**
* **Programación de citas médicas**: fecha, hora, médico, paciente
* **Modificación o cancelación de citas**
* **Reconocimiento de voz (Whisper)**:

  * Registrar pacientes dictando sus datos.
* **Interfaz por consola** amigable y dinámica.

### 🔌 Requisitos técnicos

* Lenguaje: Python
* Sistema operativo: Linux
* Whisper:
  * Python 3.9+
  * Dependencias: `openai-whisper`, `ffmpeg`, `torch`
  * Entrada: archivos `.wav` generados por grabación o micrófono
* Librerías externas para integración:

  * Comunicación entre C y Python (uso de `system()` o sockets)



## Authors

- [Marcelo](https://github.com/Fabricio2103)
- [Fabricio](https://github.com/Fabricio2103)
- [Mirko](https://github.com/Fabricio2103)
