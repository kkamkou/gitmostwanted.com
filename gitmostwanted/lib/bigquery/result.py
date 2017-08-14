from collections import Iterator, Sized


class ResultBase:
    pass


class ResultWithRows(ResultBase, Iterator, Sized):
    def __init__(self, obj: str):
        self.__iter = 0
        self.__total_rows = int(obj['totalRows'])
        self.__rows = list(map(lambda x: x['f'], obj['rows']) if self.__total_rows > 0 else [])

    def __next__(self):
        if self.__iter >= self.__total_rows:
            raise StopIteration()
        v, self.__iter = list(map(lambda x: x['v'], self.__rows[self.__iter])), self.__iter + 1
        return v

    def __len__(self):
        return self.__total_rows


class ResultJob(ResultWithRows):  # @todo 3h add field names from schema
    pass
