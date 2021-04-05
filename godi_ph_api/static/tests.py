from django.test import TestCase

# Create your tests here.

def getAvg(x, y):
    func = lambda x, y: x * y
    if len(y) == 0:
        result = 0
    else:
        result = sum(list(map(func, x, y))) / sum(y)
    return round(result, 1)
if __name__ == "__main__":
    x = [1,2,3,4,5]
    y = [2,2,2,2,2]
    getAvg(x,y)