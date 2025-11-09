"""
GUI y control de robot MyCobot 280 con reconocimiento de voz.

Este módulo integra:
- Cinemática directa/inversa vía `roboticstoolbox` (modelo DH).
- Planificación simple de trayectoria cartesiana (línea) resolviendo IK por punto.
- Interfaz Qt (PySide6) con gráfico 3D embebido (matplotlib).
- Encolado de acciones absolutas/relativas hacia `RobotController`.
- Reconocimiento de voz en streaming para comandos (por `StreamingRecognizer`).

Style:
- Docstrings en formato NumPy (numpydoc).
- Comentarios en línea concisos y orientados a lectura de mantenimiento.
- Nombres de símbolos autoexplicativos cuando es posible.

Referencias:
- Google Python Style Guide (comentarios/docstrings).  # ver README de repo
- numpydoc: guía de docstrings estilo NumPy.
- pandas docstring guide (aplicaciones prácticas).
"""

import sys
from dataclasses import dataclass
from typing import List, Tuple

import numpy as np
import roboticstoolbox as rtb
from spatialmath import SE3

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QMessageBox,
    QDialog, QVBoxLayout, QMenu, QPushButton
)
from PySide6.QtCore import Qt, Signal, QEvent
from PySide6.QtGui import QCloseEvent, QTextCursor

from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qtagg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

from robot_controller import HOME_ANGLES, RobotController
from grafico_ui import Ui_MainWindow
from speech_parser import StreamingRecognizer


# ----------------- MODELO DH (en metros) -----------------
@dataclass
class LinkDH:
    """Contenedor para parámetros DH de un eslabón.

    Parameters
    ----------
    d : float
        Desplazamiento a lo largo de z_{i-1} [m].
    a : float
        Longitud del eslabón a lo largo de x_{i} [m].
    alpha : float
        Ángulo de torsión entre z_{i-1} y z_{i} [rad].
    offset : float, default=0.0
        Offset articular (desfase en q_i) [rad].
    """
    d: float
    a: float
    alpha: float
    offset: float = 0.0


def _robot_from_teammate_DH() -> rtb.DHRobot:
    """Construye el modelo DH (myCobot 280) con parámetros proporcionados.

    Returns
    -------
    rtb.DHRobot
        Robot DH con 6 juntas revolutas.

    Notes
    -----
    - Las dimensiones vienen en mm y se convierten a metros (escala `mm = 1e-3`).
    - Los offsets reflejan la convención usada por el compañero/teammate.
    - Usamos `RevoluteDH` por consistencia con RTB.
    """
    mm = 1e-3
    # Parámetros DH (verificados contra fuente del equipo)
    d1, a1, alpha1, offset1 = 131.22*mm,   0*mm, +np.pi/2,  0
    d2, a2, alpha2, offset2 =   0.00*mm, -110.4*mm, 0,     -np.pi/2
    d3, a3, alpha3, offset3 =   0.00*mm,  -96.0*mm, 0,      0
    d4, a4, alpha4, offset4 =  63.40*mm,   0*mm,  +np.pi/2, -np.pi/2
    d5, a5, alpha5, offset5 =  75.05*mm,   0*mm,  -np.pi/2, +np.pi/2
    d6, a6, alpha6, offset6 =  45.60*mm,   0*mm,   0,        0

    # Eslabones revolutos
    L1 = rtb.RevoluteDH(d=d1, a=a1, alpha=alpha1, offset=offset1)
    L2 = rtb.RevoluteDH(d=d2, a=a2, alpha=alpha2, offset=offset2)
    L3 = rtb.RevoluteDH(d=d3, a=a3, alpha=alpha3, offset=offset3)
    L4 = rtb.RevoluteDH(d=d4, a=a4, alpha=alpha4, offset=offset4)
    L5 = rtb.RevoluteDH(d=d5, a=a5, alpha=alpha5, offset=offset5)
    L6 = rtb.RevoluteDH(d=d6, a=a6, alpha=alpha6, offset=offset6)
    return rtb.DHRobot([L1, L2, L3, L4, L5, L6], name="myCobot")


