from urllib.parse import urlparse


class Url:
    def __init__(self, url: str):
        url = url.strip()
        if url.find('://') == -1:
            url = '//' + url
        self.__url = urlparse(url, 'http')

    def __str__(self):
        return self.__url.geturl()
