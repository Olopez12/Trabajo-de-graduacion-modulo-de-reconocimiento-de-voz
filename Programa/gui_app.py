import sys
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtCore    import Qt, Signal
from PySide6.QtGui     import QCloseEvent, QTextCursor

from grafico_ui import Ui_MainWindow
from speech_parser import StreamingRecognizer

class MainWindow(QMainWindow, Ui_MainWindow):
    sig_live   = Signal(str)
    sig_final  = Signal(str)
    sig_action = Signal(list)
    sig_error  = Signal(str)

    def __init__(self):
        super().__init__()
        # Monta todo el .ui: botones, textBrowser, iconos…
        self.setupUi(self)

        # Conexiones
        self.pushButton_2.clicked.connect(self.toggle_recognition)

        # En lugar de append, reescribimos la línea [LIVE]
        self.sig_live.connect(self._update_live)
        self.sig_final.connect(lambda t: self.textBrowser.append(f"[FIN]  {t}\n"))
        self.sig_action.connect(self._show_actions)
        self.sig_error.connect(lambda e: self.textBrowser.append(f"[ERROR] {e}\n"))

        self._recognizer = None
        self._running    = False

    def _update_live(self, texto: str):
        # 1) Filtramos todas las líneas que NO empiecen con "[LIVE]"
        contenido = self.textBrowser.toPlainText()
        lineas = [l for l in contenido.splitlines() if not l.startswith("[LIVE]")]

        # 2) Añadimos la nueva línea [LIVE]
        lineas.append(f"[LIVE] {texto}")

        # 3) Reescribimos todo el contenido
        self.textBrowser.setPlainText("\n".join(lineas))

        # 4) Movemos el cursor al final para que siempre se vea la última línea
        cursor = self.textBrowser.textCursor()
        cursor.movePosition(QTextCursor.End)
        self.textBrowser.setTextCursor(cursor)

    def _show_actions(self, pairs: list):
        if not pairs:
            self.textBrowser.append("Sin órdenes\n")
        else:
            self.textBrowser.append(f"[Acciones] → {pairs}\n")

    def toggle_recognition(self):
        if not self._running:
            self._start_recognition()
            self.pushButton_2.setText("Apagar")
        else:
            self._stop_recognition()
            self.pushButton_2.setText("Encender")

    def _start_recognition(self):
        self.textBrowser.append("Transcribiendo...\n")
        self._recognizer = StreamingRecognizer(
            on_live   = self.sig_live.emit,
            on_final  = self.sig_final.emit,
            on_action = self.sig_action.emit,
            on_error  = lambda e: self.sig_error.emit(str(e))
        )
        self._recognizer.start()
        self._running = True

    def _stop_recognition(self):
        if self._recognizer:
            self._recognizer.stop()
            self._recognizer = None
        self._running = False
        self.textBrowser.append("Reconocimiento detenido.\n")

    def closeEvent(self, event: QCloseEvent):
        self._stop_recognition()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec())
