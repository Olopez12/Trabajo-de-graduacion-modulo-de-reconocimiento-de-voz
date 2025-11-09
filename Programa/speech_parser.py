# speech_parser.py
"""
Parser de comandos de voz + “loop” de reconocimiento en streaming (Google STT).

Este módulo provee:
- Normalización de texto (minúsculas, sin tildes) y parsing sintáctico-semántico
  para comandos relativos y absolutos orientados a control articular.
- Señales semánticas (MODE/HOME/CONFIRM/CANCEL/CONFREQ) extraídas del habla.
- Envolvente de reconocimiento de audio en tiempo real con `sounddevice` y
  Google Cloud Speech-to-Text, listo para integrarse en GUI (callbacks).

Estilo aplicado:
- Docstrings en formato NumPy (numpydoc), comentarios en línea breves y claros.
- Lógica intacta; únicamente documentación y notas de mantenimiento.

Referencias de estilo:
- Google Python Style Guide — google/styleguide
- numpydoc — numpy/numpydoc
- pandas docstring guide — pandas-dev/pandas
- pydocstyle (PEP 257) — PyCQA/pydocstyle
"""

from __future__ import annotations
import time, queue, re, unidecode
from six.moves import queue as six_queue
import sounddevice as sd
from google.cloud import speech
from google.oauth2 import service_account


# ---------- Configuración y datos --------------------------
MAX_JOINT = 6

# ---------------- Normalización ----------------------------
# Preferimos `unidecode` (más robusto); si no está disponible, caemos a `unicodedata`.
try:
    import unidecode as _ud
    def _norm(s: str) -> str:
        """Normaliza texto a ASCII sin tildes, en minúsculas y sin espacios extremos."""
        return _ud.unidecode(s).lower().strip()
except Exception:
    import unicodedata
    def _norm(s: str) -> str:
        """Fallback de normalización con `unicodedata` si no hay `unidecode`."""
        s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode("ascii")
        return s.lower().strip()

# Verbos que inducen signo negativo si no hay signo explícito (+/-/más/menos)
VERBS_NEG = {"decrementa","baja","restale","quita","reduce","disminuye"}
# Conjunto de verbos aceptados para detección de comandos
VERBS_ALL = r"(?:mueve|mover|gira|girar|rota|rotar|ajusta|ajustar|desplaza|desplazar|pon|coloca|lleva|incrementa|decrementa|sumale|restale|sube|baja)"

# Diccionarios de números (ordinales y cardinales en español)
ORDINALS = {
    "primer":1,"primero":1,"primera":1,
    "segundo":2,"segunda":2,
    "tercero":3,"tercera":3,
    "cuarto":4,"cuarta":4,
    "quinto":5,"quinta":5,
    "sexto":6,"sexta":6,
    "septimo":7,"septima":7,
    "octavo":8,"octava":8,
    "noveno":9,"novena":9,
    "decimo":10,"decima":10
}
CARDINALS = {
    "un":1,"uno":1,"una":1,
    "dos":2,"tres":3,"cuatro":4,"cinco":5,"seis":6,"siete":7,"ocho":8,"nueve":9,"diez":10
}

def _word_to_int(token: str):
    """Convierte un token numérico/ordinal/cardinal en entero; `None` si no aplica."""
    if token.isdigit():
        return int(token)
    return ORDINALS.get(token) or CARDINALS.get(token)


