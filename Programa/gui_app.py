"""
GUI mínima para transcripción en vivo y acciones parseadas desde voz.

Este módulo crea una ventana Qt (PySide6) que:
- Inicia/detiene un reconocedor de voz en streaming (`StreamingRecognizer`).
- Muestra la transcripción parcial ([LIVE]) reescribiendo siempre la última línea.
- Muestra transcripción final ([FIN]) y lista de acciones interpretadas.
- Gestiona errores del pipeline de voz.

Estilo aplicado:
- Docstrings formato NumPy (numpydoc) en clase y métodos públicos.
- Comentarios en línea concisos, centrados en el “por qué”.
- Sin cambios de lógica respecto al original.

Referencias de estilo:
- Google Python Style Guide (comentarios/docstrings) — google/styleguide
- numpydoc (formato de docstrings NumPy) — numpy/numpydoc
- pandas docstring guide (prácticas aplicadas) — pandas-dev/pandas
- pydocstyle (convenciones PEP 257) — PyCQA/pydocstyle
"""

import sys
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtCore    import Qt, Signal
from PySide6.QtGui     import QCloseEvent, QTextCursor

from grafico_ui import Ui_MainWindow
from speech_parser import StreamingRecognizer


class MainWindow(QMainWindow, Ui_MainWindow):
    """Ventana principal: controla el ciclo de reconocimiento y la salida de texto.

    Señales
    -------
    sig_live : Signal(str)
        Texto parcial (LIVE) emitido por el reconocedor en tiempo real.
    sig_final : Signal(str)
        Texto final (FIN) de cada fragmento reconocido.
    sig_action : Signal(list)
        Lista de acciones parseadas (tokens/pares) provenientes del analizador.
    sig_error : Signal(str)
        Mensajes de error capturados en el pipeline de reconocimiento.

    Notas
    -----
    - La interfaz `Ui_MainWindow` debe proveer `pushButton_2` y `textBrowser`.
    - La transcripción LIVE se mantiene como una única línea que se sobreescribe,
      para evitar que el log crezca con ruido mientras el usuario habla.
    """

    # Señales expuestas para enganchar callbacks Qt-safe desde StreamingRecognizer
    sig_live   = Signal(str)
    sig_final  = Signal(str)
    sig_action = Signal(list)
    sig_error  = Signal(str)

    def __init__(self):
        """Inicializa la UI, conecta señales y deja el reconocedor en estado inactivo."""
        super().__init__()
        # Monta todo el .ui: botones, textBrowser, iconos, etc.
        self.setupUi(self)

        # Conexiones de UI
        self.pushButton_2.clicked.connect(self.toggle_recognition)

        # Conexión de señales a slots: LIVE reescribe, FIN/ERROR hacen append
        self.sig_live.connect(self._update_live)
        self.sig_final.connect(lambda t: self.textBrowser.append(f"[FIN]  {t}\n"))
        self.sig_action.connect(self._show_actions)
        self.sig_error.connect(lambda e: self.textBrowser.append(f"[ERROR] {e}\n"))

        # Estado interno del reconocedor
        self._recognizer = None
        self._running    = False

    def _update_live(self, texto: str):
        """Actualiza la línea LIVE reescribiendo solo la última ocurrencia.

        Parameters
        ----------
        texto : str
            Texto parcial más reciente proveniente del reconocedor.

        Notas
        -----
        - Se filtran las líneas que empiezan con "[LIVE]" para que siempre
          exista una única línea LIVE visible.
        - Se reposiciona el cursor al final para mantener el scroll “anclado”.
        """
        # 1) Filtrar todas las líneas que NO empiecen con "[LIVE]"
        contenido = self.textBrowser.toPlainText()
        lineas = [l for l in contenido.splitlines() if not l.startswith("[LIVE]")]

        # 2) Añadir la nueva línea [LIVE]
        lineas.append(f"[LIVE] {texto}")

        # 3) Reescribir todo el contenido
        self.textBrowser.setPlainText("\n".join(lineas))

        # 4) Mover el cursor al final para que siempre se vea la última línea
        cursor = self.textBrowser.textCursor()
        cursor.movePosition(QTextCursor.End)
        self.textBrowser.setTextCursor(cursor)

    def _show_actions(self, pairs: list):
        """Muestra en el log las acciones parseadas (si las hay).

        Parameters
        ----------
        pairs : list
            Estructura heterogénea con tokens/pares provenientes del parser.
        """
        if not pairs:
            self.textBrowser.append("Sin órdenes\n")
        else:
            self.textBrowser.append(f"[Acciones] → {pairs}\n")

    def toggle_recognition(self):
        """Alterna entre iniciar y detener el reconocimiento de voz."""
        if not self._running:
            self._start_recognition()
            self.pushButton_2.setText("Apagar")
        else:
            self._stop_recognition()
            self.pushButton_2.setText("Encender")

    def _start_recognition(self):
        """Crea y arranca el `StreamingRecognizer`; engancha callbacks a señales Qt."""
        self.textBrowser.append("Transcribiendo...\n")
        # Se pasan “emit” de las señales para que el reconocedor comunique eventos
        self._recognizer = StreamingRecognizer(
            on_live   = self.sig_live.emit,
            on_final  = self.sig_final.emit,
            on_action = self.sig_action.emit,
            on_error  = lambda e: self.sig_error.emit(str(e))
        )
        self._recognizer.start()
        self._running = True

    def _stop_recognition(self):
        """Detiene el reconocedor si existe y notifica en la interfaz."""
        if self._recognizer:
            self._recognizer.stop()
            self._recognizer = None
        self._running = False
        self.textBrowser.append("Reconocimiento detenido.\n")

    def closeEvent(self, event: QCloseEvent):
        """Garantiza un cierre limpio: detiene el reconocedor antes de salir."""
        self._stop_recognition()
        event.accept()


if __name__ == "__main__":
    # Punto de entrada de la aplicación
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec())
