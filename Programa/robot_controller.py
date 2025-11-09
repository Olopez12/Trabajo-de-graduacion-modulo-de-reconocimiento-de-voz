# robot_controller.py
from __future__ import annotations
import time, threading, queue
from typing import List, Tuple
from PySide6 import QtCore

from pymycobot import MyCobot280

PORT = "COM9"
BAUD = 115200


ABS_POSITIONS_DEG = {
    1: [0,10,15,20,25,30,35,40,45,50,55,60,65,70,80,90,100,110,120,145],
    2: [-120,-114,-108,-102,-96,-90,-84,-78,-72,-66,-60,-54,-48,-42,-36,-30,-24,-18,-12,-6],
    3: [0,8,16,24,32,40,48,56,64,72,80,88,96,104,112,120,128,136,144,150],
    4: [-120,-108,-96,-84,-72,-60,-45,-30,-15,0,15,30,45,60,72,84,96,108,120,135],
    5: [-120,-108,-96,-84,-72,-60,-48,-36,-24,-12,0,12,24,36,48,60,72,84,96,108],
    6: [-160,-144,-128,-112,-96,-80,-64,-48,-32,-16,0,16,32,48,64,80,96,112,128,144],
}


HOME_ANGLES = [119.17, -94.83, 148.35, 26.71, -75.14, 117.59]
MOVE_SPEED = 50           # 0..100
SETTLE_SECONDS = 2
MOVE_WAIT_SECONDS = 5
MANUAL_SPEED = 30

# -------------------- LÍMITES --------------------
USER_LIMITS = {
    1: (0, 150.0),
    2: (-120.0,   0.0),
    3: (   0.0, 150.0),
    4: (-135.0, 135.0),
    5: (-120.0, 120.0),
    6: (-160.0, 160.0),
}
TOLERANCE_DEG = 5.0
COMMAND_WINDOW = {j: (mn - TOLERANCE_DEG, mx + TOLERANCE_DEG)
                for j, (mn, mx) in USER_LIMITS.items()}

def _within(lim, ang: float) -> bool:
    mn, mx = lim
    return (mn <= ang <= mx)


#--------------------------------------------------------------------------
# ----------------Funcion de lectura de angulos cada movimiento-----------
#-------------------------------------------------------------------------
def _read_angles(mc: MyCobot280, tries=6, delay=0.30):
    for _ in range(tries):
        ang = mc.get_angles()
        if isinstance(ang, (list, tuple)) and len(ang) == 6:
            try:
                return [float(x) for x in ang]
            except Exception:
                pass
        time.sleep(delay)
    return None

#---------------------------------------------------------------------------------
# ------Funcion para identificar cual sería el candidato ideal para la posición.--
#---------------------------------------------------------------------------------
def _candidate_final(base_angles: List[float], joint: int, delta: float) -> List[float]:
    cand = list(base_angles)
    cand[joint - 1] = float(base_angles[joint - 1]) + float(delta)
    return cand


#--------------------------------------------------------------------------------------------------------
# ----------------Funcion de validación con respecto a los límites (Función ángulos relativos)-----------
#--------------------------------------------------------------------------------------------------------


def _validate_relative(base_angles: List[float], joint: int, delta: float):
    """Devuelve (ok, msg, target_angles or None)."""
    current = list(base_angles)
    cur_ang = current[joint - 1]
    target = _candidate_final(base_angles, joint, delta)
    tgt_ang = target[joint - 1]

    # 1) destino debe respetar USER_LIMITS
    if not _within(USER_LIMITS[joint], tgt_ang):
        mn, mx = USER_LIMITS[joint]
        return False, (f"Destino {tgt_ang:.2f}° excede USER_LIMITS J{joint} [{mn}, {mx}]"), None

    # 2) lectura actual vs ventanas
    in_user_now = _within(USER_LIMITS[joint], cur_ang)
    in_cmd_now  = _within(COMMAND_WINDOW[joint], cur_ang)

    if in_user_now:
        return True, "OK", target

    if in_cmd_now:
        return True, f"Lectura J{joint} {cur_ang:.2f}° aceptada por ventana ±{TOLERANCE_DEG}°", target

    # 3) fuera de ventana → solo si corrige hacia el rango
    mn, mx = USER_LIMITS[joint]
    if cur_ang < mn and delta > 0:
        return True, f"J{joint} {cur_ang:.2f}° fuera; movimiento hacia el rango permitido", target
    if cur_ang > mx and delta < 0:
        return True, f"J{joint} {cur_ang:.2f}° fuera; movimiento hacia el rango permitido", target

    return False, f"J{joint} {cur_ang:.2f}° fuera de ventana y el delta no corrige.", None



