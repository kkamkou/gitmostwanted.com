class Status:
    def __init__(self, status: str):
        if status not in ('promising', 'new', 'unknown', 'deleted', 'hopeless'):
            raise ValueError('Unknown status')
        self.__status = status

    def __str__(self):
        return self.__status