def parse_commands(text: str, mode: str = "relative"):
    """
    Interpreta un texto y devuelve una lista de acciones semánticas.

    Si `mode == "relative"`:
        → [("REL", joint:int, delta_deg:float), ...]
    Si `mode == "absolute"`:
        → [("ABS", joint:int, target_deg:float), ...]  # ángulo absoluto en grados

    Además, siempre puede devolver intenciones globales:
        ("MODE", "absolute"|"relative"),
        ("HOME",),
        ("CONFIRM",),
        ("CANCEL",),
        ("CONFREQ", True|False)

    Parameters
    ----------
    text : str
        Texto reconocido (posiblemente con puntuación/ruido).
    mode : {"relative","absolute"}, default="relative"
        Modo activo que guía el tipo de parse.

    Returns
    -------
    list
        Secuencia de tokens semánticos listos para el controlador.

    Notas
    -----
    - El parser usa expresiones regulares para estructura + reglas semánticas
      ligeras (p. ej., deduce signo a partir del verbo si no hay “+/-/más/menos”).
    - Normaliza el texto a minúsculas y sin tildes para robustez.
    """
    if not text:
        return []

    # Normalización básica y limpieza de caracteres frecuentes
    s = _norm(text)
    s = s.replace("º", " grados").replace("°", " grados")
    s = re.sub(r"[,;]", " ", s)

    out = []

    # ---------- Intenciones globales (independientes del modo) ----------
    # Cambiar modo
    m1 = re.search(r"\bmodo\s+(absoluto|relativo)\b", s)
    m2 = re.search(r"\b(?:cambia(?:r)?|pon(?:er)?|usa(?:r)?)\s+(?:a\s+)?(absoluto|relativo)\b", s)
    if m1 or m2:
        m = (m1 or m2).group(1)
        out.append(("MODE", "absolute" if m.startswith("absol") else "relative"))

    # HOME / INICIO / ORIGEN
    if re.search(r"\b(?:ir|ve|volver|regresar|llevar|poner|mover)\s+(?:a\s+)?(?:home|inicio|origen)\b", s) \
        or re.search(r"\bposicion\s+inicial\b", s):
            out.append(("HOME",))

    # Confirmar / Cancelar por voz
    if re.search(r"\b(?:confirm\w*|acept\w*|ejecut\w*|proced\w*|adelante|dale)\b", s):
        out.append(("CONFIRM",))
    if re.search(r"\b(?:cancel\w*|anul\w*|rechaz\w*|mejor\s+no|det[eé]n|para|stop)\b", s):
        out.append(("CANCEL",))

    # Activar / desactivar confirmación por voz
    mc_on  = re.search(r"\b(?:activar|habilitar)\s+confirmaci[oó]n\b", s)
    mc_off = re.search(r"\b(?:desactivar|deshabilitar|quitar)\s+confirmaci[oó]n\b", s)
    if mc_on:
        out.append(("CONFREQ", True))
    if mc_off:
        out.append(("CONFREQ", False))

    # ---------- Piezas comunes para movimientos ----------
    VERB = VERBS_ALL
    ART  = r"(?:la|el)"
    SYN_WORDS = r"(?:juntas?|eslabones?|articulaciones?|conexiones?|links?|posiciones?)"
    SYN  = rf"(?:{SYN_WORDS}|\bj\b)"
    NUMJ = r"(?P<joint>\d+|[a-z]+)"
    CONN = r"(?:\s*(?:a|en|hasta|para)\s*)?"

    # ---------- ABSOLUTO EN GRADOS ----------
    if mode == "absolute":
        SIGN = r"(?P<sign>[+\-]|mas|menos|positivo|negativo)?"
        ANG  = r"(?P<ang>\d+(?:[.,]\d*)?)"
        DEG  = r"(?:\s*grados?)?"

        # Variantes: “junta 2 ... +15 grados”, “j#2 10”, “+20 grados ... junta segunda”
        pA = re.compile(
            rf"(?:(?P<verb>{VERB})\s+)?(?:{ART}\s+)?{SYN}\s+{NUMJ}\s*{CONN}"
            rf"(?:{ART}\s+)?(?:pos(?:icion)?)?\s*{SIGN}\s*{ANG}{DEG}"
        )
        pB = re.compile(
            rf"(?:(?P<verb>{VERB})\s+)?\bj\s*#?\s*{NUMJ}\s*{SIGN}\s*{ANG}{DEG}"
        )
        pC = re.compile(
            rf"{SIGN}\s*{ANG}{DEG}\s*{CONN}(?:{ART}\s+)?{SYN}\s+{NUMJ}"
        )

        matches = []
        for patt in (pA, pB, pC):
            matches.extend(list(patt.finditer(s)))
        matches.sort(key=lambda m: m.start())

        for m in matches:
            raw_joint = (m.group("joint") or "").strip()
            joint = _word_to_int(raw_joint)
            if joint is None or not (1 <= joint <= MAX_JOINT):
                continue

            ang_str = (m.group("ang") or "0").replace(",", ".")
            try:
                angle = float(ang_str)
            except ValueError:
                continue

            sign = (m.group("sign") or "").strip()
            if sign in {"-","menos","negativo"}:
                angle = -abs(angle)
            elif sign in {"+","mas","positivo"}:
                angle = abs(angle)

            out.append(("ABS", joint, angle))
        return out

    # ---------- RELATIVO ----------
    SIGN = r"(?P<sign>[+\-]|mas|menos|positivo|negativo)?"
    ANG  = r"(?P<ang>\d+(?:[.,]\d*)?)"
    DEG  = r"(?:\s*grados?)?"

    # Variantes: “mueve la junta 3 +15”, “j3 10”, “gira -20 en la 2”, etc.
    p1 = re.compile(rf"(?:(?P<verb>{VERB})\s+)?(?:{ART}\s+)?{SYN}\s+{NUMJ}\s*{CONN}{SIGN}\s*{ANG}{DEG}")
    p2 = re.compile(rf"(?:(?P<verb>{VERB})\s+)?{NUMJ}\s+(?:{ART}\s+)?{SYN}\s*{CONN}{SIGN}\s*{ANG}{DEG}")
    p3 = re.compile(rf"(?:(?P<verb>{VERB})\s+)?\bj\s*#?\s*{NUMJ}\s*{SIGN}\s*{ANG}{DEG}")
    p4 = re.compile(rf"(?:(?P<verb>{VERB})\s+){SIGN}\s*{ANG}{DEG}\s*{CONN}(?:{ART}\s+)?{SYN}\s+{NUMJ}")

    matches = []
    for patt in (p1, p2, p3, p4):
        matches.extend(list(patt.finditer(s)))
    matches.sort(key=lambda m: m.start())

    results = []
    for m in matches:
        raw_joint = (m.group("joint") or "").strip()
        joint = _word_to_int(raw_joint)
        if joint is None or not (1 <= joint <= MAX_JOINT):
            continue

        ang_str = (m.group("ang") or "0").replace(",", ".")
        try:
            angle = float(ang_str)
        except ValueError:
            continue

        sign = (m.group("sign") or "").strip()
        verb = (m.group("verb") or "").strip()

        # Signo por prioridad: explícito (+/-/más/menos) > verbo semántico > positivo
        if sign in {"-","menos","negativo"}:
            angle = -abs(angle)
        elif sign in {"+","mas","positivo"}:
            angle = abs(angle)
        else:
            angle = -abs(angle) if verb in VERBS_NEG else abs(angle)

        results.append(("REL", joint, angle))

    return out + results


