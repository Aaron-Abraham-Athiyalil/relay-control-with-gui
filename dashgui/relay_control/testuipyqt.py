import joblib
import numpy as np
import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QGridLayout, QMessageBox
)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QFont, QPalette, QBrush, QLinearGradient, QColor, QIcon

# Load your model
model = joblib.load('multi_output_model.joblib')

class RelayControlApp(QWidget):
    def __init__(self):
        super().__init__()
        self.is_running = False  # Track the running state
        self.relay_states = [0] * 8  # Track the state of each relay
        self.initUI()

    def initUI(self):
        # Window properties
        self.setWindowTitle("Relay Model Tester")
        self.setGeometry(100, 100, 800, 480)
        
        # Fonts
        title_font = QFont('Arial', 22, QFont.Bold)
        label_font = QFont('Arial', 12)
        button_font = QFont('Arial', 10, QFont.Bold)

        # Set a smoother off-white gradient background
        gradient = QLinearGradient(0, 0, 0, self.height())
        gradient.setColorAt(0, QColor(240, 240, 240))  # Light gray
        gradient.setColorAt(1, QColor(255, 255, 255))  # White
        palette = QPalette()
        palette.setBrush(QPalette.Window, QBrush(gradient))
        self.setPalette(palette)

        # Title Label
        title_label = QLabel("Relay Model Tester")
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("color: black;")  # Black text color
        
        # Layouts
        main_layout = QVBoxLayout()
        grid_layout = QGridLayout()

        # Input Fields
        self.input_fields = {}
        input_labels = ["IR", "IY", "IB", "VR", "VY", "VB"]
        for i, label_text in enumerate(input_labels):
            label = QLabel(f"{label_text}:")
            label.setFont(label_font)
            label.setStyleSheet("color: black;")  # Black text color
            input_field = QLineEdit()
            input_field.setFixedHeight(30)
            input_field.setStyleSheet("background-color: white; color: black; border: 1px solid #BDBDBD;")
            grid_layout.addWidget(label, i, 0)
            grid_layout.addWidget(input_field, i, 1)
            self.input_fields[label_text] = input_field

        # Error Label for invalid inputs
        self.error_label = QLabel("")
        self.error_label.setFont(QFont('Arial', 10))
        self.error_label.setStyleSheet("color: red;")
        
        # Start Button
        self.start_button = QPushButton("Start")
        self.start_button.setFixedHeight(40)
        self.start_button.setFont(button_font)
        self.start_button.setStyleSheet("background-color: #00BFFF; color: black;")  # Sky blue
        self.start_button.setIcon(QIcon("https://upload.wikimedia.org/wikipedia/commons/thumb/c/c5/Play_icon.svg/1024px-Play_icon.svg.png"))  # Play icon
        self.start_button.setIconSize(QSize(24, 24))  # Set icon size
        self.start_button.clicked.connect(self.toggle_start)

        # Predict Button
        self.predict_button = QPushButton("Predict")
        self.predict_button.setFixedHeight(40)
        self.predict_button.setFont(button_font)
        self.predict_button.setStyleSheet("background-color: #00BFFF; color: black;")  # Sky blue
        self.predict_button.setIcon(QIcon("https://upload.wikimedia.org/wikipedia/commons/thumb/5/57/Calculator_icon.svg/1024px-Calculator_icon.svg.png"))  # Calculator icon
        self.predict_button.setIconSize(QSize(24, 24))  # Set icon size
        self.predict_button.clicked.connect(self.predict)

        # Relay Output Labels and Buttons
        self.relay_buttons = []
        self.output_labels = []
        for i in range(8):
            output_label = QLabel(f"L{i+1}: Off")
            output_label.setFont(label_font)
            output_label.setAlignment(Qt.AlignCenter)
            output_label.setStyleSheet("color: black;")  # Black text color

            # Button to turn on/off the relay
            relay_button = QPushButton("Turn On")
            relay_button.setFixedHeight(40)
            relay_button.setFont(button_font)
            relay_button.setStyleSheet("background-color: #C0C0C0; color: black; border: none;")  # Default button color
            relay_button.setIcon(QIcon("https://upload.wikimedia.org/wikipedia/commons/thumb/1/1e/Power_icon.svg/1024px-Power_icon.svg.png"))  # Power icon
            relay_button.setIconSize(QSize(24, 24))  # Set icon size
            relay_button.clicked.connect(lambda checked, index=i: self.toggle_relay(index))
            
            # Adding the output label and button in the grid layout
            grid_layout.addWidget(output_label, i, 2)
            grid_layout.addWidget(relay_button, i, 3)
            self.output_labels.append(output_label)
            self.relay_buttons.append(relay_button)
        
        # Add widgets to the main layout
        main_layout.addWidget(title_label)
        main_layout.addWidget(self.error_label)
        main_layout.addLayout(grid_layout)

        # Add the start and predict buttons side by side
        button_layout = QVBoxLayout()
        button_layout.addWidget(self.start_button, alignment=Qt.AlignCenter)
        button_layout.addWidget(self.predict_button, alignment=Qt.AlignCenter)
        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)

        # Set stretch factors for responsiveness
        grid_layout.setColumnStretch(0, 1)
        grid_layout.setColumnStretch(1, 2)
        grid_layout.setColumnStretch(2, 1)
        grid_layout.setColumnStretch(3, 1)

    def toggle_start(self):
        if not self.is_running:
            self.is_running = True
            self.start_button.setText("Stop")
            self.start_button.setStyleSheet("background-color: #FF1744; color: black;")  # Red
            self.start_button.setIcon(QIcon("https://upload.wikimedia.org/wikipedia/commons/thumb/c/cb/Stop_icon.svg/1024px-Stop_icon.svg.png"))  # Stop icon
            self.start_button.setIconSize(QSize(24, 24))  # Set icon size
            # Enable the relay buttons after starting
            for button in self.relay_buttons:
                button.setEnabled(True)
        else:
            self.is_running = False
            self.start_button.setText("Start")
            self.start_button.setStyleSheet("background-color: #00BFFF; color: black;")  # Sky blue
            self.start_button.setIcon(QIcon("https://upload.wikimedia.org/wikipedia/commons/thumb/c/c5/Play_icon.svg/1024px-Play_icon.svg.png"))  # Play icon
            self.start_button.setIconSize(QSize(24, 24))  # Set icon size
            for label in self.output_labels:
                label.setText("Off")
                label.setStyleSheet("color: black;")  # Reset to black when stopped
            for button in self.relay_buttons:
                button.setEnabled(False)  # Disable buttons when stopped

    def predict(self):
        try:
            # Retrieve and validate input values
            inputs = [float(self.input_fields[field].text()) for field in self.input_fields]
            input_data = np.array([inputs])
            
            # Model prediction
            predictions = model.predict(input_data)[0]  # Adjust to access the first element
            for i, prediction in enumerate(predictions):
                self.output_labels[i].setText(f"L{i+1}: {'On' if prediction == 1 else 'Off'}")
                self.output_labels[i].setStyleSheet("color: green;" if prediction == 1 else "color: black;")  # Change color to green if on

        except ValueError:
            # If there's an input error, you can still toggle the relays
            for i in range(8):
                self.output_labels[i].setText(f"L{i+1}: {'On' if self.relay_states[i] == 1 else 'Off'}")
                self.output_labels[i].setStyleSheet("color: black;")  # Keep output text black

    def toggle_relay(self, index):
        # Toggle the relay state when the button is clicked
        if self.relay_states[index] == 0:  # If the relay is currently off
            self.relay_states[index] = 1  # Update the relay state to on
            self.output_labels[index].setText(f"L{index + 1}: On")
            self.output_labels[index].setStyleSheet("color: green;")  # Change color to green
            self.relay_buttons[index].setText("Turn Off")  # Change button text to "Turn Off"
            self.relay_buttons[index].setStyleSheet("background-color: #32CD32; color: black;")  # Change button color to green
        else:  # If the relay is currently on
            self.relay_states[index] = 0  # Update the relay state to off
            self.output_labels[index].setText(f"L{index + 1}: Off")
            self.output_labels[index].setStyleSheet("color: black;")  # Change color back to black
            self.relay_buttons[index].setText("Turn On")  # Change button text back to "Turn On"
            self.relay_buttons[index].setStyleSheet("background-color: #C0C0C0; color: black;")  # Change button color back to default

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = RelayControlApp()
    ex.show()
    sys.exit(app.exec_())
