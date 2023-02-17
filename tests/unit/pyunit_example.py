'''
Sample PyUnit test
'''
import unittest

class SimpleTestCase(unittest.TestCase):
    '''
    Example UnitTest
    '''

    def test_a(self):
        """Test case A. note that all test method names must begin with 'test.'"""
        temp1 = 544
        temp2 = 544
        assert temp1 == temp2, "equality not calculating values correctly"

    def test_hello(self):
        """Testing hello world!"""
        #assert hello() == 'hello world'


if __name__ == '__main__':
    unittest.main()
