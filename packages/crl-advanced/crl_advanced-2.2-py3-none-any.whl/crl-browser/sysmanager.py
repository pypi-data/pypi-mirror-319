import sys
import psutil
from PyQt6.QtWidgets import (
    QApplication, QDialog, QVBoxLayout, QLabel, 
    QProgressBar, QSlider, QPushButton, QMessageBox
)
from PyQt6.QtCore import QTimer, Qt

class SystemApp(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("System Manager")
        self.setGeometry(100, 100, 600, 400)
        self.setStyleSheet("""
            background-color: #151515;  /* Sade koyu arkaplan */
            font-family: Arial, sans-serif;
            font-size: 14px;
            color: white;  /* Yazılar beyaz */
        """)

        # Ana düzen
        self.layout = QVBoxLayout(self)

        # CPU ve RAM bilgileri
        self.cpu_label = QLabel("CPU Usage: 0%", self)
        self.cpu_progress = QProgressBar(self)
        self.cpu_progress.setRange(0, 100)
        self.cpu_progress.setStyleSheet("QProgressBar::chunk {background-color: #00d9ff;}")  # Neon mavi çubuk

        self.ram_label = QLabel("RAM Usage: 0%", self)
        self.ram_progress = QProgressBar(self)
        self.ram_progress.setRange(0, 100)
        self.ram_progress.setStyleSheet("QProgressBar::chunk {background-color: #00d9ff;}")  # Neon mavi çubuk

        # Ayarları uygula butonu
        self.cpu_slider = QSlider(Qt.Orientation.Horizontal, self)
        self.cpu_slider.setRange(0, 100)
        self.cpu_slider.setValue(50)

        self.ram_slider = QSlider(Qt.Orientation.Horizontal, self)
        self.ram_slider.setRange(0, 100)
        self.ram_slider.setValue(50)

        apply_button = QPushButton("Apply Settings", self)
        apply_button.clicked.connect(self.apply_settings)
        apply_button.setStyleSheet("background-color: #00d9ff; color: black; padding: 8px; border-radius: 5px;")

        # Arayüz elemanlarını düzenle
        self.layout.addWidget(self.cpu_label)
        self.layout.addWidget(self.cpu_progress)
        self.layout.addWidget(self.ram_label)
        self.layout.addWidget(self.ram_progress)

        self.layout.addWidget(QLabel("Set CPU Limit (%):", self))
        self.layout.addWidget(self.cpu_slider)
        self.layout.addWidget(QLabel("Set RAM Limit (%):", self))
        self.layout.addWidget(self.ram_slider)
        self.layout.addWidget(apply_button)

        # Zamanlayıcı
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_system_stats)
        self.timer.start(1000)  # 1 saniyede bir güncelle

    def update_system_stats(self):
        """
        CPU ve RAM kullanımını günceller.
        """
        cpu_usage = int(psutil.cpu_percent(interval=0.1))  # CPU kullanımını tam sayıya çevir
        ram_usage = int(psutil.virtual_memory().percent)  # RAM kullanımını tam sayıya çevir

        self.cpu_progress.setValue(cpu_usage)
        self.ram_progress.setValue(ram_usage)

        self.cpu_label.setText(f"CPU Usage: {cpu_usage:.1f}%")
        self.ram_label.setText(f"RAM Usage: {ram_usage:.1f}%")

    def apply_settings(self):
        """
        Kullanıcı tarafından ayarlanan limitleri uygular.
        """
        cpu_limit = self.cpu_slider.value()
        ram_limit = self.ram_slider.value()
        QMessageBox.information(
            self,
            "Settings Applied",
            f"CPU Limit: {cpu_limit}%\nRAM Limit: {ram_limit}%",
            QMessageBox.StandardButton.Ok
        )

# PyQt uygulamasını başlat
