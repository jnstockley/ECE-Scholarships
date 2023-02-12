'''
Sample PyUnit test
'''
import unittest
# from foobarbaz import Foo # code from module you're testing


class SimpleTestCase(unittest.TestCase):
    '''
    Example UnitTest
    '''

    def setUp(self):
        '''
        Run before every test
        :return:
        '''
        with open("blah", "r", encoding="utf-8") as file:
            self.file = file

    def tearDown(self):
        '''
        Run after every unit test
        :return:
        '''
        self.file.close()

    def test_a(self):
        """Test case A. note that all test method names must begin with 'test.'"""
        temp1 = 544
        temp2 = 543
        assert temp1 == temp2, "bar() not calculating values correctly"

    def test_b(self):
        """test case B"""
        temp1 = 33
        temp2 = 34
        assert temp1 == temp2, "can't add Foo instances"

    def test_c(self):
        """test case C"""
        temp1 = "some text"
        temp2 = "blah"
        assert temp1 == temp2, "baz() not returning blah correctly"
