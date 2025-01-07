from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5.QtCore import pyqtSignal

from typing import Dict, Tuple, List, Optional, Any

from plover import system
from plover import log
from plover.engine import StenoEngine
from plover.registry import registry
from plover.steno import Stroke
from plover.steno_dictionary import StenoDictionary, StenoDictionaryCollection
from plover.translation import Translation
from plover.oslayer.keyboardcontrol import KeyboardCapture

log.debug("PLL: load listening_lookup_suggestions")

from plover_listening_lookup.listening_lookup_ui import ListeningLookupUI


STROKE_TYPE = str
OUTLINE_TYPE = Tuple[STROKE_TYPE]


class TranslationNode:
    def __init__(self, translation: str = "") -> None:
        self.translation = translation
        self.children: Dict[STROKE_TYPE, "TranslationNode"] = {}

    def add_child(self, outline: OUTLINE_TYPE, translation: str) -> None:
        if not outline:
            return
        
        outline_len = len(outline)
        outline_head = outline[0]

        if outline_len == 1:
            if outline_head in self.children:
                self.children[outline_head].translation = translation
            else:
                self.children[outline_head] = TranslationNode(translation)
        else:
            outline_tail = outline[1:]
            if outline_head not in self.children:
                self.children[outline_head] = TranslationNode()
            
            self.children[outline_head].add_child(outline_tail, translation)
    
    def get_node(self, outline: OUTLINE_TYPE) -> Optional["TranslationNode"]:
        if not outline:
            return self

        outline_head = outline[0]
        if outline_head not in self.children:
            return None
        else:
            return self.children[outline_head].get_node(outline[1:])

    def get_suggestions(self) -> List[Tuple[OUTLINE_TYPE, str]]:
        suggestions_list = []

        if self.children:
            for stroke, node in self.children.items():
                if node.translation:
                    suggestions_list.append(([stroke], node.translation))

                node_suggestions = node.get_suggestions()
                for outline, translation in node_suggestions:
                    suggestions_list.append(([stroke] + outline, translation))
        
        return suggestions_list

'''
SCANCODE_TO_KEY = {
    59: 'F1', 60: 'F2', 61: 'F3', 62: 'F4', 63: 'F5', 64: 'F6',
    65: 'F7', 66: 'F8', 67: 'F9', 68: 'F10', 87: 'F11', 88: 'F12',
    41: '`', 2: '1', 3: '2', 4: '3', 5: '4', 6: '5', 7: '6', 8: '7',
    9: '8', 10: '9', 11: '0', 12: '-', 13: '=', 16: 'q',
    17: 'w', 18: 'e', 19: 'r', 20: 't', 21: 'y', 22: 'u', 23: 'i',
    24: 'o', 25: 'p', 26: '[', 27: ']', 43: '\\',
    30: 'a', 31: 's', 32: 'd', 33: 'f', 34: 'g', 35: 'h', 36: 'j',
    37: 'k', 38: 'l', 39: ';', 40: '\'', 44: 'z', 45: 'x',
    46: 'c', 47: 'v', 48: 'b', 49: 'n', 50: 'm', 51: ',',
    52: '.', 53: '/', 57: 'space', 58: "BackSpace", 83: "Delete",
    80: "Down", 79: "End", 1: "Escape", 71: "Home", 82: "Insert",
    75: "Left", 73: "Page_Down", 81: "Page_Up", 28 : "Return",
    77: "Right", 15: "Tab", 72: "Up",
}
'''
WORD_KEYS = [
    'a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z',
]
# ...I'mma just treat everything else as a break key.
#RAINY Might be nice to try to handle some of them; arrows and backspace etc.

