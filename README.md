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

## Enfoque y Metodología

### Arquitectura general
- **STT en streaming (es-ES, 16 kHz, puntuación automática)** para obtener hipótesis [LIVE]/[FIN]. :contentReference[oaicite:3]{index=3} :contentReference[oaicite:4]{index=4}  
- **Analizador sintáctico-semántico** que normaliza texto, resuelve ordinales y signos (“más/menos”), acepta coma decimal y extrae múltiples órdenes en una sola frase. :contentReference[oaicite:5]{index=5}  
- **Controlador del manipulador** con API y política de seguridad (bloqueos de fuera de rango, manejo de errores y trazabilidad). :contentReference[oaicite:6]{index=6}

<p align="center">
  <img src="Imagenes/Pruebas de parser/Modo absoluto/Prueba sencilla.png" alt="Modo absoluto - GUI" width="31%">
  <img src="Imagenes/Pruebas de parser/Modo relativo/Prueba sencilla.png" alt="Modo relativo - GUI" width="31%">
  <img src="Imagenes/Pruebas de parser/Interfaces/Interfaz de usuario final.png" alt="Interfaz final" width="31%"><br>
  <em>Interfaz gráfica en modo absoluto y modo relativo; versión final de la GUI.</em>
</p>

### Metodología de desarrollo
Se adoptó un **modelo en espiral** (iterativo) por la naturaleza híbrida HW/SW del proyecto: planificación y selección tecnológica, implementación del flujo de voz, diseño lingüístico (parser) e integración con el controlador y GUI; cada iteración se validó en escenarios con ruido moderado y variaciones de usuario. :contentReference[oaicite:7]{index=7} :contentReference[oaicite:8]{index=8}

### Procedimiento de validación
Ensayos sobre **MyCobot 280 M5** con micrófono **JBL Quantum Stream Talk**, distancias ≤1 m, y ambiente con ruido moderado; el protocolo enfatizó el ciclo “hablar–ver–corregir” (modo, límites, dicción/pausas) hasta consolidar patrones robustos. :contentReference[oaicite:9]{index=9} :contentReference[oaicite:10]{index=10} :contentReference[oaicite:11]{index=11}

---

## Resultados

- **Transcripción continua** estable para control en tiempo real con ruido moderado y sesiones prolongadas. :contentReference[oaicite:12]{index=12}  
- **Parser sintáctico-semántico** interpretó intención y parámetros; ante ambigüedad leve, activó rechazo de comando manteniendo seguridad. :contentReference[oaicite:13]{index=13}  
- **Ejecución segura**: trayectorias coinciden con la transcripción en GUI y se mantienen dentro de límites; bloqueos fuera de rango y manejo de errores explícitos. :contentReference[oaicite:14]{index=14} :contentReference[oaicite:15]{index=15}  
- **Viabilidad** del enfoque para control articular seguro y base para ampliar acentos/idiomas. :contentReference[oaicite:16]{index=16}

<p align="center">
  <img src="Imagenes/Posiciones de pruebas/Posicion de prueba 1.png" alt="Posición de prueba 1" width="48%">
  <img src="Imagenes/Posiciones de pruebas/Posicion de prueba 2.png" alt="Posición de prueba 2" width="48%"><br>
  <em>Correspondencia entre órdenes por voz, GUI y pose física del manipulador.</em>
</p>

---

## Objetivos

**General.** Diseñar y desarrollar un sistema de reconocimiento de voz capaz de interpretar comandos para el control de sistemas robóticos. :contentReference[oaicite:17]{index=17}

**Específicos.**
1) Seleccionar bibliotecas para transcripción de voz en tiempo real.  
2) Desarrollar analizador sintáctico y semántico.  
3) Validar el sistema con robots del departamento.  
4) Implementar activación por voz.  
5) Diseñar GUI para trazabilidad y estado del sistema. :contentReference[oaicite:18]{index=18}

---

## Componentes y entorno

- **Robot:** MyCobot 280 M5. :contentReference[oaicite:19]{index=19}  
- **Audio:** Micrófono JBL Quantum Stream Talk. :contentReference[oaicite:20]{index=20}  
- **Software:** Configuración del entorno, dependencias y versiones (STT, parser, GUI y controlador) documentadas en el trabajo principal. :contentReference[oaicite:21]{index=21} :contentReference[oaicite:22]{index=22}

---

## Estructura de imágenes del repositorio

- `Imagenes/Pruebas de parser/Interfaces/` → evolución de interfaces: `Interfaz para pruebas`, `Interfaz de usuario prueba`, `Interfaz de usuario final`.  
- `Imagenes/Pruebas de parser/Modo absoluto/` → capturas de pruebas (p. ej. `Prueba sencilla`, `Prueba sencilla 2`, `Prueba comando home`, `Prueba cambio de modo`).  
- `Imagenes/Pruebas de parser/Modo relativo/` → capturas de pruebas (p. ej. `Prueba sencilla`, `Prueba sencilla 2-4`, `Reinicio de posición por botón/voz`).  
- `Imagenes/Posiciones de pruebas/` → fotografías del robot: `Posicion de prueba 1`, `Posicion de prueba 2`, `Posicion home`.

> **Nota:** Usa rutas relativas como arriba para que GitHub renderice las imágenes en el README.

---

## Conclusiones (resumen)

El módulo de voz controla el manipulador con ejecución consistente bajo condiciones realistas; el analizador híbrido y la programación defensiva permiten una operación fluida y segura. Las mejoras futuras incluyen confirmaciones auditivas/visuales y empaquetado de la GUI (p. ej. distribución ejecutable). :contentReference[oaicite:23]{index=23} :contentReference[oaicite:24]{index=24}
