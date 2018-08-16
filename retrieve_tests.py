import unittest
from retrieve2 import *


class TestRetrieveFunctions(unittest.TestCase):
    
    def test_args_is_valid(self):
        self.assertFalse(args_is_valid(None))
        self.assertTrue(args_is_valid(['baseball']))
        self.assertTrue(args_is_valid([]))
        
    def test_parse_args(self):
        with self.assertRaises(InvalidArgumentException):
            parse_args(['retrieve2.py'])
        
        self.assertEqual(parse_args(['retrieve2.py','basketball']),['basketball'])
        
        
    def test_mode_most(self):
        self.assertEqual(mode_most([],make_invindex()),{})
        self.assertEqual(mode_most(['neurologist'],make_invindex()),{'neurologist': {'193.html': 1, '71.html': 1}})
        self.assertEqual(mode_most(['neurologist','yahoo','silent'],make_invindex()),{})
        self.assertEqual(mode_most(['ate','outburst','veget'],make_invindex()),{'ate' : {'227.html' : 1, '265.html' : 1}, 'outburst' : {'227.html' : 1, '265.html' : 1}})
        
    def test_tf_score(self):
        docs = get_doc_file()
        mosts = mode_most(['ate','outburst','veget'],make_invindex())
        self.assertEqual(tf_score(docs,mosts),{'ate': {'227.html': 0.0020325203252032522, '265.html': 0.002053388090349076}, 'outburst': {'227.html': 0.0020325203252032522, '265.html': 0.002053388090349076}})
        self.assertEqual(tf_score(docs,{}),{})
        self.assertEqual(tf_score(docs,{'selfi' : {'69.html' : 1}}),{'selfi': {'69.html': 0.0033003300330033004}})
        
    def test_idf_score(self):
        docs = get_doc_file()
        total_files = len(docs)
        mosts = mosts = mode_most(['ate','outburst','veget'],make_invindex())
        idf_scores = idf_score(total_files,mosts)
        
        self.assertEqual(idf_scores,{'ate': 6.214608098422191, 'outburst': 6.214608098422191})
        self.assertEqual(idf_score(total_files,{}),{})
        self.assertEqual(idf_score(total_files,{'selfi' : {'69.html' : 1}}),{'selfi': 6.907755278982137})
        
    def test_tf_idf_score(self):
        docs = get_doc_file()
        total_files = len(docs)
        mosts = mosts = mode_most(['selfi'],make_invindex())
        tf_scores = tf_score(docs,mosts)
        idf_scores = idf_score(total_files,mosts)
        tfidf = tf_idf_score(tf_scores,idf_scores)
        
        self.assertEqual(tfidf,{'69.html': 0.02279787220786184})
        mosts2 = mode_most(['ate','outburst','veget'],make_invindex())
        tf_scores2 = tf_score(docs,mosts2)
        idf_scores2 = idf_score(total_files,mosts2)
        tfidf2 = tf_idf_score(tf_scores2,idf_scores2)
        self.assertEqual(tfidf2,{'227.html': 0.025262634546431677, '265.html': 0.025522004510974094})
        
        
if __name__ == '__main__':
    unittest.main()



