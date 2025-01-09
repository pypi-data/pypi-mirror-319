import sys
import os
from PyQt6.QtCore import Qt, QUrl
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QWidget,
    QStatusBar, QMenu, QTabWidget, QMessageBox
)
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtGui import QIcon, QAction
import argparse
import subprocess

class CRLBrowser(QMainWindow):
    def __init__(self, search_url=None):
        super().__init__()

        # Pencere ayarları
        self.setWindowTitle("CRL Browser")
        self.setGeometry(100, 100, 1200, 800)
        icon_path = self.get_icon_path()

        self.setWindowIcon(QIcon(icon_path))
        # Cache dizinini hazırla
        self.setup_cache()

        # Tab widget oluştur
        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_tab)
        self.setCentralWidget(self.tabs)

        # Yeni sekme aç
        if search_url:
            self.add_new_tab(search_url, "New Tab")
        else:
            self.add_new_tab("file:///~/.local/share/crl-browser/crl-desktop-sources-index/homepage.html", "New Tab")

        # Navigasyon çubuğu
        self.nav_bar = QHBoxLayout()

        # Adres çubuğu
        self.address_bar = QLineEdit()
        self.address_bar.setPlaceholderText("Enter URL here")
        self.address_bar.returnPressed.connect(self.load_url)

        # Düğmeler
        self.back_button = QPushButton("[<]")
        self.back_button.setFixedSize(30, 30)
        self.back_button.clicked.connect(lambda: self.current_browser().back())

        self.forward_button = QPushButton("[>]")
        self.forward_button.setFixedSize(30, 30)
        self.forward_button.clicked.connect(lambda: self.current_browser().forward())

        self.reload_button = QPushButton("[R]")
        self.reload_button.setFixedSize(30, 30)
        self.reload_button.clicked.connect(lambda: self.current_browser().reload())

        self.new_tab_button = QPushButton("[+]")
        self.new_tab_button.setFixedSize(30, 30)
        self.new_tab_button.clicked.connect(self.add_new_tab)

        self.settings_button = QPushButton("☰")  # Hamburger menüsü simgesi
        self.settings_button.setFixedSize(30, 30)
        self.settings_button.clicked.connect(self.show_settings_menu)

        self.nav_bar.addWidget(self.back_button)
        self.nav_bar.addWidget(self.forward_button)
        self.nav_bar.addWidget(self.reload_button)
        self.nav_bar.addWidget(self.new_tab_button)
        self.nav_bar.addWidget(self.address_bar)
        self.nav_bar.addWidget(self.settings_button)

        # Ana widget ve layout
        self.main_widget = QWidget()
        self.main_layout = QVBoxLayout(self.main_widget)
        self.main_layout.addLayout(self.nav_bar)
        self.main_layout.addWidget(self.tabs)
        self.setCentralWidget(self.main_widget)

        # CSS stilleri
        self.apply_styles()
    
    def get_icon_path(self):
     if sys.platform == "win32":
           icon_path = os.path.join(os.getenv('USERPROFILE'), 'AppData', 'Local', 'crl-browser', 'icons', 'icon.png')
     elif sys.platform == "darwin":
           icon_path = os.path.join(os.path.expanduser('~'), 'Library', 'Application Support', 'crl-browser', 'icons', 'icon.png')
     else:
        # Linux için, ~/.local/share/crl-browser altında belirtilen yol
        icon_path = os.path.join(os.path.expanduser('~'), '.local', 'share', 'crl-browser', 'icons', 'icon.png')

     return icon_path

    def setup_cache(self):
        cache_dir = os.path.expanduser("~/.local/share/crl-browser/share/.cache")
        if not os.path.exists(cache_dir):
            os.makedirs(cache_dir)

    def add_new_tab(self, url=None, label="New Tab"):
        browser = QWebEngineView()
        browser.setUrl(QUrl(url) if url else QUrl("file:////home/goychay23/crl-browser/src/crl-desktop-sources-index/homepage.html"))
        i = self.tabs.addTab(browser, label)
        self.tabs.setCurrentIndex(i)
        browser.urlChanged.connect(lambda qurl, browser=browser: self.update_url(qurl, browser))

    def close_tab(self, index):
        if self.tabs.count() > 1:
            self.tabs.removeTab(index)
        else:
            self.close()

    def current_browser(self):
        return self.tabs.currentWidget()

    def load_url(self):
        url = self.address_bar.text()
        if not url.startswith("http://") and not url.startswith("https://"):
            url = "http://" + url
        self.current_browser().setUrl(QUrl(url))

    def update_url(self, qurl, browser):
        if browser == self.current_browser():
            self.address_bar.setText(qurl.toString())

    def run_history_manager(self):
        try:
            subprocess.Popen(["python3", "historymanager.py"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        except FileNotFoundError as e:
            QMessageBox.critical(self, "Error", f"Unable to run History Manager: {str(e)}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An unexpected error occurred: {str(e)}")

    def run_settings(self):
        try:
            subprocess.Popen(["python3", "settings_manager.py"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        except FileNotFoundError as e:
            QMessageBox.critical(self, "Error", f"Unable to run Settings: {str(e)}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An unexpected error occurred: {str(e)}")

    def show_settings_menu(self):
        """Settings menüsünü göster."""
        self.run_settings()

    def apply_styles(self):
        self.setStyleSheet("""
        QWidget {
            background-color: #0e0e0e;
            color: #00ffff;
        }
        QLineEdit {
            background-color: #1e1e1e;
            color: #00ffff;
            border: 1px solid #00ffff;
            border-radius: 5px;
            padding: 5px;
            font-size: 14px;
        }
        QPushButton {
            background-color: #1e1e1e;
            color: #00ffff;
            border: 1px solid #00ffff;
            border-radius: 5px;
            padding: 5px;
            font-size: 14px;
        }
        QPushButton:hover {
            background-color: #00ffff;
            color: #1e1e1e;
        }
        QTabWidget::pane {
            border: 1px solid #00ffff;
        }
        QTabBar::tab {
            background-color: #1e1e1e;
            color: #00ffff;
            padding: 5px;
            border: 1px solid #00ffff;
            border-bottom: none;
        }
        QTabBar::tab:selected {
            background-color: #00ffff;
            color: #1e1e1e;
        }
        QStatusBar {
            background-color: #0e0e0e;
            color: #00ffff;
        }
        QMenu {
            background-color: #1e1e1e;
            border: 1px solid #00ffff;
            color: #00ffff;
        }
        QMenu::item {
            padding: 10px;
            color: #00ffff;
        }
        QMenu::item:selected {
            background-color: #00ffff;
            color: #1e1e1e;
        }
        QMainWindow {
            background-color: #0e0e0e;
        }
        """)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--search-url", type=str, help="URL to open on start")
    args = parser.parse_args()

    app = QApplication(sys.argv)
    browser = CRLBrowser(search_url=args.search_url)
    browser.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
