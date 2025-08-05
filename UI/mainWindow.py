from PyQt6.QtWidgets import QMainWindow, QLabel, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QListWidget, QLineEdit, \
    QMessageBox, QDateTimeEdit
from database.dbManager import DBManager
from models.task import Task
from notifications.notifier import showNotification
from PyQt6.QtCore import QTimer
from datetime import datetime, timedelta
from plyer import notification

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ToDoAppPro")
        self.setGeometry(100,100,800,600)

        self.db = DBManager()
        self.tasks = []

        # Show notification of tasks
        showNotification("Tasks Alert", "Your tasks are almost out of schedule")

        # Initial message
        label = QLabel("Welcome to ToDoAppPro!", self)
        label.move(200,200)

        # Create a central widget
        centralWidget = QWidget()
        self.setCentralWidget(centralWidget)

        # Main layout
        mainLayout = QVBoxLayout()
        self.setLayout(mainLayout)

        # Task list
        self.taskList = QListWidget()
        mainLayout.addWidget(self.taskList)

        # Timer to check notification
        self.notificationTimer = QTimer()
        self.notificationTimer.timeout.connect(self.checkTasknotifications)
        self.notificationTimer.start(60000)  # Check every minute

        # Field for start date
        self.startDateInput = QDateTimeEdit()
        self.startDateInput.setDisplayFormat("yyyy-MM-dd HH:mm")
        self.startDateInput.setDateTime(datetime.now())
        # Adiciona ao layout principal
        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.startDateInput)

        # Field for due date
        self.dueDateInput = QDateTimeEdit()
        self.dueDateInput.setDisplayFormat("yyyy-MM-dd HH:mm")
        self.dueDateInput.setDateTime(datetime.now())
        mainLayout.addWidget(self.dueDateInput)

        # Input field
        self.taskInput = QLineEdit()
        self.taskInput.setPlaceholderText("Write a new task")
        mainLayout.addWidget(self.taskInput)

        # Add task button
        buttonLayout = QHBoxLayout()
        self.addButton = QPushButton("Add", self)
        self.removeButton = QPushButton("Remove", self)
        buttonLayout.addWidget(self.addButton)
        buttonLayout.addWidget(self.removeButton)
        mainLayout.addLayout(buttonLayout)

        # Connect buttons to methods
        self.addButton.clicked.connect(self.addTask)
        self.removeButton.clicked.connect(self.removeTask)

        # Apply layouts
        centralWidget.setLayout(mainLayout)

        # Carregar tarefas do banco após criar self.taskList
        self.loadTasks()

    def addTask(self):
        taskText = self.taskInput.text().strip()

        if taskText:
            task = Task(taskText)
            self.tasks.append(task)
            self.taskList.addItem(str(taskText))
            self.db.addTask(task)
            self.taskInput.clear()

        else:
            QMessageBox.warning(self, "Input Error", "Task could not be empty")

    def removeTask(self):
        selectedItems = self.taskList.selectedItems()

        if not selectedItems:

            QMessageBox.warning(self, "Selection Error", "Select a task to be removed")

            return

        for item in selectedItems:
            index = self.taskList.row(item)
            task = self.tasks[index]
            self.db.removeTask(task.title)
            self.taskList.takeItem(index)
            del self.tasks[index]

    def loadTasks(self):
        rows = self.db.loadTasks()
        for row in rows:
            title, description, completed, startDate, dueDate = row
            task = Task(title, description, bool(completed), startDate, dueDate)
            self.tasks.append(task)
            self.taskList.addItem(str(task))

    def checkTasknotifications(self):
        now = datetime.now()
        for task in self.tasks:
            if task.startDate:
                start = datetime.strptime(task.startDate, "%Y-%m-%d %H:%M")

                if now >= start - timedelta(minutes=10) and now < start:
                    notification.notify()
                    title = "Task beginning soon"
                    message = (f"Task is starting soon")
                    timeout = 10

                if task.dueDate:
                    due = datetime.strptime(task.dueDate, "%Y-%m-%d %H:%M")
                    if now >= due - timedelta(minutes=30) and now < due:
                        notification.notify()
                        title = "Task ending soon"
                        message = (f"Task is ending soon")
                        timeout = 10
