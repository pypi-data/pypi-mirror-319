# Listening Lookup for Plover
[![PyPI](https://img.shields.io/pypi/v/plover-listening-lookup)](https://pypi.org/project/plover-listening-lookup/)
![GitHub](https://img.shields.io/github/license/Erhannis/plover_listening_lookup)

This is a Plover plugin that listens to normal keyboard keypresses and gives suggested strokes for each detected word, as though you were typing into the built-in Lookup window.  Intended for learners to get a feel for words while still typing normally.

Warning: this does listen to your keyboard (as does Plover), so you might want to e.g. minimize or close it before typing any passwords.

Based off https://github.com/Kaoffie/plover_next_stroke .  There might be some leftover code I missed.

## Installation

You can install this plugin using the built-in Plover Plugin Manager, under the name `plover-listening-lookup`.

Or:
```
sudo apt install pyqt5-dev-tools
plover -s plover_plugins install --force PyQt5
plover -s plover_plugins install git+https://github.com/Erhannis/plover_listening_lookup.git#egg=plover_listening_lookup
```
(Not sure if ALL those steps are needed, but I think that's what worked for me.)<br/>
(I think you can also clone it and do `plover -s plover_plugins install PATH_TO_REPO`?  Might need to do a `pip install .` or st first, or maybe `python3 setup.py build_py build_ui`?)<br/>

## License & Credits

This plugin is licensed under the MIT license.

The icons used in this plugin are taken from [Icons8 Flat Color Icons](https://github.com/icons8/flat-color-icons), or from [https://publicdomainvectors.org](https://publicdomainvectors.org).