class RobotController(QtCore.QObject):

    sig_log    = QtCore.Signal(str)
    sig_status = QtCore.Signal(str)
    sig_angles = QtCore.Signal(list)
    sig_error  = QtCore.Signal(str)

    def __init__(self,
                
                port: str = PORT,
                baud: int = BAUD,
                home_angles: List[float] = None,
                parent=None):
        super().__init__(parent)
        self._port = port
        self._baud = baud
        self._home = home_angles or HOME_ANGLES
        self._mc: MyCobot280 | None = None
        self._thr: threading.Thread | None = None
        self._running = False
        self._q: "queue.Queue[Tuple[str, tuple]]" = queue.Queue()
        self._last_angles: List[float] = self._home[:]

    # ---------- API ----------
    def start(self):
        if self._running:
            return
        self._running = True
        self._thr = threading.Thread(target=self._loop, daemon=True)
        self._thr.start()

    def stop(self):
        if not self._running:
            return
        self._running = False
        # Vaciar la cola sin bloquear
        try:
            while True:
                self._q.get_nowait()
        except queue.Empty:
            pass
        if self._thr:
            self._thr.join(timeout=2)
            self._thr = None

    def enqueue_actions(self, pairs: List[Tuple[int, float]]):
        """pairs = [(joint, delta_deg), ...]"""
        if not pairs:
            return
        self._q.put(("apply_actions", (pairs,)))
    
    def enqueue_absolute(self, pairs: List[Tuple[int, float]]):
        if not pairs:
            return
        self._q.put(("apply_absolute", (pairs,)))

    # ---------- Núcleo ----------
    def _loop(self):
        # Conexión y preparación
        try:
            self._mc = MyCobot280(self._port, self._baud)
            time.sleep(SETTLE_SECONDS)
            self._mc.power_on()
            self.sig_status.emit("CONNECTED")
            self.sig_log.emit("Status: CONNECTED")
        except Exception as e:
            self.sig_status.emit("FAILED")
            self.sig_error.emit(f"FAILED: {e}")
            self._running = False
            return

        # Lectura inicial
        self._emit_angles("Ángulos actuales")
        # LEDs
        try:
            colors = [(255,0,0), (0,255,0), (0,0,255)]
            for _ in range(3):
                for r, g, b in colors:
                    self._mc.set_color(r, g, b)
                    time.sleep(1)
            self.sig_log.emit("LED sequence: DONE")
        except Exception as e:
            self.sig_error.emit(f"LED error: {e}")

        # HOME
        try:
            home_ok = all(_within(USER_LIMITS[j+1], ang)
                        for j, ang in enumerate(self._home))
            if not home_ok:
                self.sig_log.emit("[WARN] HOME fuera de USER_LIMITS")
            else:
                self.sig_log.emit(f"Moviendo a HOME: {[round(a,2) for a in self._home]}")
                self._mc.send_angles(self._home, MOVE_SPEED)
                time.sleep(MOVE_WAIT_SECONDS)
                self._emit_angles("Ángulos después de HOME")
                self.sig_log.emit("HOME: DONE")
        except Exception as e:
            self.sig_error.emit(f"HOME error: {e}")

        self.sig_log.emit("Escuchando instrucciones (voz)…")

        # Bucle de acciones
        while self._running:
            try:
                msg, payload = self._q.get(timeout=0.1)
            except queue.Empty:
                continue

            if msg == "apply_actions":
                (pairs,) = payload
                self._apply_actions(pairs)
            elif msg == "apply_absolute":
                (pairs,) = payload
                self._apply_absolute(pairs)

    def _emit_angles(self, prefix="Ángulos"):
        ang = _read_angles(self._mc) if self._mc else None
        if ang:
            self._last_angles = ang
            self.sig_angles.emit(ang)
            self.sig_log.emit(f"{prefix} (deg): {[round(a,2) for a in ang]}")
        else:
            self.sig_log.emit("No fue posible leer los ángulos ahora.")

    def _apply_actions(self, pairs: List[Tuple[int, float]]):
        base = _read_angles(self._mc) or self._last_angles
        # Aviso de ventana general (informativo)
        bad = []
        for j, a in enumerate(base, start=1):
            if not _within(COMMAND_WINDOW[j], a):
                bad.append(f"J{j}={a:.2f}°∉[{COMMAND_WINDOW[j][0]}, {COMMAND_WINDOW[j][1]}]")
        if bad:
            self.sig_log.emit("[Aviso] Fuera de ventana interna: " + "; ".join(bad))

        for (joint, delta) in pairs:
            if not (1 <= joint <= 6):
                self.sig_log.emit(f"  Junta inválida: {joint} (debe ser 1..6)")
                continue

            ok, msg, target = _validate_relative(base, joint, float(delta))
            if not ok:
                self.sig_log.emit("  Movimiento bloqueado: " + msg)
                continue

            tgt = target[joint - 1]
            try:
                self._mc.send_angle(joint, tgt, MANUAL_SPEED)
                self.sig_log.emit(
                    f"  → J{joint}: {base[joint-1]:.2f}° "
                    f"{'+' if delta>=0 else ''}{delta:.2f}° ⇒ {tgt:.2f}° (vel={MANUAL_SPEED})"
                )
                time.sleep(1.0)
                base = _read_angles(self._mc) or target
                self._last_angles = base
                self.sig_angles.emit(base)
            except Exception as e:
                self.sig_error.emit(f"  Error al mover J{joint}: {e}")
                # mantener base, intentar siguiente

    def _apply_absolute(self, pairs: List[Tuple[int, float]]):
        base = _read_angles(self._mc) or self._last_angles
        for (joint, target) in pairs:
            if not (1 <= joint <= 6):
                self.sig_log.emit(f"  Junta inválida: {joint} (debe ser 1..6)")
                continue
            if not _within(USER_LIMITS[joint], float(target)):
                mn, mx = USER_LIMITS[joint]
                self.sig_log.emit(f"  Bloqueado ABS J{joint}: destino {target:.2f}° fuera de [{mn}, {mx}]")
                continue
            try:
                cur = base[joint - 1]
                self._mc.send_angle(joint, float(target), MANUAL_SPEED)
                self.sig_log.emit(f"  ABS → J{joint}: {cur:.2f}° ⇒ {float(target):.2f}° (vel={MANUAL_SPEED})")
                time.sleep(1.0)
                base = _read_angles(self._mc) or base
                self._last_angles = base
                self.sig_angles.emit(base)
            except Exception as e:
                self.sig_error.emit(f"  Error ABS J{joint}: {e}")
