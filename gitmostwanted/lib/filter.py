import math


def number_humanize(n):
    return n if n < 1000 else '{}k'.format(round(n / 1000, 1)).replace('.0', '')
