from PyQt5.QtWidgets import (
    QMenuBar, QTableWidget, QFrame, QGridLayout, 
    QHeaderView, QLabel, QPlainTextEdit, QAction, 
    QAbstractItemView
)
from PyQt5.QtCore import Qt, QSettings
from PyQt5.QtGui import QIcon, QKeySequence

from plover.engine import StenoEngine
from plover.gui_qt.tool import Tool
from plover.gui_qt.utils import ToolBar
from plover.gui_qt.suggestions_widget import SuggestionsWidget
from plover_listening_lookup.resources_rc import *
from plover_listening_lookup.listening_lookup_config import ListeningLookupConfig
from plover_listening_lookup.config_ui import ConfigUI


class ListeningLookupUI(Tool):
    #CHECK Not sure why this doesn't work.
    __doc__ = "Listens to plain keyboard and suggests strokes for detected words."

    TITLE = "Listening Lookup"
    ICON = ":/listening_lookup/ear.svg"
    ROLE = "listening_lookup"

    def __init__(self, engine: StenoEngine) -> None:
        super().__init__(engine)
        self.engine: StenoEngine = engine
        self.config = ListeningLookupConfig()
        self.restore_state()
        self.show_window()
        self.finished.connect(self.save_state)

    def _restore_state(self, settings: QSettings) -> None:        
        self.prev_pin = False
        if settings.contains("pinned") and settings.value("pinned", type=bool):
            self.prev_pin = True
            self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)
        
        if settings.contains("list_len"):
            self.config.list_len = settings.value("list_len", type=int)
                
        if not settings.contains("geometry"):
            self.resize(260, 400)
        
    def _save_state(self, settings: QSettings) -> None:
        settings.setValue("pinned", self.pin_action.isChecked())
        settings.setValue("list_len", self.config.list_len)

    def show_window(self) -> None:
        self.current_label = QLabel(self)
        self.current_label.setText("Current Word")

        self.current_word = QPlainTextEdit(self)
        self.current_word.setFixedHeight(30)
        self.current_word.setLineWrapMode(True)
        self.current_word.setReadOnly(True)
        self.current_word.setPlainText("Awaiting Input")

        self.suggestions_label = QLabel(self)
        self.suggestions_label.setText("Suggestions")

        self.suggestions_table = SuggestionsWidget(self)

        self.pin_action = QAction(self)
        self.pin_action.setCheckable(True)
        self.pin_action.setChecked(self.prev_pin)
        self.pin_action.setText("Pin window")
        self.pin_action.setToolTip("Keep this suggestion window on top.")
        self.pin_action.setIcon(QIcon(":/listening_lookup/pin.svg"))
        self.pin_action.triggered.connect(self.on_toggle_pin)
        self.pin_action.setShortcut(QKeySequence("Ctrl+P"))

        self.settings_action = QAction(self)
        self.settings_action.setText("Configure Listening Lookup.")
        self.settings_action.setIcon(QIcon(":/listening_lookup/settings.svg"))
        self.settings_action.triggered.connect(self.on_settings)
        self.settings_action.setShortcut(QKeySequence("Ctrl+S"))

        self.layout = QGridLayout()
        self.layout.addWidget(self.current_label, 0, 0, 1, 2)
        self.layout.addWidget(self.current_word, 1, 0, 1, 2)
        self.layout.addWidget(self.suggestions_label, 2, 0, 1, 2)
        self.layout.addWidget(self.suggestions_table, 3, 0, 1, 2)
        self.layout.addWidget(ToolBar(
            self.pin_action,
            self.settings_action
        ), 4, 0)
        self.setLayout(self.layout)

        self.show()
    
    def on_toggle_pin(self, _: bool = False) -> None:
        flags = self.windowFlags()

        if self.pin_action.isChecked():
            flags |= Qt.WindowStaysOnTopHint
        else:
            flags &= ~Qt.WindowStaysOnTopHint

        self.setWindowFlags(flags)
        self.show()

    def on_settings(self, *args) -> None:
        config_dialog = ConfigUI(self.config.copy(), self)
        if config_dialog.exec():
            self.config = config_dialog.temp_config

    def get_listening_lookup_config(self) -> ListeningLookupConfig:
        return self.config
