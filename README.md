<!-- Encabezado institucional -->
<p align="left">
  <img src="FotosReadME/Logo.png" alt="ING | Facultad de Ingeniería" height="120" style="vertical-align:middle; margin-right:12px;">
  <img src="FotosReadME/Facultad.png"     alt="Logo UVG"                        height="64" style="vertical-align:middle;">
</p>


# Diseño e implementación de un módulo de reconocimiento de voz para el control de sistemas robóticos

**Fase V**

**Oscar Fernando López Godínez**  
Departamento de Ingeniería Mecatrónica  
Universidad del Valle de Guatemala

---

## Descripción

Este trabajo de graduación desarrolla e integra un módulo de reconocimiento de voz para el control articular seguro de un manipulador myCobot 280 M5. El sistema convierte en tiempo real enunciados verbales en órdenes ejecutables, combinando: (i) transcripción continua de habla (STT), (ii) un analizador sintáctico-semántico que normaliza el lenguaje, resuelve números/órdenes y detecta modo relativo/absoluto, y (iii) un controlador con programación defensiva que verifica límites por junta antes de ejecutar. Todo se visualiza en una GUI que muestra la transcripción, la intención interpretada y el estado de ejecución, facilitando trazabilidad.

La motivación es simplificar la interacción humano-robot frente a interfaces tradicionales. El sistema se validó experimentalmente en condiciones realistas (ruido ambiente moderado, distintas distancias al micrófono), mostrando ejecuciones consistentes, rechazos seguros ante órdenes fuera de rango y cambio de modo por voz (absoluto/relativo) con confirmación. Los resultados evidencian la viabilidad del enfoque para control articular basado en voz y sientan la base para ampliar a nuevos acentos/idiomas y añadir confirmaciones auditivas/visuales en futuras iteraciones.

<p align="center">
  <img src="Imagenes/Posiciones de pruebas/Posicion home.jpeg" alt="MyCobot 280 en HOME" width="200"><br>
  <em>MyCobot 280 M5 en posición HOME utilizada durante las validaciones.</em>
</p>

---


## Objetivos

### Objetivo general
Diseñar y desarrollar un sistema de reconocimiento de voz capaz de interpretar comandos para el control de sistemas robóticos.

### Objetivos específicos
1. Investigar, evaluar y seleccionar las bibliotecas de software más adecuadas para la transcripción de voz en tiempo real.
2. Desarrollar un analizador sintáctico y un analizador semántico para la interpretación de comandos de voz.
3. Validar la efectividad del sistema de interpretación de comandos de voz mediante pruebas con sistemas robóticos disponibles en el Departamento de Ingeniería Electrónica y Mecatrónica de la Universidad del Valle de Guatemala.
4. Implementar un módulo de activación por voz que detecte un comando o frase especial para iniciar la comunicación con el sistema robótico y habilitar la recepción de instrucciones.
5. Diseñar una interfaz gráfica intuitiva que permita visualizar en tiempo real la transcripción y el análisis de los comandos de voz, así como el estado de ejecución del sistema robótico.

---


## Enfoque y Metodología

### Enfoque
El sistema **transcribe voz en tiempo real**, **interpreta la intención del usuario** y **ejecuta trayectorias articulares seguras** en un manipulador. La arquitectura integra un **analizador sintáctico-semántico** y un **controlador con API clara** que **valida comandos relativos y absolutos** frente a **límites por junta** y **estados del sistema**. La **validación experimental**, con **ruido ambiente moderado** y **diferentes distancias al micrófono**.

### Metodología
1. **Investigación y selección** de bibliotecas de software para la **captura y transcripción de voz**.  
2. La **transcripción en tiempo real** se solucionó con **Google Cloud STT**.  
3. Se seleccionó **Python** para el desarrollo de **analizadores sintáctico-semánticos** que **extraen la intención y los parámetros, juntas y ángulos**.  
4. Posteriormente se estableció el **controlador del manipulador** que **valida cada orden contra límites por junta** y **muestra el estado del sistema**.  
5. Finalmente se realizó una **interfaz gráfica unificada** que **muestra transcripción, validaciones y estado del robot**, **cerrando el ciclo de retroalimentación usuario-sistema**.

---

## Características del Proyecto

