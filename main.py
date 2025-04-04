import sys
import requests
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout,
    QPushButton, QLineEdit, QLabel, QTextEdit
)

from variables import AppName

class AutonomousVtube(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(AppName)
        self.setGeometry(100, 100, 400, 300)


        # Layout
        layout = QVBoxLayout()

        # Widgets
        self.input = QLineEdit(self)
        self.button = QPushButton("API Req", self)
        self.button.clicked.connect(self.fetch_post)

        self.setLayout(layout)

    def fetch_post(self):

        url = f""
        try:
            # response = requests.get(url)
            # response.raise_for_status()
            # data = response.json()

            # display = f"Title: {data['title']}\n\nBody:\n{data['body']}"
            # self.result.setText(display)
            print('Button pressed')
        except requests.RequestException as e:
            print(f"Error: {str(e)}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AutonomousVtube()
    window.show()
    sys.exit(app.exec_())
