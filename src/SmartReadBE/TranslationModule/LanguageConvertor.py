language_map = {
    "English": "en",
    "Chinese": "zh",
    "French": "fr",
    "Japanese": "ja",
    "Italian": "it",
}


def convert_language(full_name):
    return language_map.get(full_name)
