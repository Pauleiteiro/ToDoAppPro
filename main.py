import sys
from PyQt6.QtWidgets import QApplication
from UI.mainWindow import MainWindow
from database.dbManager import DBManager
from models.task import Task

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()