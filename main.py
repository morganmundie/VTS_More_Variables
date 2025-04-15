import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout,
    QPushButton, QLineEdit, QLabel, QApplication, QWidget, QLabel, QLineEdit, QComboBox, QSpinBox, QPushButton,
    QHBoxLayout, QVBoxLayout, QSpacerItem, QSizePolicy, QTextEdit, QScrollArea
)
from PyQt5.QtGui import QIcon

from custom_paramter import ParamGroupWidget

from variables import AppName
from vtube_api import VTubeStudioAPI

from param_manager import ParamManager



class AutonomousVtube(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(AppName)
        self.setGeometry(100, 100, 400, 500)

        self.api = VTubeStudioAPI(
            on_message_callback=self.display_message,
            on_error_callback=self.display_error
        )

        self.param_manager = ParamManager(VTubeStudioAPI)

        layout = QVBoxLayout()

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)

        self.param_container = QWidget()
        self.param_layout = QVBoxLayout()
        self.param_container.setLayout(self.param_layout)
        self.scroll_area.setWidget(self.param_container)

        for param in self.param_manager.get_all_params():
            group = ParamGroupWidget(param.name, param.min_val, param.max_val, param.wave_type)
            self.param_layout.addWidget(group)

        self.btn_start = QPushButton("Start + Auto Auth")
        self.btn_start.clicked.connect(self.api.auto_authenticate)

        self.btn_send_input = QPushButton("Send Input")
        self.btn_send_input.clicked.connect(lambda: self.api.start_continuous_input())

        self.test = QPushButton("Save")
        self.test.clicked.connect(lambda: group.create_param(self.api))

        self.output = QTextEdit()
        self.output.setReadOnly(True)

        #todo add button and logic to add a new (empty) param
        layout.addWidget(self.scroll_area)
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