class ListeningLookupSuggestions(ListeningLookupUI):
    _update_signal = pyqtSignal()

    def __init__(self, engine: StenoEngine) -> None:
        super().__init__(engine)

        log.debug("PLL.LLS: init")

        self._translate_tree = None
        self._suggestions: List[Tuple[OUTLINE_TYPE, str]] = []
        self._prev_node: Optional[TranslationNode] = None
        self._page = 0

        self._stroke_formatter: Optional[Callable[[STROKE_TYPE], STROKE_TYPE]] = None
        self._translation_formatter: Optional[Callable[[str], str]] = None
        self._system_sorter: Optional[Callable[[Tuple[OUTLINE_TYPE, str]], Any]] = None
        self._keyboard_capture: Optional[KeyboardCapture] = None
        self._last_words: List[str] = []
        self._current_word: str = ""
        self._update_signal.connect(self._update_ui)

        # Not sure these are needed
        engine.signal_connect("dictionaries_loaded", self.on_dict_update)
        engine.signal_connect("config_changed", self.on_config_changed)
        engine.signal_connect("add_translation", self.on_dict_update)
        self.index_dictionaries()
        self.on_config_changed()
        try:
            self.start_capture()
        except Exception as e:
            log.error('PLL.LLS: ERROR! %s', e)

    def closeEvent(self, event):
        log.debug("PLL.LLS: closeEvent")
        self.stop_capture()
        super().closeEvent(event)

    def start_capture(self):
        """Begin listening for output from the stenotype machine."""
        # self._initializing()
        try:
            self._keyboard_capture = KeyboardCapture()
            self._keyboard_capture.key_down = self._key_down
            self._keyboard_capture.key_up = self._key_up
            self._keyboard_capture.start()
            # self._update_suppression()
            self._keyboard_capture.suppress(())
        except:
            # self._error()
            raise
        # self._ready()

    def stop_capture(self):
        """Stop listening for output from the stenotype machine."""
        if self._keyboard_capture is not None:
            # self._is_suppressed = False
            # self._update_suppression()
            self._keyboard_capture.cancel()
            self._keyboard_capture = None
        # self._stopped()

    def _key_down(self, key):
        """Called when a key is pressed."""
        assert key is not None
        # log.debug("PLL.LLS: key_down %s" % key)

    def _key_up(self, key):
        """Called when a key is released."""
        assert key is not None
        # log.debug("PLL.LLS: key_up %s" % key)
        if key in WORD_KEYS:
            self._current_word += key
        elif key == 'BackSpace':
            if len(self._current_word) > 0:
                self._current_word = self._current_word[:-1]
        else:
            # Word is done I guess
            if len(self._current_word.strip()) > 0:
                self._last_words.append(self._current_word)
                while len(self._last_words) > self.config.list_len:
                    self._last_words.pop(0)
            self._current_word = ""
        self._update_signal.emit()

    def _update_ui(self):
        #LEAK It's not especially efficient to redo the table on every keypress
        self.suggestions_table.clear()

        # Current word
        word = self._current_word
        word = word.strip()
        if len(word) > 0:
            log.debug("PLL.LLS: word \"%s\"" % word)
            suggestion_list = self._engine.get_suggestions(word)
            log.debug("PLL.LLS: translations: %s" % suggestion_list)
            self.suggestions_table.append(suggestion_list)
            self.current_word.setPlainText(word)

        # Previous words
        prev_words = self._last_words.copy()
        prev_words.reverse()
        for word in prev_words:
            word = word.strip()
            if len(word) == 0:
                continue
            suggestion_list = self._engine.get_suggestions(word)
            #THINK Notably, if there aren't any suggestions, nothing gets added to the list
            self.suggestions_table.append(suggestion_list)

        if self._current_word == "scroll":
            log.debug("scroll scroll scroll")
            self.suggestions_table.scrollToTop()

        if self._current_word == "clear":
            log.debug("clear clear clear")
            self._last_words.clear()
            self.suggestions_table.clear()


    def on_stroke(self, _: tuple) -> None:
        pass

    def index_dictionaries(self) -> None:
        self._update_signal.emit()
        self._translate_tree = TranslationNode()
        dictionaries: StenoDictionaryCollection = self.engine.dictionaries

        dictionary: StenoDictionary
        for dictionary in dictionaries.dicts:
            if dictionary.enabled:
                for outline, translation in dictionary.items():
                    self._translate_tree.add_child(outline, translation)

    def on_dict_update(self) -> None:
        self.index_dictionaries()
    
    def on_config_changed(self) -> None:
        self._update_signal.emit()
        system_name = system.NAME
        system_mod = registry.get_plugin("system", system_name).obj

        self._stroke_formatter = getattr(system_mod, "LL_STROKE_FORMATTER", None)
        self._translation_formatter = getattr(system_mod, "LL_TRANSLATION_FORMATTER", None)
        self._system_sorter = getattr(system_mod, "LL_SORTER", None)
