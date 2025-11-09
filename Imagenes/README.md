# Imágenes del Proyecto — Interfaz, Simulación y Posiciones Físicas

Este directorio documenta visualmente las pruebas y la evolución de la interfaz del sistema de control por voz para el **myCobot 280 M5**. Las imágenes se organizan en subcarpetas y comparten una **convención de nombres** común para vincular **interfaz**, **simulación** y **pose física** de cada prueba.

## Propósito de cada carpeta

### `Posiciones de pruebas/`
Fotos del robot **en el mundo real**:
- `Posicion de prueba 1`, `Posicion de prueba 2`: poses alcanzadas durante pruebas.
- `Posicion home`: referencia de **HOME** del sistema.

### `Pruebas de parser/Interfaces/`
Evolución de la **interfaz de usuario**:
- `Interfaz de usuario prueba` → versión consolidada para demostraciones (con colores solo de propuesta).
- `Interfaz para pruebas` → versión temprana para testeo.
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
