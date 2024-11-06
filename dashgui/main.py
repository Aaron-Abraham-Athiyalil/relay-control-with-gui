import sys
import os
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QStackedWidget, QLabel, QFrame, QPushButton, QCheckBox, QLineEdit, QGridLayout
)
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt
import joblib  # To load the deep learning model
import numpy as np

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Main Window")
        self.setWindowState(Qt.WindowFullScreen)

        # Set up background
        self.set_background_image()

        # Main layout
        self.main_layout = QHBoxLayout()
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        self.central_widget.setLayout(self.main_layout)

        # Sidebar and main pages setup
        self.sidebar_layout = QVBoxLayout()
        self.sidebar_frame = QFrame()
        self.sidebar_frame.setFixedWidth(180)
        self.sidebar_frame.setStyleSheet("background-color: #f5f5f5; border-radius: 10px;")
        self.sidebar_frame.setLayout(self.sidebar_layout)
        self.stacked_widget = QStackedWidget(self)
        self.main_layout.addWidget(self.sidebar_frame)
        self.main_layout.addWidget(self.stacked_widget)

        # Create pages
        self.create_pages()
        self.setup_sidebar()

    def set_background_image(self):
        # Set a background image
        self.setStyleSheet("background-image: url(resources/bcg/1.png); background-repeat: no-repeat; background-position: center;")

    def create_pages(self):
        # Home Page
        self.page_home = QWidget()
        home_layout = QVBoxLayout(self.page_home)
        home_label = QLabel("Welcome to the Home Page!", self)
        home_label.setAlignment(Qt.AlignCenter)
        home_layout.addWidget(home_label)
        self.stacked_widget.addWidget(self.page_home)

        # Relay Page with prediction and relay toggles
        self.page_relay = QWidget()
        relay_layout = QVBoxLayout(self.page_relay)

        # Load the deep learning model
        model_path = os.path.join("relay_control", "multi_output_model.joblib")
        self.model = joblib.load(model_path)

        # Relay page title
        relay_title = QLabel("Relay Control & Prediction")
        relay_title.setFont(QFont("Segoe UI", 16, QFont.Bold))
        relay_title.setAlignment(Qt.AlignCenter)
        relay_layout.addWidget(relay_title)

        # Input fields for Ir, Iv, Ib, Va, Vb, Vc
        input_grid = QGridLayout()
        self.input_fields = {}
        labels = ['Ir', 'Iv', 'Ib', 'Va', 'Vb', 'Vc']
        for i, label in enumerate(labels):
            input_label = QLabel(f"{label}:")
            input_field = QLineEdit()
            input_field.setPlaceholderText(f"Enter {label}")
            self.input_fields[label] = input_field
            input_grid.addWidget(input_label, i, 0)
            input_grid.addWidget(input_field, i, 1)
        relay_layout.addLayout(input_grid)

        # Buttons for starting and predicting
        button_layout = QHBoxLayout()
        start_button = QPushButton("Start")
        start_button.clicked.connect(self.start_process)
        predict_button = QPushButton("Predict")
        predict_button.clicked.connect(self.run_prediction)
        button_layout.addWidget(start_button)
        button_layout.addWidget(predict_button)
        relay_layout.addLayout(button_layout)

        # Prediction result label
        self.prediction_result = QLabel("Prediction Result: No prediction yet")
        self.prediction_result.setAlignment(Qt.AlignCenter)
        relay_layout.addWidget(self.prediction_result)

        # Relay toggle buttons
        relay_toggle_layout = QGridLayout()
        self.relay_buttons = []
        for i in range(8):
            relay_button = QCheckBox(f"Relay {i+1}")
            relay_button.setStyleSheet("font-size: 14px;")
            relay_button.stateChanged.connect(lambda state, index=i: self.toggle_relay(index, state))
            relay_toggle_layout.addWidget(relay_button, i // 4, i % 4)
            self.relay_buttons.append(relay_button)
        relay_layout.addLayout(relay_toggle_layout)

        # Adding Relay Page to stacked widget
        self.stacked_widget.addWidget(self.page_relay)

    def setup_sidebar(self):
        # Sidebar buttons
        home_button = QPushButton("Home")
        relay_button = QPushButton("Relay")
        exit_button = QPushButton("Exit")

        button_style = """
            QPushButton {
                background-color: #e0e0e0;
                color: black;
                border: none;
                border-radius: 8px;
                padding: 12px;
                font: bold 14px "Segoe UI";
                margin: 5px;
            }
            QPushButton:hover {
                background-color: #d0d0d0;
            }
            QPushButton:pressed {
                background-color: #c0c0c0;
            }
        """
        for button in [home_button, relay_button, exit_button]:
            button.setStyleSheet(button_style)

        home_button.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.page_home))
        relay_button.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.page_relay))
        exit_button.clicked.connect(self.close_application)

        self.sidebar_layout.addWidget(home_button)
        self.sidebar_layout.addWidget(relay_button)
        self.sidebar_layout.addWidget(exit_button)

    def close_application(self):
        self.close()

    def start_process(self):
        # Placeholder for any initialization code
        self.prediction_result.setText("Process started...")

    def run_prediction(self):
        # Collect inputs and make prediction
        try:
            input_data = [float(self.input_fields[key].text().strip()) for key in self.input_fields]
            prediction = self.model.predict([input_data])[0]  # Assuming single prediction output per input set

            # Update relays based on prediction result
            self.prediction_result.setText(f"Prediction Result: {prediction}")
            self.update_relays(prediction)
        except ValueError:
            self.prediction_result.setText("Invalid input. Please enter numerical values for all inputs.")
        except Exception as e:
            self.prediction_result.setText(f"Error during prediction: {e}")

    def toggle_relay(self, index, state):
        # Manual relay toggle
        if state == Qt.Checked:
            print(f"Relay {index + 1} turned ON")
        else:
            print(f"Relay {index + 1} turned OFF")

    def update_relays(self, prediction):
        # Update relays based on prediction result
        if isinstance(prediction, (int, float)):  # If single prediction value
            prediction = [int(prediction)] * len(self.relay_buttons)  # Set all relays to this value
        elif isinstance(prediction, (list, np.ndarray)):
            prediction = list(map(int, prediction))  # Ensure list of integers

        for i, relay_button in enumerate(self.relay_buttons):
            relay_state = bool(prediction[i] if i < len(prediction) else 0)
            relay_button.setChecked(relay_state)
            relay_button.setText(f"Relay {i + 1} {'ON' if relay_state else 'OFF'}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())
