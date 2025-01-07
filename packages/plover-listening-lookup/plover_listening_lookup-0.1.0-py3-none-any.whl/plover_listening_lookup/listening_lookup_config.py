

CONFIG_ITEMS = {
    "list_len": 4
}


class ListeningLookupConfig:
    def __init__(self, values: dict = None):
        if values is None:
            values = dict()

        for key, default in CONFIG_ITEMS.items():
            if key in values:
                setattr(self, key, values[key])
            else:
                setattr(self, key, default)

    def copy(self) -> "ListeningLookupConfig":
        value_dict = {k: getattr(self, k) for k in CONFIG_ITEMS.keys()}
        return ListeningLookupConfig(value_dict)
