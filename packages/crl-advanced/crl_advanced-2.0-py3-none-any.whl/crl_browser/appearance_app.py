from PyQt6.QtWidgets import (
    QApplication, QDialog, QVBoxLayout, QLabel, QPushButton, QRadioButton, 
    QFontComboBox, QSlider, QColorDialog, QMessageBox
)
from PyQt6.QtCore import Qt, pyqtSignal
import json


class SettingsManager:
    def __init__(self):
        self.settings = self.load_settings()

    def load_settings(self):
        """Load settings from a JSON file if it exists"""
        try:
            with open("settings.json", "r") as file:
                print("Settings file loaded successfully.")
                return json.load(file)
        except FileNotFoundError:
            # Varsayılan ayarlar
            print("Settings file not found, loading default settings.")
            return {
                "theme": "Light",
                "font": "Arial",
                "font_size": 16,
                "background_color": "#FFFFFF",
                "text_color": "#000000"
            }

    def save_settings(self):
        """Save current settings to a JSON file"""
        try:
            with open("settings.json", "w") as file:
                json.dump(self.settings, file)
            print("Settings saved successfully.")
        except Exception as e:
            print(f"Error saving settings: {e}")

    def update_setting(self, key, value):
        """Update a specific setting"""
        print(f"Updating setting: {key} = {value}")
        self.settings[key] = value
        self.save_settings()


def apply_global_styles(settings):
    """Apply global appearance settings to all widgets"""
    background_color = settings.get("background_color", "#FFFFFF")
    text_color = settings.get("text_color", "#000000")
    font = settings.get("font", "Arial")
    font_size = settings.get("font_size", 16)

    # Global style for all widgets
    style = f"""
        QWidget {{
            background-color: {background_color};
            color: {text_color};
            font-family: {font};
            font-size: {font_size}px;
        }}
        QLabel, QPushButton, QRadioButton, QFontComboBox, QSlider {{
            background-color: {background_color};
            color: {text_color};
            font-family: {font};
            font-size: {font_size}px;
        }}
    """
    QApplication.instance().setStyleSheet(style)
    print(f"Global style applied: {style}")


class AppearanceApp(QDialog):
    settings_changed = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.settings_manager = SettingsManager()

        self.init_ui()
        self.load_settings()

    def init_ui(self):
        """Initialize UI components"""
        self.setWindowTitle("Appearance Settings")
        self.resize(800, 600)

        main_layout = QVBoxLayout(self)

        # Tema seçimi
        self.light_theme_radio = QRadioButton("Light Theme", self)
        self.dark_theme_radio = QRadioButton("Dark Theme", self)
        main_layout.addWidget(self.light_theme_radio)
        main_layout.addWidget(self.dark_theme_radio)

        # Yazı tipi seçimi
        self.font_selector = QFontComboBox(self)
        main_layout.addWidget(QLabel("Select Font:", self))
        main_layout.addWidget(self.font_selector)

        # Yazı boyutu seçimi
        self.font_size_slider = QSlider(Qt.Orientation.Horizontal, self)
        self.font_size_slider.setRange(10, 30)
        main_layout.addWidget(QLabel("Adjust Font Size:", self))
        main_layout.addWidget(self.font_size_slider)

        # Arkaplan rengi seçimi
        self.bg_color_button = QPushButton("Choose Background Color", self)
        self.bg_color_button.clicked.connect(self.choose_background_color)
        self.bg_color_label = QLabel("Background Color: #FFFFFF", self)
        main_layout.addWidget(self.bg_color_button)
        main_layout.addWidget(self.bg_color_label)

        # Yazı rengi seçimi
        self.text_color_button = QPushButton("Choose Text Color", self)
        self.text_color_button.clicked.connect(self.choose_text_color)
        self.text_color_label = QLabel("Text Color: #000000", self)
        main_layout.addWidget(self.text_color_button)
        main_layout.addWidget(self.text_color_label)

        # Apply ve Close butonları
        apply_button = QPushButton("Apply", self)
        apply_button.clicked.connect(self.apply_changes)
        main_layout.addWidget(apply_button)

        close_button = QPushButton("Close", self)
        close_button.clicked.connect(self.close)
        main_layout.addWidget(close_button)

    def load_settings(self):
        """Load settings and update the UI"""
        settings = self.settings_manager.settings

        # Tema
        if settings.get("theme") == "Light":
            self.light_theme_radio.setChecked(True)
        else:
            self.dark_theme_radio.setChecked(True)

        # Yazı tipi
        self.font_selector.setCurrentText(settings.get("font", "Arial"))

        # Yazı boyutu
        self.font_size_slider.setValue(settings.get("font_size", 16))

        # Renkler
        self.bg_color_label.setText(f"Background Color: {settings.get('background_color', '#FFFFFF')}")
        self.text_color_label.setText(f"Text Color: {settings.get('text_color', '#000000')}")

    def choose_background_color(self):
        """Choose background color"""
        color = QColorDialog.getColor()
        if color.isValid():
            self.bg_color_label.setText(f"Background Color: {color.name()}")
            print(f"Background color chosen: {color.name()}")

    def choose_text_color(self):
        """Choose text color"""
        color = QColorDialog.getColor()
        if color.isValid():
            self.text_color_label.setText(f"Text Color: {color.name()}")
            print(f"Text color chosen: {color.name()}")

    def apply_changes(self):
        """Apply changes and save settings"""
        theme = "Light" if self.light_theme_radio.isChecked() else "Dark"
        font = self.font_selector.currentText()
        font_size = self.font_size_slider.value()
        bg_color = self.bg_color_label.text().replace("Background Color: ", "")
        text_color = self.text_color_label.text().replace("Text Color: ", "")

        print(f"Applying changes: Theme={theme}, Font={font}, Font Size={font_size}, Background Color={bg_color}, Text Color={text_color}")

        # Ayarları güncelle
        self.settings_manager.update_setting("theme", theme)
        self.settings_manager.update_setting("font", font)
        self.settings_manager.update_setting("font_size", font_size)
        self.settings_manager.update_setting("background_color", bg_color)
        self.settings_manager.update_setting("text_color", text_color)

        # Ayarların değiştiğini sinyal ile bildir
        self.settings_changed.emit()
        QMessageBox.information(self, "Settings Applied", "Your changes have been applied!")
        print("Settings applied successfully.")

        # Ayarları widget'lara uygula
        apply_global_styles(self.settings_manager.settings)  # Ayarları uygula


if __name__ == '__main__':
    app = QApplication([])
    settings_manager = SettingsManager()  # Global ayar yöneticisini başlat
    apply_global_styles(settings_manager.settings)  # Global stil ilk başta uygulanır
    window = AppearanceApp()
    window.show()
    app.exec()
