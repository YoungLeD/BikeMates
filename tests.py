import unittest


# Empty test suite
# [TODO at future] How to test flask applications:
# http://flask.pocoo.org/docs/0.12/testing/

class FirstTestCase(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_empty(self):
        self.assertEqual(1 + 1, 2)


if __name__ == '__main__':
    unittest.main()
