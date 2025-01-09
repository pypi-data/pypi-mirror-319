import sys
import os
import subprocess
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QApplication, QDialog, QVBoxLayout, QHBoxLayout, QWidget, QLineEdit,
    QLabel, QStatusBar, QPushButton, QMenu, QTextEdit, QListWidget, QMessageBox
)
from PyQt6.QtGui import QFont

class HistoryManager:
    def __init__(self, cache_dir=None):
        self.cache_dir = cache_dir or os.path.expanduser("~/local/share/crl-browser/.cache/upload")
        self.history_file = os.path.join(self.cache_dir, "history.txt")
        self.setup_cache()

    def setup_cache(self):
        try:
            os.makedirs(self.cache_dir, exist_ok=True)
            if not os.path.exists(self.history_file):
                with open(self.history_file, "w", encoding="utf-8") as file:
                    file.write("")
            print(f"Cache directory and history file are ready: {self.history_file}")
        except Exception as e:
            print(f"Error setting up cache directory: {e}")

    def add_url_to_history(self, url):
        try:
            with open(self.history_file, "a", encoding="utf-8") as file:
                file.write(url + "\n")
            print(f"URL added to history: {url}")
        except Exception as e:
            print(f"Error writing URL to history: {e}")

    def get_history(self):
        try:
            with open(self.history_file, "r", encoding="utf-8") as file:
                history = file.readlines()
            return [url.strip() for url in history]
        except Exception as e:
            print(f"Error reading history: {e}")
            return []

    def clear_history(self):
        try:
            with open(self.history_file, "w", encoding="utf-8") as file:
                file.write("")
            print("History cleared.")
        except Exception as e:
            print(f"Error clearing history: {e}")

    def delete_cache(self):
        try:
            if os.path.exists(self.cache_dir):
                for root, dirs, files in os.walk(self.cache_dir, topdown=False):
                    for name in files:
                        os.remove(os.path.join(root, name))
                    for name in dirs:
                        os.rmdir(os.path.join(root, name))
                print("Cache directory cleared.")
            else:
                print("Cache directory does not exist.")
        except Exception as e:
            print(f"Error clearing cache directory: {e}")

    def delete_history_file(self):
        try:
            if os.path.exists(self.history_file):
                os.remove(self.history_file)
                print("History file deleted.")
            else:
                print("History file does not exist.")
        except Exception as e:
            print(f"Error deleting history file: {e}")


class HistoryApp(QDialog):
    def __init__(self):
        super().__init__()
        self.history_manager = HistoryManager()
        self.setWindowTitle("History Manager")
        self.setGeometry(100, 100, 800, 600)

        # Layout for the main window (no need for central widget in QDialog)
        self.layout = QVBoxLayout(self)

        # URL input and action buttons layout
        self.nav_bar = QHBoxLayout()
        self.url_input = QLineEdit(self)
        self.url_input.setPlaceholderText("Enter URL here")
        self.url_input.returnPressed.connect(self.add_to_history)

        self.add_button = QPushButton("Add", self)
        self.add_button.clicked.connect(self.add_to_history)

        self.clear_button = QPushButton("Clear", self)
        self.clear_button.clicked.connect(self.clear_history)

        self.delete_file_button = QPushButton("Delete History File", self)
        self.delete_file_button.clicked.connect(self.delete_history_file)

        self.delete_cache_button = QPushButton("Delete Cache", self)
        self.delete_cache_button.clicked.connect(self.delete_cache)

        self.nav_bar.addWidget(self.url_input)
        self.nav_bar.addWidget(self.add_button)
        self.nav_bar.addWidget(self.clear_button)
        self.nav_bar.addWidget(self.delete_file_button)
        self.nav_bar.addWidget(self.delete_cache_button)

        self.layout.addLayout(self.nav_bar)

        # History list widget
        self.history_list = QListWidget(self)
        self.history_list.itemClicked.connect(self.open_url_in_browser)
        self.update_history_list()
        self.layout.addWidget(self.history_list)

        # Status bar
        self.status_bar = QStatusBar(self)
        self.layout.addWidget(self.status_bar)

        # Apply cyberpunk style
        self.apply_cyberpunk_style()

    def add_to_history(self):
        url = self.url_input.text()
        if url:
            self.history_manager.add_url_to_history(url)
            self.update_history_list()
            self.status_bar.showMessage(f"URL added: {url}", 2000)
            self.url_input.clear()

    def clear_history(self):
        self.history_manager.clear_history()
        self.update_history_list()
        self.status_bar.showMessage("History cleared.", 2000)

    def delete_history_file(self):
        self.history_manager.delete_history_file()
        self.update_history_list()
        self.status_bar.showMessage("History file deleted.", 2000)

    def delete_cache(self):
        self.history_manager.delete_cache()
        self.update_history_list()
        self.status_bar.showMessage("Cache directory cleared.", 2000)

    def update_history_list(self):
        self.history_list.clear()
        history = self.history_manager.get_history()
        self.history_list.addItems(history)

    def open_url_in_browser(self, item):
        url = item.text()
        if url:
            try:
                subprocess.Popen([sys.executable, "browser-main.py", "--search-url", url])
                self.status_bar.showMessage(f"Opening URL: {url}", 2000)
            except Exception as e:
                self.status_bar.showMessage(f"Failed to open URL: {e}", 2000)

    def apply_cyberpunk_style(self):
        font = QFont("Consolas", 12)
        self.setStyleSheet("""
            QDialog {
                background-color: #1a1a1a;
            }

            QLineEdit {
                background-color: #1e1e1e;
                border: 2px solid #00ffff;
                color: #ffffff;
                padding: 4px;
                font-size: 14px;
            }

            QPushButton {
                background-color: #000000;
                border: 2px solid #00ffff;
                color: #00ffff;
                font-size: 14px;
                padding: 6px;
                font-weight: bold;
            }

            QPushButton:hover {
                background-color: #005f5f;
                color: #ffffff;
            }

            QListWidget {
                background-color: #1e1e1e;
                border: 2px solid #00ffff;
                color: #00ffff;
                font-size: 12px;
            }

            QStatusBar {
                background-color: #000000;
                color: #00ffff;
            }
        """)
        self.url_input.setFont(font)
        self.add_button.setFont(font)
        self.clear_button.setFont(font)
        self.delete_file_button.setFont(font)
        self.delete_cache_button.setFont(font)
        self.history_list.setFont(font)
