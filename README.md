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
El proyecto integra un flujo de **voz → intención → movimiento** para control articular seguro del myCobot 280 M5. Se compone de tres subsistemas principales:
1. **STT (transcripción en tiempo real):** captura de audio a 16 kHz con puntuación automática para obtener hipótesis parciales [LIVE] y finales [FIN].
2. **Parser sintáctico–semántico:** normaliza el texto (minúsculas, sin tildes), interpreta números (cardinales/ordinales), signos (“más/menos”) y decide **modo relativo/absoluto**; genera tokens de acción (`REL`, `ABS`, `HOME`, `MODE`, `CONFIRM`, `CANCEL`).
3. **Controlador y GUI:** valida límites por junta, ejecuta movimientos (unitarios y absolutos) y expone en la interfaz la transcripción, la intención y el estado de ejecución para trazabilidad.

Este enfoque reduce la carga de interfaces tradicionales y habilita un ciclo natural **“hablar → ver → corregir”** con programación defensiva (bloqueos fuera de rango, confirmaciones y manejo explícito de errores).

### Metodología

**1) Diseño y selección tecnológica**
- Definición de requisitos de latencia, robustez y seguridad.
- Selección de bibliotecas para STT, parsing y control del robot.
- Estructuración del proyecto en módulos: `speech_parser.py`, `robot_controller.py`, `Gui_app_Brazo.py`.

**2) Implementación incremental**
- **STT en streaming:** configuración de audio (16 kHz, mono) y manejo de resultados interinos/finales.
- **Parser híbrido:** expresiones regulares + reglas semánticas (verbos que inducen signo, manejo de coma decimal, múltiples órdenes por frase).
- **Controlador del robot:** capa de validación (USER_LIMITS y ventana de tolerancia), envío de setpoints y retrolectura de ángulos.
- **GUI:** presentación sincronizada de [LIVE]/[FIN], acciones interpretadas y estados (modo, errores, HOME).

**3) Integración y pruebas de sistema**
- Pruebas funcionales en **modo relativo** (incrementos/decrementos) y **modo absoluto** (destinos por junta).
- Ensayos de **cambio de modo por voz** y **comando HOME** con confirmación/cancelación.
- Verificación de la correspondencia **interfaz → simulación → pose física** (con registro fotográfico).

**4) Validación experimental**
- Entorno con **ruido moderado** y distancias ≤ 1 m al micrófono.
- Métricas cualitativas: consistencia de ejecución, rechazo seguro de órdenes ambiguas/fuera de rango, recuperación tras errores.
- Iteraciones sucesivas hasta estabilizar patrones de uso y dictado.

**5) Documentación y trazabilidad**
- Capturas de interfaz, simulación y robot físico organizadas por pruebas.
- Registro de configuraciones (audio, puertos, límites por junta) y dependencias.
- Secciones de README: descripción, objetivos, metodología, resultados, estructura de imágenes y consideraciones de seguridad.

**Herramientas y entorno (resumen)**
- **Hardware:** myCobot 280 M5, micrófono de condensador USB.
- **Software:** PySide6, numpy, roboticstoolbox-python, spatialmath, pymycobot, google-cloud-speech, sounddevice.
- **SO:** Windows (ajustable a otros entornos con configuración equivalente).