def get_robot() -> rtb.DHRobot:
    """Devuelve la instancia del robot DH.

    Returns
    -------
    rtb.DHRobot
        Modelo DH del myCobot 280.

    See Also
    --------
    _robot_from_teammate_DH : Constructor base del modelo.
    """
    return _robot_from_teammate_DH()


def fk(q_deg: List[float]) -> SE3:
    """Cinemática directa (FK) desde ángulos en grados.

    Parameters
    ----------
    q_deg : list of float
        Ángulos articulares [deg], longitud 6.

    Returns
    -------
    SE3
        Pose homogénea del TCP respecto a la base.
    """
    robot = get_robot()
    q = np.radians(q_deg)
    return robot.fkine(q)


def ik(target: SE3, q0_deg: List[float] = None) -> np.ndarray:
    """Cinemática inversa (IK) por Levenberg–Marquardt.

    Parameters
    ----------
    target : SE3
        Pose objetivo homogénea.
    q0_deg : list of float, optional
        Semilla en grados; si es None usa heurística interna de RTB.

    Returns
    -------
    numpy.ndarray
        Solución en radianes (vector q).

    Notes
    -----
    - `ikine_LM` puede retornar múltiples info; aquí devolvemos `sol.q`.
    - No se fijan límites articulares aquí; se asume validados a otro nivel.
    """
    robot = get_robot()
    q0 = None if q0_deg is None else np.radians(q0_deg)
    sol = robot.ikine_LM(target, q0=q0)
    return sol.q


def plan_line(q_start_deg: List[float], d_xyz: Tuple[float, float, float], steps: int = 100):
    """Interpola una línea cartesiana y resuelve IK punto a punto.

    Parameters
    ----------
    q_start_deg : list of float
        Configuración inicial (grados).
    d_xyz : tuple of float
        Desplazamiento cartesiano (dx, dy, dz) [m] desde la pose inicial.
    steps : int, default=100
        Discretización de la trayectoria.

    Returns
    -------
    list of numpy.ndarray
        Lista de configuraciones en radianes (una por `steps`).

    Warnings
    --------
    - No hay verificación de colisiones/alcances ni límites articulares.
    - La convergencia de IK depende de la semilla; usamos warm-start con `qseed`.

    See Also
    --------
    rtb.ctraj : Interpolador cartesiano.
    """
    robot = get_robot()
    q0 = np.radians(q_start_deg)
    T0 = robot.fkine(q0)
    T1 = T0 * SE3(d_xyz[0], d_xyz[1], d_xyz[2])
    Ts = rtb.ctraj(T0, T1, steps)
    qs = []
    qseed = q0.copy()
    for Tk in Ts:
        sol = robot.ikine_LM(Tk, q0=qseed)
        qseed = sol.q
        qs.append(qseed)
    return qs


