import sys
import os

# Suppress all Qt warnings before importing PyQt5
os.environ['QT_LOGGING_RULES'] = '*.debug=false;qt.qpa.*=false'
os.environ['QT_ENABLE_HIGHDPI_SCALING'] = '0'
os.environ['QT_AUTO_SCREEN_SCALE_FACTOR'] = '0'
os.environ['QT_SCALE_FACTOR'] = '1'

from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont

class JarvisGUI(QMainWindow):
    def __init__(self, pause_event):
        super().__init__()
        self.pause_event = pause_event
        self.is_paused = False
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("JARVIS Control Panel")
        self.setGeometry(100, 100, 400, 300)
        self.setStyleSheet("""
            QMainWindow {
                background-color: #1e1e1e;
            }
            QLabel {
                color: #00ff00;
                font-size: 18px;
                font-weight: bold;
            }
            QPushButton {
                background-color: #2d2d2d;
                color: #00ff00;
                border: 2px solid #00ff00;
                border-radius: 10px;
                padding: 10px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #00ff00;
                color: #1e1e1e;
            }
            QPushButton:pressed {
                background-color: #00cc00;
            }
        """)

        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Layout
        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(30, 30, 30, 30)

        # Title
        title = QLabel("JARVIS AI Assistant")
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont("Arial", 20, QFont.Bold))
        layout.addWidget(title)

        # Status label
        self.status_label = QLabel("Status: Active 🟢")
        self.status_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.status_label)

        # Pause/Resume button
        self.pause_button = QPushButton("⏸️  Pause Listening")
        self.pause_button.clicked.connect(self.toggle_pause)
        layout.addWidget(self.pause_button)

        # Exit button
        exit_button = QPushButton("❌ Exit JARVIS")
        exit_button.clicked.connect(self.close_application)
        layout.addWidget(exit_button)

        # Info label
        info = QLabel("💡 Voice commands are active\n🎤 Say 'Jarvis' to wake")
        info.setAlignment(Qt.AlignCenter)
        info.setStyleSheet("color: #888888; font-size: 12px;")
        layout.addWidget(info)

        layout.addStretch()
        central_widget.setLayout(layout)

    def toggle_pause(self):
        """Toggle pause/resume state"""
        if self.is_paused:
            # Resume
            self.pause_event.clear()
            self.is_paused = False
            self.pause_button.setText("⏸️  Pause Listening")
            self.status_label.setText("Status: Active 🟢")
            self.status_label.setStyleSheet("color: #00ff00;")
        else:
            # Pause
            self.pause_event.set()
            self.is_paused = True
            self.pause_button.setText("▶️  Resume Listening")
            self.status_label.setText("Status: Paused 🟡")
            self.status_label.setStyleSheet("color: #ffaa00;")

    def close_application(self):
        """Close the application"""
        self.status_label.setText("Status: Shutting Down 🔴")
        self.status_label.setStyleSheet("color: #ff0000;")
        QTimer.singleShot(500, self.close)
        QTimer.singleShot(1000, lambda: sys.exit(0))

def run_gui(pause_event):
    """Run the GUI application with suppressed warnings"""
    # Additional warning suppression
    import warnings
    warnings.filterwarnings("ignore")
    
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    
    # Set application attributes to suppress DPI warnings
    app.setAttribute(Qt.AA_DisableHighDpiScaling)
    app.setAttribute(Qt.AA_Use96Dpi)
    
    window = JarvisGUI(pause_event)
    window.show()
    sys.exit(app.exec_())
