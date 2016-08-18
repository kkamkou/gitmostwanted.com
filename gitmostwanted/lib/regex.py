import re


class SearchTerm:
    pattern = '^[\w-.]{3,}$'

    def __init__(self, term: str):
        if re.match(self.pattern, term) is None:
            raise ValueError('The "{}" term is not suitable'.format(term))
        self.__term = term

    def __str__(self):
        return '%{}%'.format(self.__term)
