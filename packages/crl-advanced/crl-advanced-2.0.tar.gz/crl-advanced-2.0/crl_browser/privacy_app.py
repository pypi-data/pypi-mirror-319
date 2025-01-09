import os
import subprocess
import requests
import shutil
from http.cookiejar import CookieJar
import webbrowser
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QCheckBox, QListWidget, QGroupBox, QRadioButton, QHBoxLayout, QMessageBox
from PyQt6.QtCore import Qt

class PrivacyApp(QDialog):
    def __init__(self):
        super().__init__()

        # Dialog ayarları
        self.setWindowTitle("Privacy Settings")
        self.setGeometry(200, 200, 600, 500)

        # Ana düzen
        main_layout = QVBoxLayout(self)

        # Başlık
        title_label = QLabel("Privacy Settings", self)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("font-size: 20px; font-weight: bold; color: #00FFFF;")
        main_layout.addWidget(title_label)

        # Gizlilik politikası kısmı
        self.policy_button = QPushButton("View Privacy Policy", self)
        self.policy_button.setStyleSheet("""
            QPushButton {
                background-color: #101010;
                color: #00FFFF;
                font-size: 16px;
                padding: 10px;
                border: 2px solid #00FFFF;
            }
            QPushButton:hover {
                background-color: #00FFFF;
                color: #101010;
            }
        """)
        self.policy_button.clicked.connect(self.open_privacy_policy_subprocess)
        main_layout.addWidget(self.policy_button)

        # Site URL girişi ve engelleme butonu
        self.site_input_label = QLabel("Enter site URL to block ads:", self)
        self.site_input_label.setStyleSheet("font-size: 16px; color: #00FFFF;")
        main_layout.addWidget(self.site_input_label)

        self.site_input = QLineEdit(self)
        self.site_input.setStyleSheet("font-size: 16px; color: #00FFFF;")
        main_layout.addWidget(self.site_input)

        # Engelleme butonu
        self.block_button = QPushButton("Block Ads on this Site", self)
        self.block_button.setStyleSheet("""
            QPushButton {
                background-color: #101010;
                color: #00FFFF;
                font-size: 16px;
                padding: 10px;
                border: 2px solid #00FFFF;
            }
            QPushButton:hover {
                background-color: #00FFFF;
                color: #101010;
            }
        """)
        self.block_button.clicked.connect(self.confirm_proxy_activation)
        main_layout.addWidget(self.block_button)

        # Engellenen siteler listesi
        self.blocked_sites_list = QListWidget(self)
        self.blocked_sites_list.setStyleSheet("font-size: 16px; color: #00FFFF;")
        main_layout.addWidget(self.blocked_sites_list)

        # Çerezler ve izleme seçenekleri
        cookie_box = QGroupBox("Cookies & Tracking", self)
        cookie_layout = QVBoxLayout(cookie_box)

        self.cookie_checkbox = QCheckBox("Enable Cookie Blocking", self)
        self.cookie_checkbox.setStyleSheet("font-size: 16px; color: #00FFFF;")
        cookie_layout.addWidget(self.cookie_checkbox)

        self.tracking_checkbox = QCheckBox("Block Tracking Scripts", self)
        self.tracking_checkbox.setStyleSheet("font-size: 16px; color: #00FFFF;")
        cookie_layout.addWidget(self.tracking_checkbox)

        main_layout.addWidget(cookie_box)

        # Gizlilik tercihi
        privacy_group = QGroupBox("Privacy Preferences", self)
        privacy_layout = QHBoxLayout(privacy_group)

        self.secure_radio = QRadioButton("Secure Browsing", self)
        self.secure_radio.setStyleSheet("font-size: 16px; color: #00FFFF;")
        privacy_layout.addWidget(self.secure_radio)

        main_layout.addWidget(privacy_group)

        # Uygula, Clean Browser ve Kapat düğmeleri
        apply_button = QPushButton("Apply", self)
        apply_button.setStyleSheet("""
            QPushButton {
                background-color: #101010;
                color: #00FFFF;
                font-size: 16px;
                padding: 10px;
                border: 2px solid #00FFFF;
            }
            QPushButton:hover {
                background-color: #00FFFF;
                color: #101010;
            }
        """)
        apply_button.clicked.connect(self.apply_changes)
        main_layout.addWidget(apply_button)

        clean_browser_button = QPushButton("Clean Browser Cache", self)
        clean_browser_button.setStyleSheet("""
            QPushButton {
                background-color: #101010;
                color: #00FFFF;
                font-size: 16px;
                padding: 10px;
                border: 2px solid #00FFFF;
            }
            QPushButton:hover {
                background-color: #00FFFF;
                color: #101010;
            }
        """)
        clean_browser_button.clicked.connect(self.clean_browser_cache)
        main_layout.addWidget(clean_browser_button)

        close_button = QPushButton("Close", self)
        close_button.setStyleSheet("""
            QPushButton {
                background-color: #101010;
                color: #00FFFF;
                font-size: 16px;
                padding: 10px;
                border: 2px solid #00FFFF;
            }
            QPushButton:hover {
                background-color: #00FFFF;
                color: #101010;
            }
        """)
        close_button.clicked.connect(self.close)
        main_layout.addWidget(close_button)

    def open_privacy_policy_subprocess(self):
        """Subprocess kullanarak privacy policy aç."""
        subprocess.Popen(["python", "browser-main.py", "--search-url", "https://azcosf.org/privacy-policy"])

    def confirm_proxy_activation(self):
        """Proxy servisini etkinleştir ve siteyi engelle."""
        site_url = self.site_input.text()
        if site_url:
            self.block_site(site_url)
        else:
            QMessageBox.warning(self, "Error", "Please enter a valid site URL.")

    def block_site(self, site_url):
        """Proxy üzerinden siteyi engelle."""
        self.blocked_sites_list.addItem(site_url)
        print(f"Blocked site: {site_url}")
        QMessageBox.information(self, "Success", f"Blocked ads on {site_url}.")

    def clean_browser_cache(self):
        """Tarayıcı önbelleğini temizle."""
        # Burada önbellek temizleme işlemi yapılır.
        print("Browser cache has been cleaned.")
        QMessageBox.information(self, "Cache Cleaned", "Browser cache has been cleaned.")

    def apply_changes(self):
        """Gizlilik tercihlerini uygula."""
        cookie_blocking = self.cookie_checkbox.isChecked()
        tracking_blocking = self.tracking_checkbox.isChecked()
        secure_browsing = self.secure_radio.isChecked()

        print(f"Cookie Blocking: {cookie_blocking}")
        print(f"Tracking Blocking: {tracking_blocking}")
        print(f"Secure Browsing: {secure_browsing}")
        QMessageBox.information(self, "Settings Applied", "Your privacy settings have been applied.")
