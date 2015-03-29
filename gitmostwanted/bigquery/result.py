from collections import Iterator, Sized


# @todo! add fields names from schema
class Result(Iterator, Sized):
    """Converts result of google-api-python-client"""

    def __init__(self, obj):
        self.iter = 0
        self.total_rows = int(obj['totalRows'])
        self.rows = list(map(lambda x: x['f'], obj['rows']))

    def __next__(self):
        if self.iter >= self.total_rows:
            raise StopIteration()
        v, self.iter = list(map(lambda x: x['v'], self.rows[self.iter])), self.iter + 1
        return v

    def __len__(self):
        return self.total_rows
