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

> Abre **PowerShell** o **CMD** dentro de la carpeta del proyecto.

---

### 1) Crear y activar entorno virtual
```bash
# Crear el entorno virtual
python -m venv .venv

# Activar en PowerShell
. .venv\Scripts\Activate.ps1
# (Si usas CMD)    .venv\Scripts\activate.bat
# (Si usas Git Bash)  source .venv/Scripts/activate
```

### 2) Actualizar pip
```bash
python -m pip install --upgrade pip
```
### 3) Instalar GUI y gráficos
```bash
python -m pip install PySide6 matplotlib
```
### 4) Instalar cálculo y robótica
```bash
python -m pip install numpy scipy roboticstoolbox-python spatialmath-python
```
### 5) Instalar comunicación con myCobot
```bash
python -m pip install pymycobot pyserial
```
### 6) Instalar voz en tiempo real (STT) y utilidades de texto
```bash
python -m pip install google-cloud-speech google-auth sounddevice unidecode six
```

---

## Sistema Robótico Utilizado

Para las pruebas y demostraciones se empleó el **myCobot 280 M5**, un brazo robótico de sobremesa de **seis grados de libertad** orientado a docencia y prototipado rápido. Su tamaño y ecosistema lo hacen ideal para iterar en laboratorio sin logística complicada.

- **Formato compacto.** Ocupa poco espacio y se traslada sin esfuerzo; perfecto para mesas de trabajo y aulas.
- **Control M5Stack.** Basado en la plataforma M5, lo que facilita encendido rápido, telemetría básica y personalización.
- **6 DOF reales.** La cadena cinemática permite posicionar y orientar el efector con buena flexibilidad para tareas de prueba.
- **Integración sencilla desde Python.** Soporta bibliotecas como **`pymycobot`** para enviar/leer ángulos y manejar estados sin drivers exóticos.
- **Montaje y puesta en marcha rápidos.** Conexión por USB/serial y alimentación estándar; en minutos está listo para ejecutar rutinas.
- **Uso típicamente académico.** Adecuado para ejercicios de control, cinemática y HMI/voz, donde la seguridad y la repetibilidad pesan más que la carga útil.

> En este proyecto, el myCobot 280 M5 actuó como plataforma de validación para comandos de voz en **modo relativo y absoluto**, con límites por junta y retorno de estado integrados a la GUI.

Puedes encontrar más detalles y documentación oficial en **[Elephant Robotics](https://www.elephantrobotics.com/en/support-280-m5-en/)**.

<p align="center">
  <img src="FotosReadME/mycobot-280-m5.jpeg" alt="myCobot 280 M5" width="640">
</p>

**Fuente:** [myCobot 280 M5 — Elephant Robotics](https://www.elephantrobotics.com/en/support-280-m5-en/)






