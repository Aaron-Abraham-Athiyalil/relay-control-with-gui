from PySide6.QtWidgets import QMainWindow, QLabel, QProgressBar, QFrame, QVBoxLayout

class Ui_SplashScreen(object):
    def setupUi(self, SplashScreen):
        SplashScreen.resize(400, 300)
        
        # Main layout
        self.centralwidget = QFrame(SplashScreen)
        
        # Drop shadow frame
        self.frame = QFrame(self.centralwidget)
        self.frame.setObjectName("frame")
        
        # Title and description
        self.label_title = QLabel("MyApp", self.frame)
        self.label_description = QLabel("Loading the best app...", self.frame)
        
        # Progress bar
        self.progressBar = QProgressBar(self.frame)
        self.progressBar.setValue(0)
        
        # Arrange widgets in layout (e.g., QVBoxLayout, QHBoxLayout)
