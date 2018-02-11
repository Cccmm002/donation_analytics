import math
import heapq


class MaxHeapObj(object):
    """An auxiliary object for building max heap."""

    def __init__(self, val):
        self.val = val

    def __lt__(self, other):
        return self.val > other.val

    def __eq__(self, other):
        return self.val == other.val

    def __str__(self):
        return str(self.val)


class MinHeap(object):
    """A wrapper for python's `heapq' package."""

    def __init__(self):
        self.heap = []

    def heappush(self, x):
        heapq.heappush(self.heap, x)

    def heappop(self):
        if len(self.heap) == 0:
            return None
        else:
            return heapq.heappop(self.heap)

    def heaptop(self):
        if len(self.heap) == 0:
            return None
        else:
            return self.heap[0]

    def __getitem__(self, i):
        if len(self.heap) <= i:
            return None
        else:
            return self.heap[i]

    def __len__(self):
        return len(self.heap)


class MaxHeap(MinHeap):
    """Max heap object using Python's `heapq' package."""

    def heappush(self, x):
        heapq.heappush(self.heap, MaxHeapObj(x))

    def heappop(self):
        if len(self.heap) == 0:
            return None
        else:
            return heapq.heappop(self.heap).val

    def heaptop(self):
        if len(self.heap) == 0:
            return None
        else:
            return self.heap[0].val

    def __getitem__(self, i):
        if len(self.heap) <= i:
            return None
        else:
            return self.heap[i].val


class RunningPercentile(object):
    """Use two heaps to maintain running percentile. Similar approach as running median.

    This method puts every element less or equal to nth percentile into a max heap,
    and all other elements larger than nth percentile into a min heap.
    Then the top element in the max heap is the nearest ranking nth percentile.

    Each 'add' method uses O(log n) time, and each time get a result takes O(1) time.
    Total amount is also recorded.
    """

    def __init__(self, percent):
        self.small = MaxHeap()
        self.large = MinHeap()
        self.percentile = percent
        self.total_amount = 0

    def __len__(self):
        return len(self.small) + len(self.large)

    def add(self, obj):
        self.total_amount += obj
        if len(self) == 0 or obj <= self.small.heaptop():
            self.small.heappush(obj)
        else:
            self.large.heappush(obj)
        count_total = len(self.small) + len(self.large)
        count_small = math.ceil(float(count_total)*self.percentile)
        while count_small != len(self.small):
            if count_small < len(self.small):
                self.large.heappush(self.small.heappop())
            else:
                self.small.heappush(self.large.heappop())

    def get_percentile(self):
        return self.small.heaptop()
