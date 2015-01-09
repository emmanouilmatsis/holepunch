# python -m unittest discover myproject/tests/ 'test*.py' myproject/

import unittest

class TestTemplate(unittest.TestCase):
    """
    Test Template
    """

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test(self):
        a = 0
        b = 0
        self.assertEqual(a, b)
        #...
