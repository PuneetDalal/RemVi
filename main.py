from PyQt6.QtWidgets import QApplication, QWidget,QPushButton,QMainWindow
from PyQt6.QtCore import QSize,Qt
import sys
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("RemVi")
        button = QPushButton("Press")
        button.setCheckable(True)
        button.clicked.connect(self.the_button_was_clicked)
        button.clicked.connect(self.the_button_was_toggled)
        self.setMinimumSize(QSize(400,300))
        self.setCentralWidget(button)

    def the_button_was_clicked(self):
        print("Clicked")

    def the_button_was_toggled(self,checked):
        self.button_is_checked = checked
        print("Checked?",checked)
app=QApplication(sys.argv)
window= MainWindow()

window.show()
app.exec()