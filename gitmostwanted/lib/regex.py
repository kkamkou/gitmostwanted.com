import re


class SearchTerm:
    pattern = r'^[\w.-]{3,}$'

    def __init__(self, term: str):
        if re.match(self.pattern, term) is None:
            raise ValueError('The "{}" term is not suitable'.format(term))
        self.__term = term

    def __str__(self):
        return '%{}%'.format(self.__term)


class RepoFullName:
    pattern = (
        r'^(?:(?:https?://)?(?:www\.)?github\.com/)?'
        r'([a-zA-Z0-9](?:[a-zA-Z0-9-]{0,37}[a-zA-Z0-9])?/(?!\.+(?:\.git)?/?$)[a-zA-Z0-9._-]{1,80}?)'
        r'(?:\.git)?/?$'
    )

    def __init__(self, name: str):
        match = re.match(self.pattern, (name or '').strip())
        if match is None:
            raise ValueError('The repository name or URL is not valid')
        self.__name = match.group(1)

    def __str__(self):
        return self.__name