# ================== MAIN WINDOW ==================
class MainWindow(QMainWindow, Ui_MainWindow):
    """Ventana principal de la GUI para control y visualización 3D.

    Señales
    -------
    sig_live : Signal(str)
        Texto parcial del reconocimiento (LIVE).
    sig_final : Signal(str)
        Texto final del reconocimiento.
    sig_action : Signal(list)
        Acciones parseadas (modo, HOME, ABS/REL, confirmaciones).
    sig_error : Signal(str)
        Mensajes de error del pipeline STT.

    Notas
    -----
    - Inicia `RobotController` en un hilo propio; recibe callbacks de estado
      y ángulos para actualizar etiquetas y la vista 3D.
    - El botón de audio gestiona `StreamingRecognizer` con callbacks Qt-safe.
    """

    # Señales del STT
    sig_live   = Signal(str)
    sig_final  = Signal(str)
    sig_action = Signal(list)
    sig_error  = Signal(str)

    def __init__(self):
        """Configura UI, gráfico 3D, controlador del robot y STT."""
        super().__init__()
        self.setupUi(self)
        self._last_q_deg = None  # memoria de la última pose en grados

        # Gráfico 3D
        self._init_robot_plot()

        # === Pose inicial en HOME (visual) ===
        try:
            self._last_q_deg = list(map(float, HOME_ANGLES))
            self._set_joint_labels(self._last_q_deg)     # etiquetas en HOME
            self._update_robot_plot(self._last_q_deg)    # dibujo en HOME
        except Exception:
            # Si HOME_ANGLES no está disponible o falla la conversión
            pass

        # Botonera / modos
        self.pushButton_4.clicked.connect(self._home_clicked)
        self.radioButton_2.setChecked(True)         # modo relativo por defecto
        self.Absoluto.setAutoExclusive(True)
        self.radioButton_2.setAutoExclusive(True)

        # Controlador del robot (hilo)
        self.robot = RobotController()
        self.robot.sig_status.connect(self._status)
        self.robot.sig_angles.connect(self._angles)   # ← actualiza labels + 3D
        self.robot.sig_error.connect(self._error)
        self.robot.start()

        # Reconocedor (voz)
        self.pushButton_2.clicked.connect(self.toggle_recognition)
        self.sig_live.connect(self._update_live)
        self.sig_final.connect(lambda t: self.textBrowser.append(f"[FIN]  {t}\n"))
        self.sig_action.connect(self._handle_actions)
        self.sig_error.connect(lambda e: self.textBrowser.append(f"[ERROR] {e}\n"))

        self._recognizer = None
        self._running    = False
        self._require_confirm = True
        self._pending_abs: list[tuple[int, float]] = []
        self._pending_home = False

        self.textBrowser.append("Inicializando robot…\n")
        # Si prefieres arrancar con “—” en etiquetas, comenta la línea superior y descomenta:
        # self._set_joint_labels(None)

    # ----------------- GRAFICO 3D -----------------
    def _init_robot_plot(self):
        """Crea la figura 3D y configura estética/controles básicos."""
        # Figura y eje 3D
        self._fig3d = Figure(figsize=(4.6, 1.8), tight_layout=True)
        self._ax3d = self._fig3d.add_subplot(1, 1, 1, projection="3d")
        self._ax3d.set_title("MyCobot 280 — Pose actual")
        self._ax3d.set_xlabel("X [m]"); self._ax3d.set_ylabel("Y [m]"); self._ax3d.set_zlabel("Z [m]")

        # Canvas embebido
        self._canvas3d = FigureCanvas(self._fig3d)
        self._canvas3d.setParent(self.centralwidget)
        self._canvas3d.setGeometry(490, 15, 461, 210)

        # Modelo RTB para FK all (evita reconstruir cada vez)
        self._rtb_robot = get_robot()

        # Estética base
        self._ax3d.view_init(elev=25, azim=-60)
        self._ax3d.grid(True, alpha=0.25)
        for axis in (self._ax3d.xaxis, self._ax3d.yaxis, self._ax3d.zaxis):
            axis.pane.set_alpha(0.06)

        # Segmentos y juntas (grosor y colores legibles en proyector)
        self._seg_colors = ["#e74c3c", "#27ae60", "#2980b9", "#f39c12", "#8e44ad", "#16a085"]
        self._segments = []
        self._joint_scat = None

        # Límites iniciales (vista compacta de trabajo)
        self._set_equal_3d_limits([-0.35, 0.35], [-0.35, 0.35], [0.0, 0.45])
        self._canvas3d.draw_idle()

        # ---- Interacción / Fullscreen ----
        self._btn_max = QPushButton("⤢", self.centralwidget)
        self._btn_max.setToolTip("Ampliar gráfico 3D")
        self._btn_max.setFixedSize(36, 36)
        self._btn_max.setStyleSheet(
            "QPushButton{background:#f6e6c3;border:2px solid #d9a441;"
            "border-radius:10px;padding:2px 4px;color:#1e1a11;font-size:20px;font-weight:800;}"
            "QPushButton:disabled{background:#e5d6b9;color:#7a7363;border-color:#c9a739;}"
        )
        g = self._canvas3d.geometry()
        self._btn_max.setGeometry(g.right()-40, g.top()+6, 36, 36)
        self._btn_max.clicked.connect(self._open_plot_dialog)
        self._btn_max.raise_()

        # Menú contextual y doble clic para ampliar
        self._canvas3d.setContextMenuPolicy(Qt.CustomContextMenu)
        self._canvas3d.customContextMenuRequested.connect(self._plot_context_menu)
        self._canvas3d.installEventFilter(self)

    def _plot_context_menu(self, pos):
        """Menú contextual de la figura 3D (vistas rápidas + reset)."""
        m = QMenu(self)
        m.addAction("Maximizar", self._open_plot_dialog)
        m.addSeparator()
        m.addAction("Vista isométrica", lambda: self._set_view(25, -60))
        m.addAction("Vista superior",  lambda: self._set_view(90,   0))
        m.addAction("Vista frontal",   lambda: self._set_view(0,    0))
        m.addAction("Vista lateral",   lambda: self._set_view(0,   90))
        m.addSeparator()
        m.addAction("Reset (Home)", self._home_view)
        m.exec(self._canvas3d.mapToGlobal(pos))

    def _set_view(self, elev, azim):
        """Ajusta la vista (elevación/azimut) y refresca."""
        self._ax3d.view_init(elev=elev, azim=azim)
        self._canvas3d.draw_idle()

    def _home_view(self):
        """Restaura la vista por defecto y redibuja la pose almacenada."""
        self._set_view(25, -60)
        if self._last_q_deg:
            self._update_robot_plot(self._last_q_deg)

    def eventFilter(self, obj, event):
        """Permite ampliar con doble clic el canvas 3D."""
        if obj is self._canvas3d and event.type() == QEvent.MouseButtonDblClick:
            self._open_plot_dialog()
            return True
        return super().eventFilter(obj, event)

    def _open_plot_dialog(self):
        """Mueve el canvas a un diálogo grande con toolbar y restaura al cerrar."""
        # Si ya hay diálogo visible, solo enfocarlo
        if getattr(self, "_plot_dialog", None) and self._plot_dialog.isVisible():
            self._plot_dialog.raise_(); self._plot_dialog.activateWindow(); return

        dlg = QDialog(self)
        dlg.setWindowTitle("Vista 3D — MyCobot")
        dlg.resize(900, 650)
        lay = QVBoxLayout(dlg)

        toolbar = NavigationToolbar(self._canvas3d, dlg)
        lay.addWidget(toolbar)
        lay.addWidget(self._canvas3d)

        # No ocultes: deshabilita, así no “desaparece” por Z-order
        self._btn_max.setEnabled(False)

        def _restore():
            # Volver a poner el canvas en su sitio
            self._canvas3d.setParent(self.centralwidget)
            self._canvas3d.setGeometry(490, 15, 461, 210)
            self._canvas3d.show()
            g = self._canvas3d.geometry()
            self._btn_max.setGeometry(g.right()-40, g.top()+6, 36, 36)
            self._btn_max.setEnabled(True)
            self._btn_max.raise_()

        dlg.finished.connect(_restore)
        self._plot_dialog = dlg
        dlg.show()

    def _set_equal_3d_limits(self, xlim, ylim, zlim):
        """Fija límites con misma escala para evitar distorsión visual."""
        self._ax3d.set_xlim(xlim[0], xlim[1])
        self._ax3d.set_ylim(ylim[0], ylim[1])
        self._ax3d.set_zlim(zlim[0], zlim[1])
        xr = xlim[1] - xlim[0]; yr = ylim[1] - ylim[0]; zr = zlim[1] - zlim[0]
        maxr = max(xr, yr, zr)
        cx = sum(xlim)/2; cy = sum(ylim)/2; cz = sum(zlim)/2
        self._ax3d.set_xlim(cx - maxr/2, cx + maxr/2)
        self._ax3d.set_ylim(cy - maxr/2, cy + maxr/2)
        self._ax3d.set_zlim(cz - maxr/2, cz + maxr/2)

    def _compute_positions_fkine_all(self, q_deg: List[float]):
        """Devuelve la lista de posiciones de cada frame desde base a TCP.

        Parameters
        ----------
        q_deg : list of float
            Configuración articular en grados.

        Returns
        -------
        list of numpy.ndarray
            Puntos 3D (x, y, z) en metros, incluyendo base y TCP.

        Notes
        -----
        - Usa `fkine_all` de RTB, luego extrae `Ti.t` (traslaciones).
        """
        q = np.radians(q_deg)
        Tlist = self._rtb_robot.fkine_all(q)
        pts = [np.array([0.0, 0.0, 0.0])]
        for Ti in Tlist:
            p = np.asarray(Ti.t).reshape(-1)
            pts.append(np.array([float(p[0]), float(p[1]), float(p[2])]))
        return pts

    def _ensure_segments(self, n_segments: int):
        """Crea líneas 3D coloreadas según el número de eslabones.

        Rehace el eje manteniendo estilo si cambia `n_segments`.
        """
        if len(self._segments) == n_segments:
            return
        # Reset del eje manteniendo estilo
        self._ax3d.cla()
        self._ax3d.set_title("MyCobot 280 — Pose actual")
        self._ax3d.set_xlabel("X [m]"); self._ax3d.set_ylabel("Y [m]"); self._ax3d.set_zlabel("Z [m]")
        self._ax3d.view_init(elev=25, azim=-60)
        self._ax3d.grid(True, alpha=0.25)
        for axis in (self._ax3d.xaxis, self._ax3d.yaxis, self._ax3d.zaxis):
            axis.pane.set_alpha(0.06)

        self._segments = []
        for i in range(n_segments):
            (line,) = self._ax3d.plot(
                [], [], [], linewidth=6, solid_capstyle="round",   # más grueso = mejor visibilidad
                color=self._seg_colors[i % len(self._seg_colors)]
            )
            self._segments.append(line)
        self._joint_scat = None  # se recrea en cada update

    def _update_robot_plot(self, q_deg: List[float]):
        """Actualiza la geometría 3D (segmentos + juntas) según `q_deg`."""
        pts = self._compute_positions_fkine_all(q_deg)
        xs = [p[0] for p in pts]; ys = [p[1] for p in pts]; zs = [p[2] for p in pts]
        n_segments = max(0, len(pts) - 1)
        self._ensure_segments(n_segments)

        # Actualizar segmentos
        for i in range(n_segments):
            self._segments[i].set_data([xs[i], xs[i+1]], [ys[i], ys[i+1]])
            self._segments[i].set_3d_properties([zs[i], zs[i+1]])

        # Juntas (discos/puntos más grandes)
        if self._joint_scat is not None:
            self._joint_scat.remove()
        self._joint_scat = self._ax3d.scatter(xs, ys, zs, s=40, c="#2c3e50", depthshade=True)

        # Auto-límites suaves para mantener el robot centrado
        pad = 0.03
        xmin, xmax = min(xs)-pad, max(xs)+pad
        ymin, ymax = min(ys)-pad, max(ys)+pad
        zmin, zmax = min(zs)-pad, max(zs)+pad
        self._set_equal_3d_limits([xmin, xmax], [ymin, ymax], [zmin, zmax])

        self._canvas3d.draw_idle()

    # ----------------- Labels -----------------
    def _set_joint_labels(self, angles):
        """Escribe los valores articulares en la UI (o “—” si no disponibles)."""
        def fmt(a): return f"{a:.2f}°" if a is not None else "—"
        if not angles or len(angles) != 6:
            vals = [None]*6
        else:
            vals = angles
        self.ValorJ1.setText(fmt(vals[0])); self.ValorJ2.setText(fmt(vals[1])); self.ValorJ3.setText(fmt(vals[2]))
        self.ValorJ4.setText(fmt(vals[3])); self.ValorJ5.setText(fmt(vals[4])); self.ValorJ6.setText(fmt(vals[5]))

    # ----------------- Slots de robot -----------------
    def _home_clicked(self):
        """Dialoga confirmación y envía HOME al controlador si el usuario acepta."""
        resp = QMessageBox.question(
            self, "Confirmar HOME",
            "¿Mover el robot a la posición HOME?",
            QMessageBox.Yes | QMessageBox.No
        )
        if resp == QMessageBox.Yes:
            pairs = [(i+1, float(HOME_ANGLES[i])) for i in range(6)]
            self.textBrowser.append(f"[ABS] HOME → {pairs}\n")
            self.robot.enqueue_absolute(pairs)

    def _status(self, s: str):
        """Callback de estado del controlador."""
        self.textBrowser.append(f"Status: {s}\n")

    def _angles(self, ang_list):
        """Callback de ángulos: actualiza labels y dibujo 3D."""
        self._set_joint_labels(ang_list)
        if not ang_list or len(ang_list) != 6:
            return
        self._last_q_deg = ang_list[:]
        try:
            self._update_robot_plot(ang_list)
        except Exception as e:
            self.textBrowser.append(f"[PLOT] error al actualizar 3D: {e}\n")

    def _error(self, e: str):
        """Callback de error del controlador."""
        self.textBrowser.append(f"[ERROR] {e}\n")

    def _enqueue_home(self):
        """Encola HOME sin diálogo (usado por confirmación por voz)."""
        pairs = [(i+1, float(HOME_ANGLES[i])) for i in range(6)]
        self.textBrowser.append(f"[ABS] HOME → {pairs}\n")
        self.robot.enqueue_absolute(pairs)

    # ----------------- STT live/final -----------------
    def _update_live(self, texto: str):
        """Muestra el texto LIVE del STT (mantiene solo una línea LIVE)."""
        contenido = self.textBrowser.toPlainText()
        lineas = [l for l in contenido.splitlines() if not l.startswith("[LIVE]")]
        lineas.append(f"[LIVE] {texto}")
        self.textBrowser.setPlainText("\n".join(lineas))
        cursor = self.textBrowser.textCursor()
        cursor.movePosition(QTextCursor.End)
        self.textBrowser.setTextCursor(cursor)

    def _handle_actions(self, actions: list):
        """Gestiona acciones parseadas desde voz (ABS/REL, HOME, confirm/cancel).

        Parameters
        ----------
        actions : list
            Lista heterogénea con tuplas del tipo:
            - ("MODE", "absolute"|"relative")
            - ("CONFIRM",)
            - ("CANCEL",)
            - ("CONFREQ", bool)
            - ("HOME",)
            - ("REL", j:int, delta_deg:float)
            - ("ABS", j:int, target_deg:float)
        """
        if not actions:
            self.textBrowser.append("Sin órdenes\n")
            return

        rel_pairs = []
        abs_pairs_instant = []

        for act in actions:
            if isinstance(act, tuple) and act and act[0] == "MODE":
                _, m = act
                if m == "absolute":
                    self.Absoluto.setChecked(True); self.radioButton_2.setChecked(False)
                    self.textBrowser.append("[MODO] Cambiado a ABSOLUTO\n")
                else:
                    self.radioButton_2.setChecked(True); self.Absoluto.setChecked(False)
                    self.textBrowser.append("[MODO] Cambiado a RELATIVO\n")
                continue

            if isinstance(act, tuple) and act and act[0] == "CONFIRM":
                if self._pending_home:
                    self._pending_home = False
                    self.textBrowser.append("[HOME] Confirmado por voz\n")
                    self._enqueue_home()
                if self._pending_abs:
                    to_send = self._pending_abs[:]
                    self._pending_abs.clear()
                    self.textBrowser.append(f"[ABS] Confirmado por voz → {to_send}\n")
                    self.robot.enqueue_absolute(to_send)
                continue

            if isinstance(act, tuple) and act and act[0] == "CANCEL":
                if self._pending_home or self._pending_abs:
                    self._pending_home = False
                    self._pending_abs.clear()
                    self.textBrowser.append("[CANCEL] Se descartaron órdenes pendientes\n")
                else:
                    self.textBrowser.append("[CANCEL] No había pendientes\n")
                continue

            if isinstance(act, tuple) and act and act[0] == "CONFREQ":
                _, val = act
                self._require_confirm = bool(val)
                self.textBrowser.append(
                    "[CONF] Confirmación por voz "
                    + ("ACTIVADA (se requerirá 'confirma')" if self._require_confirm else "DESACTIVADA (auto-ejecuta)")
                    + "\n"
                )
                continue

            if isinstance(act, tuple) and act and act[0] == "HOME":
                if self._require_confirm:
                    self._pending_home = True
                    self.textBrowser.append("[HOME] Pendiente de confirmación (di: 'confirma' o 'cancela')\n")
                else:
                    self.textBrowser.append("[HOME] Ejecutando (sin confirmación)\n")
                    self._enqueue_home()
                continue

            if isinstance(act, tuple) and len(act) == 3 and act[0] == "REL":
                _, j, d = act
                rel_pairs.append((int(j), float(d)))
                continue

            if isinstance(act, tuple) and len(act) == 3 and act[0] == "ABS":
                _, j, angle = act
                j = int(j); target = float(angle)
                if self._require_confirm:
                    self._pending_abs.append((j, target))
                    self.textBrowser.append(
                        f"[ABS] Pendiente J{j} → {target:.2f}° (di: 'confirma' o 'cancela')\n"
                    )
                else:
                    abs_pairs_instant.append((j, target))
                continue

            # Fallback de depuración si llega un token no previsto
            self.textBrowser.append(f"[DBG] Acción no reconocida: {act}\n")

        if rel_pairs:
            self.textBrowser.append(f"[REL] → {rel_pairs}\n")
            self.robot.enqueue_actions(rel_pairs)

        if abs_pairs_instant:
            self.textBrowser.append(f"[ABS] (sin confirmación) → {abs_pairs_instant}\n")
            self.robot.enqueue_absolute(abs_pairs_instant)

    # ----------------- Botón de audio -----------------
    def toggle_recognition(self):
        """Alterna el reconocimiento de voz (start/stop) y actualiza el texto del botón."""
        if not self._running:
            self._start_recognition()
            self.pushButton_2.setText("Apagar")
        else:
            self._stop_recognition()
            self.pushButton_2.setText("Encender")

    def _start_recognition(self):
        """Inicializa `StreamingRecognizer` y engancha callbacks a señales Qt."""
        self.textBrowser.append("Escuchando instrucciones (voz)…\n")
        self._recognizer = StreamingRecognizer(
            on_live   = self.sig_live.emit,
            on_final  = self.sig_final.emit,
            on_action = self.sig_action.emit,
            on_error  = lambda e: self.sig_error.emit(str(e)),
            mode_provider = lambda: ("absolute" if self.Absoluto.isChecked() else "relative")
        )
        self._recognizer.start()
        self._running = True

    def _stop_recognition(self):
        """Detiene el reconocimiento en curso (si existe) y notifica en UI."""
        if self._recognizer:
            self._recognizer.stop()
            self._recognizer = None
        self._running = False
        self.textBrowser.append("Reconocimiento detenido.\n")

    # ----------------- Redimensionado / cierre -----------------
    def resizeEvent(self, event):
        """Mantiene el botón “max” alineado con el canvas al redimensionar."""
        super().resizeEvent(event)
        if hasattr(self, "_btn_max") and hasattr(self, "_canvas3d"):
            g = self._canvas3d.geometry()
            self._btn_max.setGeometry(g.right()-40, g.top()+6, 36, 36)
            self._btn_max.raise_()  # asegurar visibilidad

    def closeEvent(self, event: QCloseEvent):
        """Cierra limpiamente: detiene STT y controlador del robot."""
        self._stop_recognition()
        try:
            self.robot.stop()
        except Exception:
            pass
        event.accept()


if __name__ == "__main__":
    # Punto de entrada de la aplicación Qt
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec())
