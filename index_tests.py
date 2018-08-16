import unittest
from index import *
from bs4 import BeautifulSoup as bs


class TestRetrieveFunctions(unittest.TestCase):
    
    def test_format_words(self):
        self.assertEqual(format_words(['baseball','or']),['basebal'])
        self.assertEqual(format_words(['or','of']),[])
        self.assertEqual(format_words([]),[])
        
    def test_parse(self):
        html = '<html><head></head><body></body></html>'
        html2 = '<html><head></head><body><p>text</p></body></html>'
        html3 = ''' <html>
  <head>
   <title>
    The Dormouse's story
   </title>
  </head>
  <body>
   <p class="title">
    <b>
     The Dormouse's story
    </b>
   </p>
   <p class="story">
    Once upon a time there were three little sisters; and their names were
    <a class="sister" href="http://example.com/elsie" id="link1">
     Elsie
    </a>
    ,
    <a class="sister" href="http://example.com/lacie" id="link2">
     Lacie
    </a>
    and
    <a class="sister" href="http://example.com/tillie" id="link2">
     Tillie
    </a>
    ; and they lived at the bottom of a well.
   </p>
   <p class="story">
    ...
   </p>
  </body>
 </html>
 '''
        self.assertEqual(parse(bs(html,'lxml')),[])
        self.assertEqual(parse(bs(html2,'lxml')),['text'])
        self.assertEqual(parse(bs(html3,'lxml')),[u'the',u'dormous',u'stori',u'the',u'dormous',u'stori',u'onc',u'upon',u'time',u'three',u'littl',u'sister',u'name',u'elsi',u'laci',u'tilli',u'live',u'bottom',u'well'])   
        
        
    def test_remove_junk(self):
        html = '<html><head><script></script></head><body></body></html>'
        self.assertEqual(remove_junk(bs(html,'lxml')),bs('<html><head></head><body></body></html>','lxml'))
        html2 = '<html><head><script></script></head><body><style> test </style></body></html>'
        self.assertEqual(remove_junk(bs(html2,'lxml')),bs('<html><head></head><body></body></html>','lxml'))
    
if __name__ == '__main__':
    unittest.main()