import re
import unicodedata


class TextWithoutSmilies:
    pattern = '\s*:[a-z0-9_-]+:\s*'

    def __init__(self, text: str):
        self.__text = text

    def __str__(self):
        return re.sub(self.pattern, ' ', self.__text)


class TextNormalized:
    def __init__(self, text: str):
        self.__text = unicodedata.normalize('NFC', text.strip())

    def __str__(self):
        return self.__text.encode(errors='ignore').decode()
