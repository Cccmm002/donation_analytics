# Introduction
This is a repeat donor analyzer for campaigns of United States federal elections. Data comes from Federal Election Commission.

# Algorithm
## Running Percentile
The major part of this analyzer is calculating running percentile. I use a similar approach as running median. Maintaining two heaps, one max heap and a min heap. Each time a new element comes in, make sure that the max heap contains all elements smaller or equal to nth percentile, while all elements that are larger than nth percentile stay in the min heap. Using this data structure, each adding element method takes O(log n) time.

`running_percentile.py` contains a generic data structure for running percentile that can be used. This implementation uses Python's heapq module. However, Python's heapq is a min heap. To build a max heap, we need some auxiliary class objects.

A unit test is built to test the running percentile part, which is set in `heap_unittest.py`.

## Detect repeat donors
As a donor with same name and same zip code can be identified as the same, a Donor class is used. To be used as key in Python dictionary, a hash function is written. All appeared donors are stored in a dictionary where years as values. Years are stored because we need to make sure it is appeared in previous years.

As running percentiles are calculated by each recipient, zip code and year, another key class is built. RunningPercentile heap is its value.

# How to run
This program is written by Python, composed by two files: `donation_analytics.py` and `running_percentile.py`. No third party modules are used, except for the unit test. It has three arguments, for two input files and one output file.

A sample run command line is:

`python ./src/donation_analytics.py ./input/itcont.txt ./input/percentile.txt ./output/repeat_donors.txt`

This code is well documented, following PEP guidelines.