- **Control por voz natural.** El robot entiende instrucciones habladas sencillas y las convierte en movimientos reales.
- **Seguridad primero.** Antes de moverse, el sistema revisa que cada orden sea segura para el brazo robótico.
- **Interfaz clara.** La pantalla muestra lo que se dijo, cómo lo entendió el sistema y qué está ejecutando.
- **Dos formas de moverlo.**
  - **Absoluto:** “Mueve la junta 4 a la posición 30” (va directo a ese ángulo).
  - **Relativo:** “Mueve la junta 2 más 50°” (ajusta respecto a la posición actual).
- **Pruebas en condiciones reales.** Funciona con ruido moderado y distintas distancias al micrófono.

---

## Tecnologías y Librerías Utilizadas

- **Python:** Lenguaje principal para todo el proyecto (parser, GUI y controlador).
- **PySide6 (Qt for Python):** Construcción de la interfaz gráfica (ventanas, botones, señales).
- **Matplotlib (QtAgg):** Gráficos embebidos y vista 3D del brazo dentro de la GUI.
- **NumPy:** Cálculo numérico y manejo de ángulos y transformaciones.
- **Robotics Toolbox for Python (rtb) + SpatialMath:** Modelo DH del robot y cinemática directa e inversa.
- **PyMyCobot:** Comunicación con el **myCobot 280 M5** (envío de ángulos, lectura de estado, LEDs).
- **Google Cloud Speech-to-Text:** Transcripción de voz en streaming (hipótesis parciales y finales).

---


##  Requisitos previos
- **Python 3.10–3.12** (64-bit).
- **Windows** con puerto USB/COM para el myCobot.
- **Micrófono USB** funcional.
- **Credenciales de Google Cloud STT** (archivo JSON de servicio).

---
  
## Guía de Instalación Paso a Paso

Abre tu terminal (PowerShell o CMD) y ejecuta los siguientes comandos para preparar el entorno y **todas** las librerías usadas por el proyecto.

:: ============================================================
:: INSTALACIÓN PASO A PASO (WINDOWS) — PROYECTO CONTROL POR VOZ
:: ============================================================

:: 1) CREAR ENTORNO VIRTUAL (en la carpeta del proyecto)
python -m venv .venv

:: 1.1) ACTIVAR ENTORNO
:: - PowerShell:
. .venv\Scripts\Activate.ps1
:: - CMD:
:: .venv\Scripts\activate.bat
:: - Git Bash:
:: source .venv/Scripts/activate

:: ------------------------------------------------------------

:: 2) ACTUALIZAR PIP
python -m pip install --upgrade pip

:: ------------------------------------------------------------

:: 3) INSTALAR LIBRERÍAS DE GUI Y GRÁFICOS (Qt + canvas)
python -m pip install PySide6 matplotlib

:: ------------------------------------------------------------

:: 4) INSTALAR CÁLCULO Y ROBÓTICA (cinemática, SE3, trayectorias)
python -m pip install numpy scipy roboticstoolbox-python spatialmath-python

:: ------------------------------------------------------------

:: 5) INSTALAR SOPORTE PARA MYCOBOT (comunicación serie)
python -m pip install pymycobot pyserial

:: ------------------------------------------------------------

:: 6) INSTALAR VOZ EN TIEMPO REAL (STT) Y UTILIDADES DE TEXTO
python -m pip install google-cloud-speech google-auth sounddevice unidecode six
:: Nota: si sounddevice pide compiladores, instala "Microsoft C++ Build Tools" y repite.

:: ------------------------------------------------------------

:: 7) CONFIGURAR CREDENCIALES DE GOOGLE STT (ajusta la ruta a tu JSON)
set GOOGLE_APPLICATION_CREDENTIALS=D:\Programa\STT_demo.json
:: (Opcional) También puedes editar 'speech_parser.py' -> KEYFILE = "D:\\Programa\\STT_demo.json"

:: ------------------------------------------------------------

:: 8) CONFIGURAR PUERTO DEL ROBOT (editar en robot_controller.py)
:: PORT = "COM9"   # cámbialo al COM real (COM3, COM7, etc.)
:: BAUD = 115200

:: ------------------------------------------------------------

:: 9) EJECUTAR LA APLICACIÓN GRÁFICA
python Gui_app_Brazo.py
:: Verás en la GUI: [LIVE]/[FIN], acciones (REL/ABS/HOME/MODE/CONFIRM/CANCEL) y el 3D del robot.

:: ------------------------------------------------------------

:: 10) CERRAR / LIMPIAR SESIÓN
:: - Detener el programa en consola:  Ctrl + C
:: - Desactivar el entorno virtual:
deactivate
:: - Cerrar la terminal:
:: exit

