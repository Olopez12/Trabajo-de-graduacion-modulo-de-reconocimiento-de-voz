# speech_parser.py

# SPEECH_PARSER — PARSER sintáctico

# DESCRIPCIÓN GENERAL

#    • mode="relative" → ("REL", joint:int, delta_deg:float)
#    • mode="absolute" → ("ABS", joint:int, pos_index:int)  con pos ∈ [1..20]
# - Usa expresiones regulares para la estructura (sintaxis) y reglas semánticas
#   ligeras para inferir el signo según el VERBO cuando no hay “+ / - / más / menos”.
# - Normaliza texto (minúsculas, sin tildes; fallback si falta unidecode),
#   soporta ordinales/cardinales (“segunda”, “tres”) y sinónimos/abreviaturas:
#   “junta/eslabón/articulación/conexión/link/posición” y “j”, “j#”.

# - Patrones RELATIVOS (p1–p4) cubren variantes como:
#     “mueve la junta 3 a 15 grados”, “j3 10”, “gira +20 en la 2”, etc.
# - Patrones ABSOLUTOS (pA–pC) cubren:
#     “junta 2 a posición 7”, “j#2 pos 5”, “posición 3 de la junta segunda”.


from __future__ import annotations
import time, queue, re, unidecode
from six.moves import queue as six_queue
import sounddevice as sd
from google.cloud import speech
from google.oauth2 import service_account


# ---------- Configuración y datos --------------------------
MAX_JOINT = 6
#---------------- Normalización------------------------------
try:
    import unidecode as _ud
    def _norm(s: str) -> str:
        return _ud.unidecode(s).lower().strip()
except Exception:
    import unicodedata
    def _norm(s: str) -> str:
        s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode("ascii")
        return s.lower().strip()

# Verbos con semántica de signo cuando NO hay + / - / más / menos explícitos
VERBS_NEG = {"decrementa","baja","restale","quita","reduce","disminuye"}
VERBS_ALL = r"(?:mueve|mover|gira|girar|rota|rotar|ajusta|ajustar|desplaza|desplazar|pon|coloca|lleva|incrementa|decrementa|sumale|restale|sube|baja)"

# Diccionarios de números
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
    if token.isdigit():
        return int(token)
    return ORDINALS.get(token) or CARDINALS.get(token)

def parse_commands(text: str, mode: str = "relative"):
    """
    Si mode == 'relative' → [("REL", joint:int, delta_deg:float), ...]
    Si mode == 'absolute' → [("ABS", joint:int, target_deg:float), ...]  (ángulo absoluto)
    Además, siempre puede devolver intenciones:
    ("MODE", "absolute"|"relative"), ("HOME",), ("CONFIRM",), ("CANCEL",),
    ("CONFREQ", True|False)
    """
    if not text:
        return []

    s = _norm(text)
    s = s.replace("º", " grados").replace("°", " grados")
    s = re.sub(r"[,;]", " ", s)

    out = []

    # ---------- Intenciones globales (independientes del modo) ----------
    # MODO
    m1 = re.search(r"\bmodo\s+(absoluto|relativo)\b", s)
    m2 = re.search(r"\b(?:cambia(?:r)?|pon(?:er)?|usa(?:r)?)\s+(?:a\s+)?(absoluto|relativo)\b", s)
    if m1 or m2:
        m = (m1 or m2).group(1)
        out.append(("MODE", "absolute" if m.startswith("absol") else "relative"))

    # HOME / INICIO / ORIGEN
    if re.search(r"\b(?:ir|ve|volver|regresar|llevar|poner|mover)\s+(?:a\s+)?(?:home|inicio|origen)\b", s) \
        or re.search(r"\bposicion\s+inicial\b", s):
            out.append(("HOME",))

    # CONFIRMAR / CANCELAR (por voz)
    if re.search(r"\b(?:confirm\w*|acept\w*|ejecut\w*|proced\w*|adelante|dale)\b", s):
        out.append(("CONFIRM",))
    if re.search(r"\b(?:cancel\w*|anul\w*|rechaz\w*|mejor\s+no|det[eé]n|para|stop)\b", s):
        out.append(("CANCEL",))

    # (Opcional) activar/desactivar confirmación por voz
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

    # ---------- RELATIVO (como ya lo tenías) ----------
    SIGN = r"(?P<sign>[+\-]|mas|menos|positivo|negativo)?"
    ANG  = r"(?P<ang>\d+(?:[.,]\d*)?)"
    DEG  = r"(?:\s*grados?)?"

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
        if sign in {"-","menos","negativo"}:
            angle = -abs(angle)
        elif sign in {"+","mas","positivo"}:
            angle = abs(angle)
        else:
            angle = -abs(angle) if verb in VERBS_NEG else abs(angle)
        results.append(("REL", joint, angle))

    return out + results



# ---------- Google STT ---------------------------------------------------------------------------
KEYFILE = "D:\Programa\STT_demo.json"                 # Cambia la ruta si es necesario
creds   = service_account.Credentials.from_service_account_file(KEYFILE)
client  = speech.SpeechClient(credentials=creds)

RATE  = 16000
CHUNK = int(RATE / 10)

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

audio_q: six_queue.Queue[bytes] = queue.Queue()

def _sd_callback(indata, frames, time_info, status):
    if status:
        print(f"[SD status] {status}", flush=True)
    # Convierte el buffer CFFI a bytes de forma segura
    data_bytes = indata.tobytes() if hasattr(indata, "tobytes") else bytes(indata)
    audio_q.put(data_bytes)


def _audio_generator():
    while True:
        chunk = audio_q.get()
        if chunk is None:
            return
        yield speech.StreamingRecognizeRequest(audio_content=chunk)

# ---------- Clase de alto nivel para usar en GUI -------------------------------------------------
class StreamingRecognizer:
    def __init__(self, *, on_live, on_final, on_action, on_error, mode_provider=lambda: "relative"):
        self._on_live   = on_live
        self._on_final  = on_final
        self._on_action = on_action
        self._on_error  = on_error
        self._running   = False
        self._mode_provider = mode_provider

    # ---- Hilo principal ------------------------------------------------------------------------
    def _loop(self):
        from threading import current_thread
        print(f"[Reconocedor] Iniciado en {current_thread().name}")
        while self._running:
            try:
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
                            self._on_final(txt)
                            mode = self._mode_provider()  # "relative" | "absolute"
                            acts = parse_commands(txt, mode=mode)
                            self._on_action(acts if acts else [])
                        else:
                            self._on_live(txt)
            except Exception as e:
                self._on_error(e)
                time.sleep(1)  # reintento simple
        print("[Reconocedor] Detenido")

    # --------------------------------------------------------------------------------------------
    def start(self):
        if self._running:
            return
        self._running = True
        import threading, functools
        self._thr = threading.Thread(target=functools.partial(self._loop), daemon=True)
        self._thr.start()

    def stop(self):
        if not self._running:
            return
        self._running = False
        audio_q.put(None)   # desbloquea generador
        self._thr.join(timeout=2)
