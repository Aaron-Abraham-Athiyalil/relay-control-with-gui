from PySide6.QtWidgets import QWidget, QStackedWidget, QLabel, QPushButton, QVBoxLayout

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.resize(800, 600)
        
        # Main layout setup
        self.centralwidget = QWidget(MainWindow)
        MainWindow.setCentralWidget(self.centralwidget)

        # Stack for pages
        self.stackedWidget = QStackedWidget(self.centralwidget)
        
        # Page 1 (Home)
        self.page_home = QWidget()
        self.stackedWidget.addWidget(self.page_home)
        
        # Page 2 (Settings)
        self.page_settings = QWidget()
        self.stackedWidget.addWidget(self.page_settings)
        
        # Title label
        self.label_title = QLabel("Home Page", self.centralwidget)
        
        # Buttons to navigate
        self.btn_home = QPushButton("Home", self.centralwidget)
        self.btn_settings = QPushButton("Settings", self.centralwidget)
        
        # Layout arrangement (vertical layout for simplicity)
        layout = QVBoxLayout(self.centralwidget)
        layout.addWidget(self.label_title)
        layout.addWidget(self.btn_home)
        layout.addWidget(self.btn_settings)
        layout.addWidget(self.stackedWidget)

        # Set the default page
        self.stackedWidget.setCurrentWidget(self.page_home)
