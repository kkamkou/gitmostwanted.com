from collections import Iterator


class Result(Iterator):
    __total_rows = 0
    __rows = []
    __iter = 0

    def __init__(self, obj):
        self.__total_rows = int(obj['totalRows'])
        self.__rows = list(map(lambda x: x['f'], obj['rows']))

    def __next__(self):
        if self.__iter >= self.__total_rows:
            raise StopIteration()
        v, self.__iter = list(map(lambda x: x['v'], self.__rows[self.__iter])), self.__iter + 1
        return v
