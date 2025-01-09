import subprocess
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from PyQt6.QtGui import QFont


class  TorProxyPanel(QWidget):
    def __init__(self):
        super().__init__()

        # Layout ve widget ayarları
        self.layout = QVBoxLayout(self)

        # Font ayarları
        custom_font = QFont("Courier New", 11, QFont.Weight.Bold)

        # Proxy address input field
        self.proxy_label = QLabel("Proxy Address (e.g., 127.0.0.1:9050):", self)
        self.proxy_label.setFont(custom_font)
        self.layout.addWidget(self.proxy_label)

        self.proxy_input = QLineEdit(self)
        self.proxy_input.setPlaceholderText("127.0.0.1:9050")
        self.layout.addWidget(self.proxy_input)

        # Start Tor button
        self.start_button = QPushButton("START TOR", self)
        self.start_button.setFont(custom_font)
        self.start_button.clicked.connect(self.start_tor)
        self.layout.addWidget(self.start_button)

        # Check Tor status button
        self.check_button = QPushButton("CHECK TOR STATUS", self)
        self.check_button.setFont(custom_font)
        self.check_button.clicked.connect(self.check_tor_status)
        self.layout.addWidget(self.check_button)

        # Status label
        self.status_label = QLabel("Tor status: Unknown", self)
        self.status_label.setFont(custom_font)
        self.layout.addWidget(self.status_label)

        # Apply Black and Blue style
        self.apply_black_blue_style()

    def apply_black_blue_style(self):
        # Set main window styles
        self.setStyleSheet("""
            QWidget {
                background-color: #000000;  /* Pure black background */
                color: #00BFFF;  /* Deep Sky Blue for text */
            }
            QLabel {
                color: #00BFFF;  /* Deep Sky Blue for labels */
            }
            QLineEdit {
                background-color: #000000;  /* Black background */
                color: #00BFFF;  /* Blue text */
                border: 2px solid #00BFFF;  /* Blue border */
                border-radius: 8px;
                padding: 5px;
            }
            QPushButton {
                background-color: #000000;  /* Black background */
                color: #00BFFF;  /* Blue text */
                border: 2px solid #00BFFF;  /* Blue border */
                border-radius: 8px;
                padding: 10px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #001F3F;  /* Slightly darker blue on hover */
                border: 2px solid #00BFFF;
                color: #00BFFF;
            }
            QPushButton:pressed {
                background-color: #00BFFF;  /* Blue background when pressed */
                color: #000000;  /* Black text when pressed */
            }
            QLabel#status_label {
                font-size: 12px;
                color: #00BFFF;  /* Deep Sky Blue for status text */
            }
        """)

    def start_tor(self):
        try:
            # Manually start Tor (runs in the background)
            subprocess.Popen(["tor"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            self.status_label.setText("Starting Tor...")
            QMessageBox.information(self, "Success", "Tor service started in the background.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to start Tor: {str(e)}")

    def check_tor_status(self):
        proxy_address = self.proxy_input.text().strip()

        if not proxy_address:
            QMessageBox.warning(self, "Error", "Proxy address cannot be empty!")
            return

        try:
            # Tor status check using curl through the proxy
            response = subprocess.run(
                ["curl", "--socks5-hostname", proxy_address, "https://check.torproject.org/"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )

            if "Congratulations. This browser is configured to use Tor." in response.stdout:
                self.status_label.setText("Tor connection is active!")
                QMessageBox.information(self, "Status", "Tor connection is active!")
            else:
                self.status_label.setText("Tor connection failed.")
                QMessageBox.warning(self, "Status", "Tor connection failed.")
        except Exception as e:
            self.status_label.setText("Failed to check Tor status.")
            QMessageBox.critical(self, "Error", f"Failed to check Tor status: {str(e)}")
