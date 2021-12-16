def getLinesFromFile(path):
    with open(path) as input:
        return [''.join(filter(lambda c: c != '\n', s)) for s in input.readlines()]

def maxBy(elements, selector = None):
    elementList = list(elements)
    highestElement = elementList[0]
    highest = elementList[0] if selector == None else selector(elementList[0])
    if (selector == None):
        for e in elementList:
            if (e > highest):
                highest = e
                highestElement = e
    else:
        for e in elementList:
            if (selector(e) > highest):
                highest = selector(e)
                highestElement = e
    return highestElement
    
def minBy(elements, selector = None):
    elementList = list(elements)
    lowestElement = elementList[0]
    lowest = elementList[0] if selector == None else selector(elementList[0])
    if(selector == None):
        for e in elementList:
            if (e < lowest):
                lowest = e
                lowestElement = e
    else:
        for e in elementList:
            if (selector(e) < lowest):
                lowest = selector(e)
                lowestElement = e
    return lowestElement