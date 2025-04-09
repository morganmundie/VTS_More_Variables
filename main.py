import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout,
    QPushButton, QLineEdit, QLabel, QApplication, QWidget, QLabel, QLineEdit, QComboBox, QSpinBox, QPushButton,
    QHBoxLayout, QVBoxLayout, QSpacerItem, QSizePolicy, QTextEdit
)
from PyQt5.QtGui import QIcon

from custom_paramter import ParamGroupWidget

from variables import AppName
from vtube_api import VTubeStudioAPI



class AutonomousVtube(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(AppName)
        self.setGeometry(100, 100, 400, 500)

        self.api = VTubeStudioAPI(
            on_message_callback=self.display_message,
            on_error_callback=self.display_error
        )

        layout = QVBoxLayout()

        group = ParamGroupWidget()
        # group.remove_requested.connect(self.remove_param_group)
        # self.param_groups.append(group)
        layout.addWidget(group)

        self.btn_start = QPushButton("Start + Auto Auth")
        self.btn_start.clicked.connect(self.api.auto_authenticate)

        self.btn_send_input = QPushButton("Send Input")
        self.btn_send_input.clicked.connect(lambda: self.api.start_continuous_input())

        self.test = QPushButton("Save")
        self.test.clicked.connect(lambda: group.create_param(self.api))

        self.output = QTextEdit()
        self.output.setReadOnly(True)

        layout.addWidget(self.btn_send_input)
        layout.addWidget(self.test)
        layout.addWidget(self.output)
        layout.addWidget(self.btn_start)

        self.setLayout(layout)

    def display_message(self, message):
        self.output.append(f"[Response]\n{message}\n")

    def display_error(self, error):
        self.output.append(f"[Error]\n{error}\n")



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AutonomousVtube()
    window.show()
    sys.exit(app.exec_())
