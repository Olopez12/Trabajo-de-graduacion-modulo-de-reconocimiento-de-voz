# Gui_app_Brazo.py
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
    d: float
    a: float
    alpha: float
    offset: float = 0.0

def _robot_from_teammate_DH() -> rtb.DHRobot:
    mm = 1e-3
    d1, a1, alpha1, offset1 = 131.22*mm,   0*mm, +np.pi/2,  0
    d2, a2, alpha2, offset2 =   0.00*mm, -110.4*mm, 0,     -np.pi/2
    d3, a3, alpha3, offset3 =   0.00*mm,  -96.0*mm, 0,      0
    d4, a4, alpha4, offset4 =  63.40*mm,   0*mm,  +np.pi/2, -np.pi/2
    d5, a5, alpha5, offset5 =  75.05*mm,   0*mm,  -np.pi/2, +np.pi/2
    d6, a6, alpha6, offset6 =  45.60*mm,   0*mm,   0,        0

    L1 = rtb.RevoluteDH(d=d1, a=a1, alpha=alpha1, offset=offset1)
    L2 = rtb.RevoluteDH(d=d2, a=a2, alpha=alpha2, offset=offset2)
    L3 = rtb.RevoluteDH(d=d3, a=a3, alpha=alpha3, offset=offset3)
    L4 = rtb.RevoluteDH(d=d4, a=a4, alpha=alpha4, offset=offset4)
    L5 = rtb.RevoluteDH(d=d5, a=a5, alpha=alpha5, offset=offset5)
    L6 = rtb.RevoluteDH(d=d6, a=a6, alpha=alpha6, offset=offset6)
    return rtb.DHRobot([L1, L2, L3, L4, L5, L6], name="myCobot")

def get_robot() -> rtb.DHRobot:
    return _robot_from_teammate_DH()

def fk(q_deg: List[float]) -> SE3:
    robot = get_robot()
    q = np.radians(q_deg)
    return robot.fkine(q)

def ik(target: SE3, q0_deg: List[float] = None) -> np.ndarray:
    robot = get_robot()
    q0 = None if q0_deg is None else np.radians(q0_deg)
    sol = robot.ikine_LM(target, q0=q0)
    return sol.q

