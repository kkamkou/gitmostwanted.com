from collections import Iterator, Sized


# @todo! add fields names from schema
class Result(Iterator, Sized):
    """Converts result of google-api-python-client"""

    def __init__(self, obj):
        self.__iter = 0
        self.__total_rows = int(obj['totalRows'])
        self.__rows = list(map(lambda x: x['f'], obj['rows']))

    def __next__(self):
        if self.__iter >= self.__total_rows:
            raise StopIteration()
        v, self.__iter = list(map(lambda x: x['v'], self.__rows[self.__iter])), self.__iter + 1
        return v

    def __len__(self):
        return self.__total_rows
