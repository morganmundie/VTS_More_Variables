from PyQt5.QtWidgets import (
    QWidget, QLabel, QLineEdit, QComboBox, QSpinBox, QPushButton,
    QHBoxLayout, QVBoxLayout, QSpacerItem, QSizePolicy, QGroupBox
)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSignal
from vtube_api import VTubeStudioAPI


class ParamGroupWidget(QGroupBox):
    remove_requested = pyqtSignal(QWidget)  # Signal to notify parent for deletion

    def __init__(self, parent=None):
        super().__init__("Parameter", parent)
        self.init_ui()
        self.api = VTubeStudioAPI()

    def init_ui(self):
        main_layout = QVBoxLayout()

        # Row 1: Param Name
        row1 = QHBoxLayout()
        row1.addWidget(QLabel("Param Name:"))
        self.name_input = QLineEdit()
        row1.addWidget(self.name_input)
        main_layout.addLayout(row1)

        # Row 2: Type, Min, Max
        row2 = QHBoxLayout()
        row2.addWidget(QLabel("Type:"))
        self.type_dropdown = QComboBox()
        self.type_dropdown.addItems(["Wave", "Step", "Pulse"])
        row2.addWidget(self.type_dropdown)

        row2.addWidget(QLabel("Min"))
        self.min_input = QSpinBox()
        self.min_input.setRange(-9999, 9999)
        row2.addWidget(self.min_input)

        row2.addWidget(QLabel("Max"))
        self.max_input = QSpinBox()
        self.max_input.setRange(-9999, 9999)
        row2.addWidget(self.max_input)
        main_layout.addLayout(row2)

        # Row 3: Speed, Multiplier, Randomness, Delete
        row3 = QHBoxLayout()
        row3.addWidget(QLabel("Speed:"))
        self.speed_dropdown = QComboBox()
        self.speed_dropdown.addItems(["Constant", "Variable"])
        row3.addWidget(self.speed_dropdown)

        row3.addWidget(QLabel("Multiplier"))
        self.multiplier_input = QSpinBox()
        self.multiplier_input.setRange(0, 1000)
        row3.addWidget(self.multiplier_input)

        row3.addWidget(QLabel("Randomness"))
        self.randomness_input = QSpinBox()
        self.randomness_input.setRange(0, 1000)
        row3.addWidget(self.randomness_input)

        row3.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))

        self.delete_button = QPushButton()
        # Try using system theme icon, fallback to emoji
        icon = QIcon.fromTheme("user-trash")
        if icon.isNull():
            self.delete_button.setText("🗑")
        else:
            self.delete_button.setIcon(icon)
        self.delete_button.setFixedSize(32, 32)
        self.delete_button.clicked.connect(self.request_delete)
        row3.addWidget(self.delete_button)

        main_layout.addLayout(row3)

        self.setLayout(main_layout)

    def request_delete(self):
        self.remove_requested.emit(self)

    def get_values(self):
        """Returns a dictionary of all input values."""
        return {
            "name": self.name_input.text(),
            "type": self.type_dropdown.currentText(),
            "min": self.min_input.value(),
            "max": self.max_input.value(),
            "speed": self.speed_dropdown.currentText(),
            "multiplier": self.multiplier_input.value(),
            "randomness": self.randomness_input.value()
        }

    def create_param(self):
        print("Create")
        # todo create and save wave data too, below call is to create vtube studio param
        self.api.create_param(self.name_input,self.min_input, self.max_input)
