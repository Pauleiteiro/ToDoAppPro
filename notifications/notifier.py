from plyer import notification

def showNotification(title, message):
    notification.notify(title=title, message=message, timeout=10)