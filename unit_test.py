
import unittest

print 'dsfsdfsdfsdf'

def fun(x):
    return x + 1

class MyTest(unittest.TestCase):
    def test(self):
        self.assertEqual(fun(3), 4)
        self.assertEqual(1, 2)
