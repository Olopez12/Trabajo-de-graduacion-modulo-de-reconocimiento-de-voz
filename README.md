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