# ---------- Google STT ---------------------------------------------------------------------------
# ADVERTENCIA: `KEYFILE` contiene ruta local a credenciales. Manténlo fuera del repo público
# o usa variables de entorno / secret managers. No cambiar la lógica aquí (solo documentación).
KEYFILE = "D:\\Programa\\STT_demo.json"  # Cambia la ruta si es necesario (doble backslash en Windows)
creds   = service_account.Credentials.from_service_account_file(KEYFILE)
client  = speech.SpeechClient(credentials=creds)

# Parámetros de audio (16 kHz mono, bloques de 100 ms)
RATE  = 16000
CHUNK = int(RATE / 10)

# Configuración de reconocimiento (es-ES con puntuación automática)
recognition_config = speech.RecognitionConfig(
    encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
    sample_rate_hertz=RATE,
    language_code="es-ES",
    enable_automatic_punctuation=True
)
streaming_config = speech.StreamingRecognitionConfig(
    config=recognition_config,
    interim_results=True
)

# Cola de audio crudo PCM para alimentar a la API de streaming
audio_q: six_queue.Queue[bytes] = queue.Queue()

def _sd_callback(indata, frames, time_info, status):
    """Callback de `sounddevice`: encola audio PCM en `audio_q`."""
    if status:
        print(f"[SD status] {status}", flush=True)
    # Convierte el buffer CFFI a bytes de forma segura
    data_bytes = indata.tobytes() if hasattr(indata, "tobytes") else bytes(indata)
    audio_q.put(data_bytes)


