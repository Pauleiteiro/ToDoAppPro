from PyQt6.QtWidgets import QMainWindow, QLabel

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ToDoAppPro")
        self.setGeometry(100,100,600,400)


        label = QLabel("Welcome to ToDoAppPro!", self)

        label.move(200,200)
