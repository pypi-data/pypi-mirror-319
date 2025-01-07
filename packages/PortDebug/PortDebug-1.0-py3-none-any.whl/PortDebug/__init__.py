
from main_en import MainWindow
from PySide6.QtWidgets import QApplication
def start():
    app = QApplication()
    window = MainWindow()
    window.show()
    app.exec()