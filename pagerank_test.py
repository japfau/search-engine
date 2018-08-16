import unittest
from pagerank import *

class TestPageRank(unittest.TestCase):

    def test_args_is_valid(self):
	with self.assertRaises(InvalidArgumentsException):
	    args_is_valid(['pagerank.py'])
        self.assertTrue(args_is_valid(['pagerank.py', 'graph'])) 

    def test_get_inlinks(self):
	test_graph = {'0' : ['1','2'], '1' : ['2'], '2' : ['1'], '3' : ['2']} 
	self.assertEqual(get_inlinks(test_graph),{'1': ['0', '2'], '0': [], '3': [], '2': ['1', '0', '3']}) 
        self.assertEqual(get_inlinks({}),{})

    def test_page_rank(self):
	graph = {'0': [], '1': [], '2': [],  '3': [], '4': []}
	self.assertEqual(pagerank(graph), {'0': 0.16999999999999998, '1': 0.16999999999999998, '2': 0.16999999999999998, '3': 0.16999999999999998, '4': 0.16999999999999998})   
        graph2 = {'0' : ['1'] , '1' : ['2'] , '2' : ['3'] , '3' : []}
	self.assertEqual(pagerank(graph2),{'1': 0.244375, '0': 0.2125, '3': 0.2498734375, '2': 0.24915625})
        graph3 =  {'1' : ['2','3'], '2' : ['3'], '3' : ['1'], '4' : ['3']}
	self.assertEqual(pagerank(graph3), {'1': 0.2572658772874058, '2': 0.23179494079655544, '3': 0.29843918191603874, '4': 0.2125})

if __name__ == '__main__':

    unittest.main()
