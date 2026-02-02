#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
JARVIS GUI - Modern Control Panel
Features:
- Real-time status updates
- Voice visualization
- Command history
- System monitoring
- Indian language support
- Dark/Light theme
- Animations and effects
"""

import sys
import os
import time
from datetime import datetime
from collections import deque

# Suppress all Qt warnings before importing PyQt5
os.environ['QT_LOGGING_RULES'] = '*.debug=false;qt.qpa.*=false'
os.environ['QT_ENABLE_HIGHDPI_SCALING'] = '0'
os.environ['QT_AUTO_SCREEN_SCALE_FACTOR'] = '0'
os.environ['QT_SCALE_FACTOR'] = '1'
os.environ['QT_DEVICE_PIXEL_RATIO'] = '0'

# Suppress Python warnings
import warnings
warnings.filterwarnings("ignore")

try:
    from PyQt5.QtWidgets import (
        QApplication, QMainWindow, QPushButton, QVBoxLayout, QHBoxLayout,
        QWidget, QLabel, QTextEdit, QFrame, QScrollArea, QGridLayout,
        QProgressBar, QTabWidget, QListWidget, QListWidgetItem, QGroupBox,
        QSystemTrayIcon, QMenu, QAction, QSplitter
    )
    from PyQt5.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve, pyqtSignal, QThread
    from PyQt5.QtGui import QFont, QColor, QPalette, QIcon, QPixmap, QPainter, QLinearGradient
    GUI_AVAILABLE = True
except ImportError as e:
    print(f"⚠️  GUI not available: {e}")
    print("Running in terminal mode only.")
    GUI_AVAILABLE = False


class StatusMonitor(QThread):
    """Background thread for monitoring system status"""
    status_update = pyqtSignal(dict)
    
    def __init__(self):
        super().__init__()
        self.running = True
        
    def run(self):
        """Monitor system resources"""
        while self.running:
            try:
                import psutil
                cpu = psutil.cpu_percent(interval=1)
                memory = psutil.virtual_memory().percent
                
                # Check GPU if available
                gpu_usage = 0
                try:
                    import torch
                    if torch.cuda.is_available():
                        gpu_usage = torch.cuda.memory_allocated() / torch.cuda.max_memory_allocated() * 100
                except:
                    pass
                
                self.status_update.emit({
                    'cpu': cpu,
                    'memory': memory,
                    'gpu': gpu_usage,
                    'timestamp': datetime.now().strftime("%H:%M:%S")
                })
            except:
                pass
            
            time.sleep(2)
    
    def stop(self):
        """Stop monitoring"""
        self.running = False


class JarvisGUI(QMainWindow):
    """Modern JARVIS Control Panel with advanced features"""
    
    def __init__(self, pause_event):
        super().__init__()
        self.pause_event = pause_event
        self.is_paused = False
        self.dark_mode = True
        self.command_history = deque(maxlen=50)
        self.status_monitor = None
        
        # Initialize UI
        self.init_ui()
        self.setup_animations()
        self.start_monitoring()
        
    def init_ui(self):
        """Initialize the user interface"""
        self.setWindowTitle("🤖 JARVIS - AI Assistant Control Panel")
        self.setGeometry(100, 100, 1200, 800)
        self.setMinimumSize(900, 600)
        
        # Apply theme
        self.apply_theme()
        
        # Central widget with tabs
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QVBoxLayout()
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        # Header
        header = self.create_header()
        main_layout.addWidget(header)
        
        # Tab widget
        self.tabs = QTabWidget()
        self.tabs.setStyleSheet("""
            QTabWidget::pane {
                border: none;
                background: transparent;
            }
            QTabBar::tab {
                background: #2d2d2d;
                color: #00ff00;
                padding: 12px 24px;
                margin-right: 2px;
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
                font-size: 13px;
                font-weight: bold;
            }
            QTabBar::tab:selected {
                background: #1e1e1e;
                color: #00ff00;
            }
            QTabBar::tab:hover {
                background: #3d3d3d;
            }
        """)
        
        # Create tabs
        self.tabs.addTab(self.create_dashboard_tab(), "📊 Dashboard")
        self.tabs.addTab(self.create_commands_tab(), "💬 Commands")
        self.tabs.addTab(self.create_system_tab(), "⚙️ System")
        self.tabs.addTab(self.create_settings_tab(), "🔧 Settings")
        
        main_layout.addWidget(self.tabs)
        
        # Footer
        footer = self.create_footer()
        main_layout.addWidget(footer)
        
        central_widget.setLayout(main_layout)
        
        # System tray
        self.setup_system_tray()
        
    def create_header(self):
        """Create header with logo and controls"""
        header = QFrame()
        header.setFixedHeight(80)
        header.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #1a1a1a, stop:1 #2d2d2d);
                border-bottom: 2px solid #00ff00;
            }
        """)
        
        layout = QHBoxLayout()
        layout.setContentsMargins(20, 10, 20, 10)
        
        # Logo and title
        title_layout = QVBoxLayout()
        title = QLabel("🤖 JARVIS")
        title.setFont(QFont("Arial", 24, QFont.Bold))
        title.setStyleSheet("color: #00ff00; background: transparent;")
        
        subtitle = QLabel("Autonomous AI Assistant")
        subtitle.setFont(QFont("Arial", 10))
        subtitle.setStyleSheet("color: #888888; background: transparent;")
        
        title_layout.addWidget(title)
        title_layout.addWidget(subtitle)
        layout.addLayout(title_layout)
        
        layout.addStretch()
        
        # Status indicator
        self.status_indicator = QLabel("● ACTIVE")
        self.status_indicator.setFont(QFont("Arial", 12, QFont.Bold))
        self.status_indicator.setStyleSheet("color: #00ff00; background: transparent;")
        layout.addWidget(self.status_indicator)
        
        # Control buttons
        self.pause_btn = QPushButton("⏸️ Pause")
        self.pause_btn.setFixedSize(100, 40)
        self.pause_btn.clicked.connect(self.toggle_pause)
        self.pause_btn.setStyleSheet(self.get_button_style())
        layout.addWidget(self.pause_btn)
        
        theme_btn = QPushButton("🌓 Theme")
        theme_btn.setFixedSize(100, 40)
        theme_btn.clicked.connect(self.toggle_theme)
        theme_btn.setStyleSheet(self.get_button_style())
        layout.addWidget(theme_btn)
        
        header.setLayout(layout)
        return header
    
    def create_dashboard_tab(self):
        """Create main dashboard tab"""
        widget = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # Top row - Quick stats
        stats_layout = QHBoxLayout()
        
        # Active status card
        self.active_card = self.create_stat_card("Status", "ACTIVE", "#00ff00")
        stats_layout.addWidget(self.active_card)
        
        # Commands processed
        self.commands_card = self.create_stat_card("Commands", "0", "#00aaff")
        stats_layout.addWidget(self.commands_card)
        
        # Uptime
        self.uptime_card = self.create_stat_card("Uptime", "00:00:00", "#ffaa00")
        stats_layout.addWidget(self.uptime_card)
        
        # Mode
        self.mode_card = self.create_stat_card("Mode", "Voice", "#ff00ff")
        stats_layout.addWidget(self.mode_card)
        
        layout.addLayout(stats_layout)
        
        # Middle row - Voice visualization and recent commands
        middle_layout = QHBoxLayout()
        
        # Voice visualization
        voice_group = QGroupBox("🎤 Voice Activity")
        voice_group.setStyleSheet(self.get_group_style())
        voice_layout = QVBoxLayout()
        
        self.voice_level = QProgressBar()
        self.voice_level.setRange(0, 100)
        self.voice_level.setValue(0)
        self.voice_level.setTextVisible(False)
        self.voice_level.setStyleSheet("""
            QProgressBar {
                border: 2px solid #00ff00;
                border-radius: 5px;
                background: #1a1a1a;
                height: 30px;
            }
            QProgressBar::chunk {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #00ff00, stop:1 #00aa00);
                border-radius: 3px;
            }
        """)
        voice_layout.addWidget(self.voice_level)
        
        self.voice_status = QLabel("🔇 Listening...")
        self.voice_status.setAlignment(Qt.AlignCenter)
        self.voice_status.setStyleSheet("color: #888888; font-size: 12px;")
        voice_layout.addWidget(self.voice_status)
        
        voice_group.setLayout(voice_layout)
        middle_layout.addWidget(voice_group, 1)
        
        # Recent commands
        recent_group = QGroupBox("📝 Recent Commands")
        recent_group.setStyleSheet(self.get_group_style())
        recent_layout = QVBoxLayout()
        
        self.recent_list = QListWidget()
        self.recent_list.setStyleSheet("""
            QListWidget {
                background: #1a1a1a;
                border: 1px solid #333333;
                border-radius: 5px;
                color: #00ff00;
                font-family: 'Courier New';
                font-size: 11px;
            }
            QListWidget::item {
                padding: 5px;
                border-bottom: 1px solid #2a2a2a;
            }
            QListWidget::item:selected {
                background: #2d2d2d;
            }
        """)
        recent_layout.addWidget(self.recent_list)
        
        recent_group.setLayout(recent_layout)
        middle_layout.addWidget(recent_group, 2)
        
        layout.addLayout(middle_layout)
        
        # Bottom row - System resources
        resources_group = QGroupBox("💻 System Resources")
        resources_group.setStyleSheet(self.get_group_style())
        resources_layout = QGridLayout()
        
        # CPU
        cpu_label = QLabel("CPU:")
        cpu_label.setStyleSheet("color: #00ff00; font-weight: bold;")
        self.cpu_bar = QProgressBar()
        self.cpu_bar.setRange(0, 100)
        self.cpu_bar.setStyleSheet(self.get_progress_style("#00aaff"))
        resources_layout.addWidget(cpu_label, 0, 0)
        resources_layout.addWidget(self.cpu_bar, 0, 1)
        
        # Memory
        mem_label = QLabel("Memory:")
        mem_label.setStyleSheet("color: #00ff00; font-weight: bold;")
        self.mem_bar = QProgressBar()
        self.mem_bar.setRange(0, 100)
        self.mem_bar.setStyleSheet(self.get_progress_style("#ffaa00"))
        resources_layout.addWidget(mem_label, 1, 0)
        resources_layout.addWidget(self.mem_bar, 1, 1)
        
        # GPU
        gpu_label = QLabel("GPU:")
        gpu_label.setStyleSheet("color: #00ff00; font-weight: bold;")
        self.gpu_bar = QProgressBar()
        self.gpu_bar.setRange(0, 100)
        self.gpu_bar.setStyleSheet(self.get_progress_style("#ff00ff"))
        resources_layout.addWidget(gpu_label, 2, 0)
        resources_layout.addWidget(self.gpu_bar, 2, 1)
        
        resources_group.setLayout(resources_layout)
        layout.addWidget(resources_group)
        
        widget.setLayout(layout)
        return widget
    
    def create_commands_tab(self):
        """Create commands history tab"""
        widget = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Header
        header = QLabel("💬 Command History & Logs")
        header.setFont(QFont("Arial", 16, QFont.Bold))
        header.setStyleSheet("color: #00ff00;")
        layout.addWidget(header)
        
        # Command log
        self.command_log = QTextEdit()
        self.command_log.setReadOnly(True)
        self.command_log.setStyleSheet("""
            QTextEdit {
                background: #1a1a1a;
                border: 2px solid #00ff00;
                border-radius: 8px;
                color: #00ff00;
                font-family: 'Courier New';
                font-size: 12px;
                padding: 10px;
            }
        """)
        layout.addWidget(self.command_log)
        
        # Clear button
        clear_btn = QPushButton("🗑️ Clear History")
        clear_btn.setFixedHeight(40)
        clear_btn.clicked.connect(self.clear_history)
        clear_btn.setStyleSheet(self.get_button_style())
        layout.addWidget(clear_btn)
        
        widget.setLayout(layout)
        return widget
    
    def create_system_tab(self):
        """Create system information tab"""
        widget = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # Header
        header = QLabel("⚙️ System Information")
        header.setFont(QFont("Arial", 16, QFont.Bold))
        header.setStyleSheet("color: #00ff00;")
        layout.addWidget(header)
        
        # System info
        self.system_info = QTextEdit()
        self.system_info.setReadOnly(True)
        self.system_info.setStyleSheet("""
            QTextEdit {
                background: #1a1a1a;
                border: 2px solid #00ff00;
                border-radius: 8px;
                color: #00ff00;
                font-family: 'Courier New';
                font-size: 11px;
                padding: 15px;
            }
        """)
        
        # Populate system info
        self.update_system_info()
        layout.addWidget(self.system_info)
        
        # Refresh button
        refresh_btn = QPushButton("🔄 Refresh Info")
        refresh_btn.setFixedHeight(40)
        refresh_btn.clicked.connect(self.update_system_info)
        refresh_btn.setStyleSheet(self.get_button_style())
        layout.addWidget(refresh_btn)
        
        widget.setLayout(layout)
        return widget
    
    def create_settings_tab(self):
        """Create settings tab"""
        widget = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # Header
        header = QLabel("🔧 Settings & Controls")
        header.setFont(QFont("Arial", 16, QFont.Bold))
        header.setStyleSheet("color: #00ff00;")
        layout.addWidget(header)
        
        # Control buttons
        controls_group = QGroupBox("🎮 Controls")
        controls_group.setStyleSheet(self.get_group_style())
        controls_layout = QVBoxLayout()
        
        # Pause/Resume
        pause_resume_btn = QPushButton("⏸️ Pause/Resume Listening")
        pause_resume_btn.setFixedHeight(50)
        pause_resume_btn.clicked.connect(self.toggle_pause)
        pause_resume_btn.setStyleSheet(self.get_button_style())
        controls_layout.addWidget(pause_resume_btn)
        
        # Theme toggle
        theme_btn = QPushButton("🌓 Toggle Dark/Light Theme")
        theme_btn.setFixedHeight(50)
        theme_btn.clicked.connect(self.toggle_theme)
        theme_btn.setStyleSheet(self.get_button_style())
        controls_layout.addWidget(theme_btn)
        
        # Minimize to tray
        tray_btn = QPushButton("📥 Minimize to System Tray")
        tray_btn.setFixedHeight(50)
        tray_btn.clicked.connect(self.hide)
        tray_btn.setStyleSheet(self.get_button_style())
        controls_layout.addWidget(tray_btn)
        
        controls_group.setLayout(controls_layout)
        layout.addWidget(controls_group)
        
        layout.addStretch()
        
        # Exit button
        exit_btn = QPushButton("❌ Exit JARVIS")
        exit_btn.setFixedHeight(60)
        exit_btn.clicked.connect(self.close_application)
        exit_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #ff0000, stop:1 #cc0000);
                color: white;
                border: none;
                border-radius: 10px;
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #ff3333, stop:1 #ff0000);
            }
            QPushButton:pressed {
                background: #aa0000;
            }
        """)
        layout.addWidget(exit_btn)
        
        widget.setLayout(layout)
        return widget
    
    def create_footer(self):
        """Create footer with status bar"""
        footer = QFrame()
        footer.setFixedHeight(40)
        footer.setStyleSheet("""
            QFrame {
                background: #1a1a1a;
                border-top: 1px solid #333333;
            }
        """)
        
        layout = QHBoxLayout()
        layout.setContentsMargins(20, 5, 20, 5)
        
        # Version
        version = QLabel("JARVIS v2.0 | NPU Accelerated")
        version.setStyleSheet("color: #888888; font-size: 11px;")
        layout.addWidget(version)
        
        layout.addStretch()
        
        # Time
        self.time_label = QLabel()
        self.time_label.setStyleSheet("color: #00ff00; font-size: 11px; font-weight: bold;")
        self.update_time()
        layout.addWidget(self.time_label)
        
        footer.setLayout(layout)
        return footer
    
    def create_stat_card(self, title, value, color):
        """Create a stat card widget"""
        card = QFrame()
        card.setStyleSheet(f"""
            QFrame {{
                background: #2d2d2d;
                border: 2px solid {color};
                border-radius: 10px;
                padding: 10px;
            }}
        """)
        
        layout = QVBoxLayout()
        
        title_label = QLabel(title)
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet(f"color: {color}; font-size: 12px; font-weight: bold;")
        
        value_label = QLabel(value)
        value_label.setAlignment(Qt.AlignCenter)
        value_label.setFont(QFont("Arial", 20, QFont.Bold))
        value_label.setStyleSheet(f"color: {color};")
        value_label.setObjectName("value")
        
        layout.addWidget(title_label)
        layout.addWidget(value_label)
        
        card.setLayout(layout)
        return card
    
    def get_button_style(self):
        """Get button stylesheet"""
        return """
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #2d2d2d, stop:1 #3d3d3d);
                color: #00ff00;
                border: 2px solid #00ff00;
                border-radius: 8px;
                padding: 10px;
                font-size: 13px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #00ff00, stop:1 #00cc00);
                color: #1e1e1e;
            }
            QPushButton:pressed {
                background: #00aa00;
            }
        """
    
    def get_group_style(self):
        """Get group box stylesheet"""
        return """
            QGroupBox {
                background: #2d2d2d;
                border: 2px solid #00ff00;
                border-radius: 10px;
                margin-top: 10px;
                padding-top: 10px;
                font-size: 13px;
                font-weight: bold;
                color: #00ff00;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
            }
        """
    
    def get_progress_style(self, color):
        """Get progress bar stylesheet"""
        return f"""
            QProgressBar {{
                border: 2px solid {color};
                border-radius: 5px;
                background: #1a1a1a;
                text-align: center;
                color: white;
                font-weight: bold;
            }}
            QProgressBar::chunk {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 {color}, stop:1 {self.adjust_color(color, -30)});
                border-radius: 3px;
            }}
        """
    
    def adjust_color(self, color, amount):
        """Adjust color brightness"""
        # Simple color adjustment
        return color  # Simplified for now
    
    def apply_theme(self):
        """Apply dark/light theme"""
        if self.dark_mode:
            self.setStyleSheet("""
                QMainWindow {
                    background-color: #1e1e1e;
                }
                QWidget {
                    background-color: #1e1e1e;
                    color: #00ff00;
                }
                QLabel {
                    background: transparent;
                }
            """)
        else:
            self.setStyleSheet("""
                QMainWindow {
                    background-color: #f0f0f0;
                }
                QWidget {
                    background-color: #f0f0f0;
                    color: #006600;
                }
                QLabel {
                    background: transparent;
                }
            """)
    
    def setup_animations(self):
        """Setup UI animations"""
        # Pulse animation for status indicator
        self.pulse_timer = QTimer()
        self.pulse_timer.timeout.connect(self.pulse_status)
        self.pulse_timer.start(1000)
        
        # Update time
        self.time_timer = QTimer()
        self.time_timer.timeout.connect(self.update_time)
        self.time_timer.start(1000)
        
        # Voice level animation
        self.voice_timer = QTimer()
        self.voice_timer.timeout.connect(self.update_voice_level)
        self.voice_timer.start(100)
        
        # Uptime counter
        self.start_time = time.time()
        self.uptime_timer = QTimer()
        self.uptime_timer.timeout.connect(self.update_uptime)
        self.uptime_timer.start(1000)
    
    def start_monitoring(self):
        """Start system monitoring"""
        try:
            self.status_monitor = StatusMonitor()
            self.status_monitor.status_update.connect(self.update_system_stats)
            self.status_monitor.start()
        except:
            pass
    
    def setup_system_tray(self):
        """Setup system tray icon"""
        try:
            self.tray_icon = QSystemTrayIcon(self)
            self.tray_icon.setToolTip("JARVIS AI Assistant")
            
            # Create tray menu
            tray_menu = QMenu()
            
            show_action = QAction("Show", self)
            show_action.triggered.connect(self.show)
            tray_menu.addAction(show_action)
            
            pause_action = QAction("Pause/Resume", self)
            pause_action.triggered.connect(self.toggle_pause)
            tray_menu.addAction(pause_action)
            
            tray_menu.addSeparator()
            
            quit_action = QAction("Exit", self)
            quit_action.triggered.connect(self.close_application)
            tray_menu.addAction(quit_action)
            
            self.tray_icon.setContextMenu(tray_menu)
            self.tray_icon.activated.connect(self.tray_icon_activated)
            self.tray_icon.show()
        except:
            pass
    
    def tray_icon_activated(self, reason):
        """Handle tray icon activation"""
        if reason == QSystemTrayIcon.DoubleClick:
            self.show()
    
    def pulse_status(self):
        """Pulse status indicator"""
        if not self.is_paused:
            current = self.status_indicator.styleSheet()
            if "color: #00ff00" in current:
                self.status_indicator.setStyleSheet("color: #00cc00; background: transparent;")
            else:
                self.status_indicator.setStyleSheet("color: #00ff00; background: transparent;")
    
    def update_time(self):
        """Update time display"""
        current_time = datetime.now().strftime("%H:%M:%S")
        self.time_label.setText(f"🕐 {current_time}")
    
    def update_uptime(self):
        """Update uptime display"""
        uptime = int(time.time() - self.start_time)
        hours = uptime // 3600
        minutes = (uptime % 3600) // 60
        seconds = uptime % 60
        
        uptime_str = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        value_label = self.uptime_card.findChild(QLabel, "value")
        if value_label:
            value_label.setText(uptime_str)
    
    def update_voice_level(self):
        """Update voice level visualization"""
        import random
        if not self.is_paused:
            # Simulate voice activity
            level = random.randint(20, 80)
            self.voice_level.setValue(level)
            
            if level > 60:
                self.voice_status.setText("🎤 Speaking...")
                self.voice_status.setStyleSheet("color: #00ff00; font-size: 12px; font-weight: bold;")
            else:
                self.voice_status.setText("🔇 Listening...")
                self.voice_status.setStyleSheet("color: #888888; font-size: 12px;")
        else:
            self.voice_level.setValue(0)
            self.voice_status.setText("⏸️ Paused")
            self.voice_status.setStyleSheet("color: #ffaa00; font-size: 12px; font-weight: bold;")
    
    def update_system_stats(self, stats):
        """Update system resource displays"""
        self.cpu_bar.setValue(int(stats['cpu']))
        self.cpu_bar.setFormat(f"{stats['cpu']:.1f}%")
        
        self.mem_bar.setValue(int(stats['memory']))
        self.mem_bar.setFormat(f"{stats['memory']:.1f}%")
        
        self.gpu_bar.setValue(int(stats['gpu']))
        self.gpu_bar.setFormat(f"{stats['gpu']:.1f}%")
    
    def update_system_info(self):
        """Update system information display"""
        info = []
        info.append("=" * 60)
        info.append("🖥️  SYSTEM INFORMATION")
        info.append("=" * 60)
        info.append("")
        
        # Python info
        info.append(f"Python Version: {sys.version.split()[0]}")
        info.append("")
        
        # Platform info
        import platform
        info.append(f"Platform: {platform.system()} {platform.release()}")
        info.append(f"Machine: {platform.machine()}")
        info.append(f"Processor: {platform.processor()}")
        info.append("")
        
        # PyTorch info
        try:
            import torch
            info.append(f"PyTorch Version: {torch.__version__}")
            info.append(f"CUDA Available: {torch.cuda.is_available()}")
            if torch.cuda.is_available():
                info.append(f"CUDA Version: {torch.version.cuda}")
                info.append(f"GPU: {torch.cuda.get_device_name(0)}")
                info.append(f"GPU Memory: {torch.cuda.get_device_properties(0).total_memory / 1e9:.2f} GB")
        except:
            info.append("PyTorch: Not installed")
        info.append("")
        
        # NPU info
        try:
            from core.npu_accelerator import npu_accelerator
            info.append("🚀 NPU Acceleration: Enabled")
            info.append(f"   Device: {npu_accelerator.device}")
        except:
            info.append("NPU Acceleration: Not available")
        info.append("")
        
        # Environment
        info.append("🔑 Environment:")
        groq_key = os.environ.get("GROQ_API_KEY")
        info.append(f"   GROQ_API_KEY: {'✅ Set' if groq_key else '❌ Not set'}")
        info.append("")
        
        info.append("=" * 60)
        
        self.system_info.setText("\n".join(info))
    
    def add_command(self, command, response):
        """Add command to history"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        # Add to recent list
        item = QListWidgetItem(f"[{timestamp}] {command}")
        self.recent_list.insertItem(0, item)
        
        # Keep only last 10
        while self.recent_list.count() > 10:
            self.recent_list.takeItem(self.recent_list.count() - 1)
        
        # Add to command log
        log_entry = f"[{timestamp}] USER: {command}\n"
        log_entry += f"[{timestamp}] JARVIS: {response}\n"
        log_entry += "-" * 60 + "\n"
        self.command_log.append(log_entry)
        
        # Update command counter
        value_label = self.commands_card.findChild(QLabel, "value")
        if value_label:
            current = int(value_label.text())
            value_label.setText(str(current + 1))
    
    def clear_history(self):
        """Clear command history"""
        self.command_log.clear()
        self.recent_list.clear()
        
        # Reset counter
        value_label = self.commands_card.findChild(QLabel, "value")
        if value_label:
            value_label.setText("0")
    
    def toggle_pause(self):
        """Toggle pause/resume state"""
        if self.is_paused:
            # Resume
            self.pause_event.clear()
            self.is_paused = False
            self.pause_btn.setText("⏸️ Pause")
            self.status_indicator.setText("● ACTIVE")
            self.status_indicator.setStyleSheet("color: #00ff00; background: transparent;")
            
            # Update status card
            value_label = self.active_card.findChild(QLabel, "value")
            if value_label:
                value_label.setText("ACTIVE")
        else:
            # Pause
            self.pause_event.set()
            self.is_paused = True
            self.pause_btn.setText("▶️ Resume")
            self.status_indicator.setText("● PAUSED")
            self.status_indicator.setStyleSheet("color: #ffaa00; background: transparent;")
            
            # Update status card
            value_label = self.active_card.findChild(QLabel, "value")
            if value_label:
                value_label.setText("PAUSED")
    
    def toggle_theme(self):
        """Toggle dark/light theme"""
        self.dark_mode = not self.dark_mode
        self.apply_theme()
    
    def close_application(self):
        """Close the application"""
        self.status_indicator.setText("● SHUTTING DOWN")
        self.status_indicator.setStyleSheet("color: #ff0000; background: transparent;")
        
        # Stop monitoring
        if self.status_monitor:
            self.status_monitor.stop()
            self.status_monitor.wait()
        
        QTimer.singleShot(500, self.close)
        QTimer.singleShot(1000, lambda: sys.exit(0))
    
    def closeEvent(self, event):
        """Handle window close event"""
        # Minimize to tray instead of closing
        event.ignore()
        self.hide()
        try:
            self.tray_icon.showMessage(
                "JARVIS",
                "JARVIS is still running in the background",
                QSystemTrayIcon.Information,
                2000
            )
        except:
            pass


def run_gui(pause_event):
    """Run the GUI application with error handling"""
    if not GUI_AVAILABLE:
        print("❌ GUI dependencies not available. Install with: pip install PyQt5")
        return False
    
    try:
        # Check if QApplication already exists
        app = QApplication.instance()
        if app is None:
            app = QApplication(sys.argv)
        
        # Set application attributes to suppress DPI warnings
        try:
            app.setAttribute(Qt.AA_DisableHighDpiScaling)
            app.setAttribute(Qt.AA_Use96Dpi)
        except:
            pass  # Ignore if attributes not available
        
        # Create and show window
        window = JarvisGUI(pause_event)
        window.show()
        
        print("✅ GUI started successfully")
        
        # Run event loop
        return app.exec_()
        
    except Exception as e:
        print(f"❌ GUI Error: {e}")
        print("Falling back to terminal mode...")
        import traceback
        traceback.print_exc()
        return False
