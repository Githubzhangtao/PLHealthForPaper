from django.test import TestCase

# Create your tests here.


if __name__ == "__main__":
    dict1 = {(0, 20): 0, (21, 40): 0, (41, 60): 0, (61, 80): 0, (81, 100): 0}
    dict1.update('(0,20)',dict1.pop())