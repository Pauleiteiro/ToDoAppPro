import sqlite3

class DBManager:
    def __init__(self, dbName = "tasks.db"):

        self.connection = sqlite3.connect(dbName)

        self.createTable()

    def createTable(self):
        cursor = self.connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT,
                completed INTEGER,
                startDate TEXT,
                dueDate TEXT
            )
        """)
        self.connection.commit()

    def addTask(self, task):
        cursor = self.connection.cursor()
        cursor.execute("""INSERT INTO tasks (title, description, completed, startDate, dueDate)
        VALUES (?, ?, ?, ?, ?)""", (task.title, task.description, bool(task.completed), task.startDate, task.dueDate))
        self.connection.commit()


    def removeTask(self, title):
        cursor = self.connection.cursor()
        cursor.execute("DELETE FROM tasks WHERE title = ?", (title,))
        self.connection.commit()


    def loadTasks(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT title,description,completed,startDate,dueDate FROM tasks")
        rows = cursor.fetchall()
        return rows
