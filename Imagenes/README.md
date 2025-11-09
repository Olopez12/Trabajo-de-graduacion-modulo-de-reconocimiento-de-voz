# Imágenes del Proyecto — Interfaz, Simulación y Posiciones Físicas

Este directorio documenta visualmente las pruebas y la evolución de la interfaz del sistema de control por voz para el **myCobot 280 M5**. Las imágenes se organizan en subcarpetas y comparten una **convención de nombres** común para vincular **interfaz**, **simulación** y **pose física** de cada prueba.

## Propósito de cada carpeta

### `Posiciones de pruebas/`
Fotos del robot **en el mundo real**:
- `Posicion de prueba 1`, `Posicion de prueba 2`: poses alcanzadas durante pruebas.
- `Posicion home`: referencia de **HOME** del sistema.

### `Pruebas de parser/Interfaces/`
Evolución de la **interfaz de usuario**:
- `Interfaz de usuario prueba` → versión temprana.
- `Interfaz para pruebas` → layout intermedio para testeo.
- `Interfaz de usuario final` → versión consolidada para demostraciones.

### `Pruebas de parser/Modo absoluto/`
Casos donde el parser está en **modo absoluto** (el valor es el ángulo destino):
- `Prueba cambio de modo`: evidencia del cambio verbal de REL→ABS (o viceversa).
- `Prueba comando home`: uso del comando *home* por voz.
- `Prueba sencilla`, `Prueba sencilla 2`: pruebas unitarias de órdenes ABS.

### `Pruebas de parser/Modo relativo/`
Casos en **modo relativo** (el valor es incremento/decremento):
- `Prueba reinicio de posicion usando el boton`: retorno a HOME con botón.
- `Prueba reinicio de posicion usando el habla`: retorno a HOME por voz.
- `Prueba sencilla`, `Prueba sencilla 2/3/4`: incrementos/decrementos sobre juntas.

---

## Convenciones de referencia (sin renombrar archivos)

Para enlazar una **prueba completa** en tu documentación principal (README del repo o informe), usa esta plantilla y ajusta las rutas según la extensión:

```markdown
**Prueba relativa (incrementos sobre juntas)**  
- Interfaz: `Imagenes/Pruebas de parser/Modo relativo/Prueba sencilla 3.png`  
- Resultado físico relacionado (si aplica): `Imagenes/Posiciones de pruebas/Posicion de prueba 2.jpg`
**Prueba absoluta con cambio de modo y home por voz**  
- Cambio de modo: `Imagenes/Pruebas de parser/Modo absoluto/Prueba cambio de modo.png`  
- Comando home: `Imagenes/Pruebas de parser/Modo absoluto/Prueba comando home.png`  
- Pose HOME: `Imagenes/Posiciones de pruebas/Posicion home.jpg`
