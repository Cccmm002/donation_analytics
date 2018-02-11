import unittest
import numpy as np
from running_percentile import RunningPercentile


class TestHeap(unittest.TestCase):
    def test_heap(self):
        n = 500
        arr = np.random.randint(0, high=100, size=n + 1)
        arr[0] = -1
        for i in range(1, 100):
            p = RunningPercentile(float(i)/100.0)
            for j in range(n):
                p.add(arr[j + 1])
                self.assertEqual(p.get_percentile(), np.percentile(arr[:j + 2], i, interpolation='higher'))


if __name__ == '__main__':
    unittest.main()
