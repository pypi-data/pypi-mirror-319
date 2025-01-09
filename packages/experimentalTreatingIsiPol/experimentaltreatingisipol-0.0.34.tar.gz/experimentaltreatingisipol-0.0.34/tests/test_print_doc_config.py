import unittest
import sys
import os
sys.path.insert(0, os.path.join(os.getcwd(),r'src'))

print(os.getcwd())
from experimentalTreatingIsiPol.docConfig import print_docConfig

class TestPrintDocConfig(unittest.TestCase):

    def test_print_docConfig(self):
        """ Testing printing the docConfig example parameter."""
        self.assertEqual(type(print_docConfig()), str)
