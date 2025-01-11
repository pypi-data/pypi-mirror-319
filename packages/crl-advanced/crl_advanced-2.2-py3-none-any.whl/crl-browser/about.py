import sys
from PyQt6.QtWidgets import QApplication, QDialog, QVBoxLayout, QLabel, QPushButton, QHBoxLayout
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QDesktopServices
from PyQt6.QtCore import QUrl

class AboutApp(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("About")
        self.setGeometry(100, 100, 400, 400)
        self.setStyleSheet("""
            background-color: #151515; 
            font-family: Arial, sans-serif;
            font-size: 14px;
            color: white;
        """)

        # Ana düzen
        layout = QVBoxLayout(self)

        # Uygulama hakkında bilgi
        about_label = QLabel("CRL Browser python qt6 based browser\n\n"
                             "Version 2.0\n"
                             "Developed by Azcosf Founder", self)
        layout.addWidget(about_label, alignment=Qt.AlignmentFlag.AlignTop)

        # Lisans Bilgisi
        license_label = QLabel("CRL browser version v2.0 based on Python is copyrighted by Azencompiler open source foundation. "
                               "It is distributed under azcosf license policies. "
                               "For more details, visit: "
                               "<a href='https://azencompileropensourcefoundation.com/license.html'>azcosf license</a>", self)
        license_label.setTextFormat(Qt.TextFormat.RichText)
        license_label.setOpenExternalLinks(True)
        layout.addWidget(license_label)

        # Bağlantılar bölümü
        links_layout = QHBoxLayout()

        # Bağlantı butonları
        github_button = QPushButton("GitHub", self)
        github_button.clicked.connect(self.open_github)
        github_button.setStyleSheet("background-color: #00d9ff; color: black; padding: 8px; border-radius: 5px;")

        pypi_button = QPushButton("PyPI", self)
        pypi_button.clicked.connect(self.open_pypi)
        pypi_button.setStyleSheet("background-color: #00d9ff; color: black; padding: 8px; border-radius: 5px;")

        site_button = QPushButton("Website", self)
        site_button.clicked.connect(self.open_website)
        site_button.setStyleSheet("background-color: #00d9ff; color: black; padding: 8px; border-radius: 5px;")

        links_layout.addWidget(github_button)
        links_layout.addWidget(pypi_button)
        links_layout.addWidget(site_button)

        layout.addLayout(links_layout)

        # Kapama butonu
        close_button = QPushButton("Close", self)
        close_button.clicked.connect(self.accept)
        close_button.setStyleSheet("background-color: #00d9ff; color: black; padding: 8px; border-radius: 5px;")
        layout.addWidget(close_button, alignment=Qt.AlignmentFlag.AlignBottom)

    def open_github(self):
        """
        GitHub sayfasını açar.
        """
        QDesktopServices.openUrl(QUrl("https://github.com/goychay23/crl-browser"))

    def open_pypi(self):
        """
        PyPI sayfasını açar.
        """
        QDesktopServices.openUrl(QUrl("https://pypi.org/project/crl-advanced"))

    def open_website(self):
        """
        Kişisel web sitesini açar.
        """
        QDesktopServices.openUrl(QUrl("https://azencompileropensourcefoundation.com"))

