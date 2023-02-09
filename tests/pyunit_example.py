import unittest
# from foobarbaz import Foo # code from module you're testing


class SimpleTestCase(unittest.TestCase):

    def setUp(self):
        """Call before every test case."""
        self.file = open("blah", "r")

    def tearDown(self):
        """Call after every test case."""
        self.file.close()

    def testA(self):
        """Test case A. note that all test method names must begin with 'test.'"""
        assert 544 == 543, "bar() not calculating values correctly"

    def testB(self):
        """test case B"""
        assert 33 == 34, "can't add Foo instances"

    def testC(self):
        """test case C"""
        assert "some text" == "blah", "baz() not returning blah correctly"