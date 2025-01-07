from PyQt5.QtWidgets import (
    QDialog, QWidget, QLabel, QSpinBox, 
    QComboBox, QDialogButtonBox, QGridLayout
)

from plover_listening_lookup.listening_lookup_config import ListeningLookupConfig


class ConfigUI(QDialog):

    def __init__(self, temp_config: ListeningLookupConfig, parent: QWidget = None) -> None:
        super().__init__(parent)
        self.temp_config = temp_config
        self.setup_window()

    def setup_window(self) -> None:
        self.resize(350, 200)

        self.list_len_label = QLabel(self)
        self.list_len_label.setText("List Length")
        
        self.list_len_box = QSpinBox(self)
        self.list_len_box.setValue(self.temp_config.list_len)
        self.list_len_box.setRange(1, 100)

        self.button_box = QDialogButtonBox(
            (
                QDialogButtonBox.Cancel | 
                QDialogButtonBox.Ok
            ),
            parent=self
        )
        self.button_box.rejected.connect(self.reject)
        self.button_box.accepted.connect(self.save_settings)

        self.layout = QGridLayout()
        self.layout.addWidget(self.list_len_label, 0, 0)
        self.layout.addWidget(self.list_len_box, 0, 1)
        self.layout.addWidget(self.button_box, 1, 0, 2, 1)
        self.setLayout(self.layout)

    def save_settings(self) -> None:
        self.temp_config.list_len = self.list_len_box.value()
        
        self.accept()
