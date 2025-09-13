def get_sort(sort="created_at"):
    if sort:
        if sort.startswith('-'):
            sort = (sort[1:], -1)
        else:
            sort = (sort, 1)
    return sort