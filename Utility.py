def getLinesFromFile(path):
    with open(path) as input:
        return [''.join(filter(lambda c: c != '\n', s)) for s in input.readlines()]
