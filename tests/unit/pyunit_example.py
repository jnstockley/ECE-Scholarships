'''
Sample PyUnit test
'''
import unittest
# from foobarbaz import Foo # code from module you're testing


class SimpleTestCase(unittest.TestCase):
    '''
    Example UnitTest
    '''

    def test_a(self):
        """Test case A. note that all test method names must begin with 'test.'"""
        temp1 = 544
        temp2 = 544
        assert temp1 == temp2, "equality not calculating values correctly"


if __name__ == '__main__':
    unittest.main()
