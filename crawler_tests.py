from crawl import *
import unittest


class TestCrawler(unittest.TestCase):
    
    
    def test_parse_args(self):
        self.assertEqual(parse_args(['crawl.py','200','pages/','https://www.cnn.com/']),['200','pages/','https://www.cnn.com/'])
        with self.assertRaises(InvalidArgumentException):
            parse_args(['crawl.py','200','pages/'])
        
    def test_crawler_errors(self):
        with self.assertRaises(NumPageNotProvidedException):
            Crawler(None,'pages/','https://www.cnn.com/')
            
        with self.assertRaises(DestFolderNotProvidedException):
            Crawler(num=10,urls='https://www.cnn.com/')
            
        with self.assertRaises(UrlNotProvidedException):
            Crawler(num=10,directory='pages/')
        
        
if __name__ == '__main__':
    unittest.main()