# Imágenes del Proyecto — Interfaz, Simulación y Posiciones Físicas

Este directorio documenta visualmente las pruebas y la evolución de la interfaz del sistema de control por voz para el **myCobot 280 M5**. Las imágenes se organizan en subcarpetas y comparten una **convención de nombres** común para vincular **interfaz**, **simulación** y **pose física** de cada prueba.

---

## Estructura de carpetas

Las imágenes ligadas entre sí comparten el **mismo índice**:

| Prefijo | Carpeta      | Significado                                        | Ejemplo de archivo |
|:------:|---------------|----------------------------------------------------|--------------------|
| **I#** | `interfaz/`   | Prueba en la interfaz (GUI)                        | `I1.png`           |
| **S#** | `simulacion/` | Simulación/planeación de la misma prueba           | `S1.png`           |
| **F#** | `fisico/`     | Pose física lograda por el myCobot (mundo real)    | `F1.jpg`           |

- El **número** `#` es el vínculo entre las tres imágenes.  
  Por ejemplo: `I7` ↔ `S7` ↔ `F7` representan **la misma prueba**.

### Ejemplos
- **Prueba 1**:  
  - Interfaz: `interfaz/I1.png`  
  - Simulación: `simulacion/S1.png`  
  - Físico: `fisico/F1.jpg`
- **Prueba 12**:  
  - Interfaz: `interfaz/I12.png`  
  - Simulación: `simulacion/S12.png`  
  - Físico: `fisico/F12.jpg`

---

## Modos y comandos por voz

En `modos/` se documentan cambios de **modo verbal**:

- **ABS** (absoluto): el ángulo objetivo se interpreta como posición final de la junta.  
- **REL** (relativo): el valor se interpreta como incremento/decremento sobre la posición actual.

**Sugerencia de nombres**:
- `modos/ABS_on_01.png`, `modos/REL_on_01.png`  
- `modos/cambio_REL_a_ABS_02.png`  
- `modos/confirmacion_voz_03.png`, `modos/cancelacion_voz_03.png`

Incluye subtítulos breves en el commit para clarificar el contexto del cambio (p. ej., “Cambio a ABS tras ‘modo absoluto’”).

---

## Sistema Junto

La carpeta `sistema_junto/` agrupa imágenes del **sistema completo en funcionamiento** (todas las juntas y elementos integrados). Útil para mostrar:
- Vista general del **pipeline** (voz → parser → controlador → robot).
- Secuencias de operación (inicio, confirmación, ejecución, home).
- Demostraciones para presentaciones o documentación técnica.

**Sugerencia de nombres**:
- `sistema_junto/overview_01.jpg`
- `sistema_junto/ejecucion_comando_02.jpg`
- `sistema_junto/home_sequence_03.jpg`

---

## Versiones de la interfaz

Si tu GUI evolucionó en el tiempo (v1, v2, v3), puedes documentarlo así:

- `interfaz/v1/I3.png`  — Primera versión (botones básicos).
- `interfaz/v2/I3.png`  — Ajustes visuales y estados.
- `interfaz/v3/I3.png`  — Vista final con 3D/etiquetas.

> Mantén el mismo índice `I#` para **la misma prueba**, y usa subcarpetas por versión para reflejar la evolución sin perder la vinculación `S#/F#`.

---

## Recomendaciones de captura

- **Resolución**: preferible 1280×720 o 1920×1080 para lectura clara en informes.  
- **Formato**: PNG para capturas de pantalla (sin artefactos); JPG para fotos reales.  
- **Fondo y contraste**: evita fondos con mucho ruido; usa zoom adecuado en la GUI.  
- **Nomenclatura consistente**: no mezcles `I-1.png`, `i1.PNG`, etc.; usa el estándar `I#`.

---

## Cómo agregar nuevas imágenes (paso a paso)

1. Determina el **índice** de la nueva prueba (siguiente número libre).  
2. Exporta:
   - GUI → `interfaz/I#.png`
   - Simulación → `simulacion/S#.png`
   - Física → `fisico/F#.jpg`
3. Si el caso muestra cambio de modo o confirmaciones → añade capturas en `modos/`.  
4. Haz commit con un mensaje descriptivo, por ejemplo:  
