from plover.translation import Translator
from plover.steno import Stroke


def prev_page(translator: Translator, stroke: Stroke, argument: str):
    translator.listening_lookup_state = "prev_page"


def next_page(translator: Translator, stroke: Stroke, argument: str):
    translator.listening_lookup_state = "next_page"


def listening_lookup_reload(translator: Translator, stroke: Stroke, argument: str):
    translator.listening_lookup_state = "listening_lookup_reload"
