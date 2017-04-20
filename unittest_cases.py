from __future__ import division
import unittest
import pytest
import csv
import sys
import math
import test_source_code
import pandas as pd
from test_source_code import get_median
from test_source_code import get_lower_half
from test_source_code import get_upper_half
from test_source_code import calculate_score
from test_source_code import normalize
from test_source_code import show_results


median_list1 = [0, 12, 24, 35, 100]

# Testcase1: To test the functionality of get_median function 
def test_get_median1():
	assert get_median(median_list1) == 24
	
# Testcase2: To test the functionality of get_lower_half function	
def test_get_lower_half1():
	assert get_lower_half(median_list1) == [0, 12]
	
# Testcase3: To test the functionality of get_upper_half function
def test_get_upper_half1():
	assert get_upper_half(median_list1) == [35, 100]
	
median_list2 = [12, 24]

'''
Testcase (4,5,6): To test the functionality of get_median, get_lower_half
				  and get_upper_half when there are only two values in the list
				  or even number of elements in the list
'''

# Testcase4
def test_get_median2():
	assert get_median(median_list2) == 18
	
# Testcase5
def test_get_lower_half2():
	assert get_lower_half(median_list2) == [12]

# Testcase6	
def test_get_upper_half2():
	assert get_upper_half(median_list2) == [24]

median_list3 = [12]

# Testcase7: To test the get_median function when there is only one element
def test_get_median3():
	assert get_median(median_list3) == 12
	
# Testcase8: To test the functionality of normalize function
def test_normalize1():
	list = [43.21, 163.30, 43.50, 26.40, 74.25]
	assert normalize(list) == [12, 100, 12, 0, 35]

# Testcase9: To test the functionality of normalize function when there is only one element
def test_normalize2():
	list = [43.21]
	assert normalize(list) == [0]

# Testcase10: To test whether the weighted scores are calculated correctly 
def test_calculate_score():

	freader = pd.read_csv('data.csv')
	fscore = [34.33, 4.08, 4.8, 110.8, 22.5, 30.0, 35.5, 8.0, 5.3999999999999995, 21.0, 36.0, 38.25]
	assert calculate_score(freader) == fscore
	
# Testcase11: To test whether the final result (quartile labels) are obtained correctly
def test_show_results():
	dict = [{'Id': 1, 'normalized_score': 12},
			{'Id': 2, 'normalized_score': 100},
			{'Id': 3, 'normalized_score': 12},
			{'Id': 4, 'normalized_score': 0},
			{'Id': 5, 'normalized_score': 35}]
	df = pd.DataFrame(dict)
	expected = ['silver', 'platinum', 'silver', 'bronze', 'gold']
	assert show_results(df) == expected
	

	
if __name__ == '__main__':
	unittest.main()
	