def plan_line(q_start_deg: List[float], d_xyz: Tuple[float, float, float], steps: int = 100):
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
    # Señales del STT
    sig_live   = Signal(str)
    sig_final  = Signal(str)
    sig_action = Signal(list)
    sig_error  = Signal(str)

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self._last_q_deg = None

        # Gráfico 3D
        self._init_robot_plot()

        # === Pose inicial en HOME (visual) ===
        try:
            self._last_q_deg = list(map(float, HOME_ANGLES))
            self._set_joint_labels(self._last_q_deg)     # etiquetas en HOME
            self._update_robot_plot(self._last_q_deg)    # dibujo en HOME
        except Exception:
            pass

        # Botonera
        self.pushButton_4.clicked.connect(self._home_clicked)
        self.radioButton_2.setChecked(True)
        self.Absoluto.setAutoExclusive(True)
        self.radioButton_2.setAutoExclusive(True)

        # Controlador del robot
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
        # Figura y eje 3D
        self._fig3d = Figure(figsize=(4.6, 1.8), tight_layout=True)
        self._ax3d = self._fig3d.add_subplot(1, 1, 1, projection="3d")
        self._ax3d.set_title("MyCobot 280 — Pose actual")
        self._ax3d.set_xlabel("X [m]"); self._ax3d.set_ylabel("Y [m]"); self._ax3d.set_zlabel("Z [m]")

        # Canvas embebido
        self._canvas3d = FigureCanvas(self._fig3d)
        self._canvas3d.setParent(self.centralwidget)
        self._canvas3d.setGeometry(490, 15, 461, 210)

        # Modelo RTB
        self._rtb_robot = get_robot()

        # Estética base
        self._ax3d.view_init(elev=25, azim=-60)
        self._ax3d.grid(True, alpha=0.25)
        for axis in (self._ax3d.xaxis, self._ax3d.yaxis, self._ax3d.zaxis):
            axis.pane.set_alpha(0.06)

        # Segmentos y juntas (más grueso / visible)
        self._seg_colors = ["#e74c3c", "#27ae60", "#2980b9", "#f39c12", "#8e44ad", "#16a085"]
        self._segments = []
        self._joint_scat = None

        # Límites iniciales
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

        # Menú contextual
        self._canvas3d.setContextMenuPolicy(Qt.CustomContextMenu)
        self._canvas3d.customContextMenuRequested.connect(self._plot_context_menu)

        # Doble clic = ampliar
        self._canvas3d.installEventFilter(self)

    def _plot_context_menu(self, pos):
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
        self._ax3d.view_init(elev=elev, azim=azim)
        self._canvas3d.draw_idle()

    def _home_view(self):
        self._set_view(25, -60)
        if self._last_q_deg:
            self._update_robot_plot(self._last_q_deg)

    def eventFilter(self, obj, event):
        if obj is self._canvas3d and event.type() == QEvent.MouseButtonDblClick:
            self._open_plot_dialog()
            return True
        return super().eventFilter(obj, event)

    def _open_plot_dialog(self):
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

        # En lugar de ocultar el botón, lo deshabilitamos para que NUNCA desaparezca
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
        """Posiciones de la cadena (base→TCP) usando fkine_all."""
        q = np.radians(q_deg)
        Tlist = self._rtb_robot.fkine_all(q)
        pts = [np.array([0.0, 0.0, 0.0])]
        for Ti in Tlist:
            p = np.asarray(Ti.t).reshape(-1)
            pts.append(np.array([float(p[0]), float(p[1]), float(p[2])]))
        return pts

    def _ensure_segments(self, n_segments: int):
        """Crea (si hace falta) n segmentos de colores y guarda los Line3D."""
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
                [], [], [], linewidth=6, solid_capstyle="round",   # ← más grueso
                color=self._seg_colors[i % len(self._seg_colors)]
            )
            self._segments.append(line)
        self._joint_scat = None  # se recrea en cada update

    def _update_robot_plot(self, q_deg: List[float]):
        pts = self._compute_positions_fkine_all(q_deg)
        xs = [p[0] for p in pts]; ys = [p[1] for p in pts]; zs = [p[2] for p in pts]
        n_segments = max(0, len(pts) - 1)
        self._ensure_segments(n_segments)

        # Actualizar “palitos”
        for i in range(n_segments):
            self._segments[i].set_data([xs[i], xs[i+1]], [ys[i], ys[i+1]])
            self._segments[i].set_3d_properties([zs[i], zs[i+1]])

        # Juntas (bolas más grandes)
        if self._joint_scat is not None:
            self._joint_scat.remove()
        self._joint_scat = self._ax3d.scatter(xs, ys, zs, s=40, c="#2c3e50", depthshade=True)

        # Auto-límites suaves
        pad = 0.03
        xmin, xmax = min(xs)-pad, max(xs)+pad
        ymin, ymax = min(ys)-pad, max(ys)+pad
        zmin, zmax = min(zs)-pad, max(zs)+pad
        self._set_equal_3d_limits([xmin, xmax], [ymin, ymax], [zmin, zmax])

        self._canvas3d.draw_idle()

    # ----------------- Labels -----------------
    def _set_joint_labels(self, angles):
        def fmt(a): return f"{a:.2f}°" if a is not None else "—"
        if not angles or len(angles) != 6:
            vals = [None]*6
        else:
            vals = angles
        self.ValorJ1.setText(fmt(vals[0])); self.ValorJ2.setText(fmt(vals[1])); self.ValorJ3.setText(fmt(vals[2]))
        self.ValorJ4.setText(fmt(vals[3])); self.ValorJ5.setText(fmt(vals[4])); self.ValorJ6.setText(fmt(vals[5]))

    # ----------------- Slots de robot -----------------
    def _home_clicked(self):
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
        self.textBrowser.append(f"Status: {s}\n")

    def _angles(self, ang_list):
        self._set_joint_labels(ang_list)
        if not ang_list or len(ang_list) != 6:
            return
        self._last_q_deg = ang_list[:]
        try:
            self._update_robot_plot(ang_list)
        except Exception as e:
            self.textBrowser.append(f"[PLOT] error al actualizar 3D: {e}\n")

    def _error(self, e: str):
        self.textBrowser.append(f"[ERROR] {e}\n")

    def _enqueue_home(self):
        pairs = [(i+1, float(HOME_ANGLES[i])) for i in range(6)]
        self.textBrowser.append(f"[ABS] HOME → {pairs}\n")
        self.robot.enqueue_absolute(pairs)

    # ----------------- STT live/final -----------------
    def _update_live(self, texto: str):
        contenido = self.textBrowser.toPlainText()
        lineas = [l for l in contenido.splitlines() if not l.startswith("[LIVE]")]
        lineas.append(f"[LIVE] {texto}")
        self.textBrowser.setPlainText("\n".join(lineas))
        cursor = self.textBrowser.textCursor()
        cursor.movePosition(QTextCursor.End)
        self.textBrowser.setTextCursor(cursor)

    def _handle_actions(self, actions: list):
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

            self.textBrowser.append(f"[DBG] Acción no reconocida: {act}\n")

        if rel_pairs:
            self.textBrowser.append(f"[REL] → {rel_pairs}\n")
            self.robot.enqueue_actions(rel_pairs)

        if abs_pairs_instant:
            self.textBrowser.append(f"[ABS] (sin confirmación) → {abs_pairs_instant}\n")
            self.robot.enqueue_absolute(abs_pairs_instant)

    # ----------------- Botón de audio -----------------
    def toggle_recognition(self):
        if not self._running:
            self._start_recognition()
            self.pushButton_2.setText("Apagar")
        else:
            self._stop_recognition()
            self.pushButton_2.setText("Encender")

    def _start_recognition(self):
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
        if self._recognizer:
            self._recognizer.stop()
            self._recognizer = None
        self._running = False
        self.textBrowser.append("Reconocimiento detenido.\n")

    # ----------------- Redimensionado / cierre -----------------
    def resizeEvent(self, event):
        super().resizeEvent(event)
        if hasattr(self, "_btn_max") and hasattr(self, "_canvas3d"):
            g = self._canvas3d.geometry()
            self._btn_max.setGeometry(g.right()-40, g.top()+6, 36, 36)
            self._btn_max.raise_()  # ← aseguramos que se vea siempre

    def closeEvent(self, event: QCloseEvent):
        self._stop_recognition()
        try:
            self.robot.stop()
        except Exception:
            pass
        event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec())
            