def _audio_generator():
    """Generador infinito de `StreamingRecognizeRequest` desde `audio_q`."""
    while True:
        chunk = audio_q.get()
        if chunk is None:
            return
        yield speech.StreamingRecognizeRequest(audio_content=chunk)


# ---------- Clase de alto nivel para usar en GUI -------------------------------------------------
class StreamingRecognizer:
    """Envolvente de reconocimiento en streaming con callbacks Qt-safe.

    Parameters
    ----------
    on_live : Callable[[str], None]
        Callback para texto parcial (interino).
    on_final : Callable[[str], None]
        Callback para texto final de cada resultado.
    on_action : Callable[[list], None]
        Callback para lista de acciones semánticas (tokens) parseadas.
    on_error : Callable[[Exception], None]
        Callback para notificar errores del bucle de reconocimiento.
    mode_provider : Callable[[], str], default=lambda: "relative"
        Función que devuelve el modo actual ("relative"|"absolute") para el parser.

    Notas
    -----
    - `start()` lanza un hilo `daemon` que abre la entrada de audio y consume
      la API `streaming_recognize`. `stop()` corta el bucle de forma segura.
    - El parser `parse_commands` se invoca para resultados finales (`is_final`).
    """

    def __init__(self, *, on_live, on_final, on_action, on_error, mode_provider=lambda: "relative"):
        self._on_live   = on_live
        self._on_final  = on_final
        self._on_action = on_action
        self._on_error  = on_error
        self._running   = False
        self._mode_provider = mode_provider

    # ---- Hilo principal ------------------------------------------------------------------------
    def _loop(self):
        """Bucle de reconocimiento: audio → Google STT → callbacks (LIVE/FIN/ACCIONES)."""
        from threading import current_thread
        print(f"[Reconocedor] Iniciado en {current_thread().name}")
        while self._running:
            try:
                # Captura de audio crudo (PCM 16-bit mono)
                with sd.RawInputStream(samplerate=RATE, blocksize=CHUNK, dtype="int16",
                    channels=1, callback=_sd_callback):
                    requests  = _audio_generator()
                    responses = client.streaming_recognize(streaming_config, requests)
                    for resp in responses:
                        if not self._running:          # parada solicitada
                            break
                        if not resp.results:
                            continue
                        result = resp.results[0]
                        txt = result.alternatives[0].transcript.strip()
                        if result.is_final:
                            # Texto final → notificar, parsear y emitir acciones
                            self._on_final(txt)
                            mode = self._mode_provider()  # "relative" | "absolute"
                            acts = parse_commands(txt, mode=mode)
                            self._on_action(acts if acts else [])
                        else:
                            # Texto interino/LIVE
                            self._on_live(txt)
            except Exception as e:
                # Reintento simple con backoff mínimo
                self._on_error(e)
                time.sleep(1)
        print("[Reconocedor] Detenido")

    # --------------------------------------------------------------------------------------------
    def start(self):
        """Arranca el hilo de reconocimiento si no está corriendo."""
        if self._running:
            return
        self._running = True
        import threading, functools
        self._thr = threading.Thread(target=functools.partial(self._loop), daemon=True)
        self._thr.start()

    def stop(self):
        """Detiene el reconocimiento y desbloquea generadores/bloqueos."""
        if not self._running:
            return
        self._running = False
        audio_q.put(None)   # desbloquea generador
        self._thr.join(timeout=2)
