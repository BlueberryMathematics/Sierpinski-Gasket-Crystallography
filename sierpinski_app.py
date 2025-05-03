import sys
import os
from PyQt6.QtWidgets import (QApplication, QMainWindow, QPushButton, 
                          QVBoxLayout, QWidget, QStyle)
from PyQt6.QtCore import Qt, QUrl
from PyQt6.QtGui import QIcon
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWebEngineCore import QWebEngineSettings

class SuperStretchButton(QPushButton):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(30, 30)
        self.setToolTip("Super Stretch (Across All Monitors)")
        self.setText("⬒")
        self.setStyleSheet("""
            QPushButton {
                background-color: rgba(255, 255, 255, 0.1);
                border: none;
                color: #666;
                font-size: 16px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 0.2);
                color: #000;
            }
        """)
        self.stretched = False

class SierpinskiWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle('Sierpinski Circlet Visualizer')
        self.setGeometry(100, 100, 1200, 800)

        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Create WebEngine view with settings
        self.web_view = QWebEngineView()
        settings = self.web_view.settings()
        settings.setAttribute(QWebEngineSettings.WebAttribute.LocalContentCanAccessRemoteUrls, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.WebGLEnabled, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.Accelerated2dCanvasEnabled, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.JavascriptEnabled, True)

        # Load the HTML file using absolute path
        html_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'fixed-sierpinski-circlet.html'))
        self.web_view.setUrl(QUrl.fromLocalFile(html_path))
        layout.addWidget(self.web_view)

        # Add super stretch button
        self.super_stretch_btn = SuperStretchButton(self)
        self.super_stretch_btn.clicked.connect(self.toggleSuperStretch)
        self.positionSuperStretchButton()

    def positionSuperStretchButton(self):
        titlebar_height = self.style().pixelMetric(QStyle.PixelMetric.PM_TitleBarHeight)
        button_margin = 5
        self.super_stretch_btn.move(
            self.width() - 100 - self.super_stretch_btn.width() - button_margin,
            titlebar_height // 2 - self.super_stretch_btn.height() // 2 + button_margin
        )

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.positionSuperStretchButton()

    def toggleSuperStretch(self):
        if not self.super_stretch_btn.stretched:
            # Get combined geometry of all screens
            screens = QApplication.screens()
            combined_geometry = screens[0].geometry()
            for screen in screens[1:]:
                combined_geometry = combined_geometry.united(screen.geometry())
            
            # Save current geometry for restoration
            self.normal_geometry = self.geometry()
            
            # Set window to cover all screens
            self.setGeometry(combined_geometry)
            self.super_stretch_btn.setText("⬓")
        else:
            # Restore previous geometry
            self.setGeometry(self.normal_geometry)
            self.super_stretch_btn.setText("⬒")
        
        self.super_stretch_btn.stretched = not self.super_stretch_btn.stretched

def main():
    # Set DPI environment variables before creating QApplication
    os.environ["QT_ENABLE_HIGHDPI_SCALING"] = "1"
    os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
    
    app = QApplication(sys.argv)
    
    # Create and show window
    window = SierpinskiWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
