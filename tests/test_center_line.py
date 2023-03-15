import unittest
from simulator.center_line import Arc
import numpy as np

class TestArc(unittest.TestCase):
    def test_sample_at(self):
        a = Arc((0, 0), 10, np.pi/4, np.pi/2)
        self.assertAlmostEqual(a.get_length(), 10 * np.pi / 2)
        p, tangent = a.sample_at(a.get_length()/2)
        self.assertAlmostEqual(p[0], 0.0)
        self.assertAlmostEqual(tangent[0], -1)