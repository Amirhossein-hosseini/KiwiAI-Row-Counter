import unittest
from analyzer import TCV

class TCVTests(unittest.TestCase):
    def test_counts_only_after_both_containers(self):
        tcv = TCV(); self.assertFalse(tcv.update(7, 30, 100)); self.assertFalse(tcv.update(7, 45, 100)); self.assertTrue(tcv.update(7, 70, 100)); self.assertFalse(tcv.update(7, 80, 100))

if __name__ == "__main__": unittest.main()
