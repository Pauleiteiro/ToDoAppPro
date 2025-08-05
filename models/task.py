from datetime import datetime

class Task:
    def __init__(self, title, description="", completed = False,startDate = None, dueDate = None):
        self.title = title
        self.description = description
        self.completed = completed
        self.startDate = startDate or datetime.now().strftime("%Y-%m-%d %H:%M")
        self.dueDate = dueDate

    def __str__(self):
        return f"{self.title}{'✓' if self.completed else ''}"
