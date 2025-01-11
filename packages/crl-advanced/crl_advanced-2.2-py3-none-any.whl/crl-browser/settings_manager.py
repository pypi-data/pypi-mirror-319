from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QListWidget, QVBoxLayout, QHBoxLayout, QWidget, QPushButton, QFrame
from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.QtCore import Qt, QTimer, QProcess
import os
import sys
from tor_proxy_app import TorProxyPanel
from privacy_app import PrivacyApp
from historymanager import HistoryApp
from appearance_app import AppearanceApp
from sysmanager import SystemApp
from about import AboutApp

    

  
 
class SettingsManager(QMainWindow):
   
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CRL Browser - Settings Manager")
        self.setGeometry(100, 100, 1000, 650)
        icon_path = self.get_icon_path()

        self.setWindowIcon(QIcon(icon_path))
       
        # Ana widget ve düzen
        main_widget = QWidget()
        main_layout = QVBoxLayout(main_widget)

        # Üst çubuk: Logo ve başlık
        self.top_bar = self.create_top_bar()

        # Ana içerik düzeni
        content_layout = QHBoxLayout()

        # Sol menü (ayarlar listesi)
        self.menu_list = QListWidget()
        self.menu_list.setStyleSheet("""
            QListWidget {
                background-color: #101010;
                border-right: 2px solid #00FFFF;
                font-size: 18px;
                color: #00FFFF;
                padding: 5px;
            }
            QListWidget::item {
                padding: 10px;
            }
            QListWidget::item:selected {
                background-color: #00FFFF;
                color: #101010;
                font-weight: bold;
            }
        """)
        self.menu_list.addItems(["Tor Proxy Settings","History", "Privacy", "Appearance", "System", "About"])
        self.menu_list.setFixedWidth(200)
        self.menu_list.currentRowChanged.connect(self.display_settings)

        # Sağ içerik alanı (ayar ekranları)
        self.right_panel = QWidget()  # QLabel yerine QWidget kullanıyoruz
        self.right_panel_layout = QVBoxLayout(self.right_panel)  # Layout ekliyoruz
        self.right_panel.setStyleSheet("""
            QWidget {
                background-color: #0F0F0F;
                color: #00FFFF;
                font-size: 18px;
                padding: 20px;
                border: none;
            }
        """)

        general_layout = QVBoxLayout()
        executables = [
            ("Tor Proxy", "tor_proxy_panel"),
            ("Privacy", "privacy_panel"),
            ("History", "history_panel"),
            ("Appearance", "appearance_panel"),
            ("System", "system_panel"),
            ("About", "about_panel")
        ]
        for name, executable in executables:
            button = QPushButton(name)
            button.setStyleSheet("""
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
            button.clicked.connect(lambda _, exe=executable, label=name: self.run_executable(exe, label))
            general_layout.addWidget(button)

        general_widget = QWidget()
        general_widget.setLayout(general_layout)

        # İçerik düzeni
        content_layout.addWidget(self.menu_list)  # Sol menü
        content_layout.addWidget(self.right_panel, 3)  # Sağ panel
        content_layout.setStretch(0, 1)

        # Ana düzenin yapılandırılması
        main_layout.addWidget(self.top_bar)  # Üst çubuk
        main_layout.addLayout(content_layout)  # Ana içerik

        # Ana widget'i ayarla
        self.setCentralWidget(main_widget)

        # Cyberpunk stilini uygula
        self.setStyleSheet("background-color: #0F0F0F; color: #00FFFF;")

        # Yürütülebilir dosyalar için bir kontrol listesi
        self.running_process = None
    def get_icon_path(self):
    # Platforma göre uygun simge yolunu belirle
     if sys.platform == "win32":
        # Windows yolu, kullanıcının AppData dizinine göre belirleniyor
        icon_path = os.path.join(os.getenv('USERPROFILE'), 'AppData', 'Local', 'crl-browser', 'icons', 'icon.png')
     elif sys.platform == "darwin":
        # macOS yolu, genellikle uygulama paket yapısının içindeki Resources dizininde bulunur
        icon_path = os.path.join(os.path.expanduser('~'), 'Library', 'Application Support', 'crl-browser', 'icons', 'icon.png')
     else:
        # Linux için, ~/.local/share/crl-browser altında belirtilen yol
        icon_path = os.path.join(os.path.expanduser('~'), '.local', 'share', 'crl-browser', 'icons', 'icon.png')

     return icon_path

    def create_top_bar(self):
        """Üst çubuğu oluştur (ikon ve başlık içeren çubuk)."""
        top_bar = QFrame()
        top_bar.setStyleSheet("""
            QFrame {
                background-color: #101010;
                border-bottom: 2px solid #00FFFF;
                height: 60px; def apply_global_styles(settings):
        #function
            }
        """)
        top_layout = QHBoxLayout(top_bar)
        top_layout.setContentsMargins(10, 0, 10, 0)

        # Uygulama ikonu
        icon_label = QLabel()
        icon_label.setPixmap(QPixmap("icon.webp").scaled(40, 40, Qt.AspectRatioMode.KeepAspectRatio))
        top_layout.addWidget(icon_label, alignment=Qt.AlignmentFlag.AlignLeft)

        # Uygulama başlığı
        title_label = QLabel("CRL Browser - Settings Manager")
        title_label.setStyleSheet("""
            QLabel {
                font-size: 20px;
                font-weight: bold;
                color: #00FFFF;
            }
        """)
        top_layout.addWidget(title_label, alignment=Qt.AlignmentFlag.AlignLeft)

        # Sağ taraf boşluk
        top_layout.addStretch()

        return top_bar
    def run_executable(self, executable, label):

    
    # Önceki süreç varsa durdur
     if self.running_process:
        self.running_process.terminate()
        self.running_process.waitForFinished()  # İşlemin tamamen sonlanmasını bekleyin

    # Var olan içerikleri temizle
     for i in reversed(range(self.right_panel_layout.count())):
        widget = self.right_panel_layout.itemAt(i).widget()
        if widget is not None:
            widget.deleteLater()

    # Yeni işlemi başlat
     self.running_process = QProcess(self)
     self.running_process.start(executable)

    # Paneli açmak için açma fonksiyonunu çağır
     QTimer.singleShot(2000, lambda: self.open_dialog(executable, label))

    
   
    def open_dialog(self, executable, label):
        """Yürütülebilir dosyayı bir panel olarak aç."""
        if executable == "tor_proxy_panel":
            self.open_tor_proxy_panel()
        elif executable == "privacy_panel":
            self.open_privacy_panel()
        elif executable == "history_panel":
            self.open_history_panel()
        elif executable == "appearance_panel":
            self.open_appearance_panel()
        elif executable == "system_panel":
            self.open_system_panel()
        elif executable == "about_panel":
            self.open_about_panel()
    
    
    def open_tor_proxy_panel(self):
        self.right_panel_layout.setContentsMargins(0, 0, 0, 0)  # Var olan içerikleri temizle
        self.tor_proxy_panel = TorProxyPanel()  # TorProxyPanel sınıfını kullan
        self.right_panel_layout.addWidget(self.tor_proxy_panel)  # Layout'a ekle
    
   

    def open_privacy_panel(self):
        """Privacy Panel'ini aç."""
        self.right_panel_layout.setContentsMargins(0, 0, 0, 0)  # Var olan içerikleri temizle
        self.privacy_panel = PrivacyApp()  # PrivacyApp sınıfını kullan
        self.right_panel_layout.addWidget(self.privacy_panel)
    def open_history_panel(self):
        self.right_panel_layout.setContentsMargins(0, 0, 0, 0)  # Var olan içerikleri temizle
        self.history_panel = HistoryApp()  # PrivacyApp sınıfını kullan
        self.right_panel_layout.addWidget(self.history_panel)

    def open_appearance_panel(self):
        """Appearance Panel'ini aç."""
        self.right_panel_layout.setContentsMargins(0, 0, 0, 0)  # Var olan içerikleri temizle
        self.appearance_panel = AppearanceApp()  # AppearanceApp sınıfını kullan
        self.right_panel_layout.addWidget(self.appearance_panel)

    def open_system_panel(self):
        """System Panel'ini aç."""
        self.right_panel_layout.setContentsMargins(0, 0, 0, 0)  # Var olan içerikleri temizle
        self.system_panel = SystemApp()  # SystemApp sınıfını kullan
        self.right_panel_layout.addWidget(self.system_panel)

    def open_about_panel(self):
        """About Panel'ini aç."""
        self.right_panel_layout.setContentsMargins(0, 0, 0, 0)  # Var olan içerikleri temizle
        self.about_panel = AboutApp()  # AboutApp sınıfını kullan
        self.right_panel_layout.addWidget(self.about_panel)
    
    def display_settings(self, index):
    
        setting = self.menu_list.item(index).text()
    
        if setting == "Tor Proxy Settings":
           QTimer.singleShot(2000, lambda: self.run_executable("tor_proxy_panel", "Tor Proxy"))
        elif setting == "Privacy":
           QTimer.singleShot(2000, lambda: self.run_executable("privacy_panel", "Privacy"))
        elif setting == "History":
           QTimer.singleShot(2000, lambda: self.run_executable("history_panel", "History"))
        elif setting == "Appearance":
           QTimer.singleShot(2000, lambda: self.run_executable("appearance_panel", "Appearance"))
        elif setting == "System":
          QTimer.singleShot(2000, lambda: self.run_executable("system_panel", "System"))
        elif setting == "About":
          QTimer.singleShot(2000, lambda: self.run_executable("about_panel", "About"))



if __name__ == '__main__':
    app = QApplication(sys.argv)  # QApplication'ı başlat
    window = SettingsManager()  # Ana pencereyi oluştur
    window.show()  # Pencereyi göster
    sys.exit(app.exec()) 
