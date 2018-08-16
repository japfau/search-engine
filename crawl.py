# import all the modules we need
from collections import deque
from collections import defaultdict
import scrapy
import urllib2
import urlparse
import sys
import os
from lxml import html
import time
import cPickle as pickle


#===========
# Exceptions
#===========
class AlgoNotProvidedException(Exception):
    def handle(self):
        self.message

class AlgoNotSupportedException(Exception):
    def handle(self):
        self.message

class NumPageNotProvidedException(Exception):
    def handle(self):
        self.message

class DestFolderNotProvidedException(Exception):
    def handle(self):
        self.message

class UrlNotProvidedException(Exception):
    def handle(self):
        self.message
        
        
class InvalidArgumentException(Exception):
    def handle(self):
        self.message

#===========
# Containers
#===========
class Container(deque):
    ''' This is a class that serves as interface to the Spider '''
    def add_element(self, ele):
        ''' Add an element to the contain, always to the right '''
        return self.append(ele)

    def get_element(self):
        ''' This is an abstract method '''
        raise NotImplementedError

class Queue(Container):
    ''' Queue data structure implemented by deque '''
    def get_element(self):
        ''' Pop an element from the left '''
        return self.popleft()

class Crawler(object):
    '''
    A class that crawls web pages
    '''
    
    def __init__(self,num=None,directory=None,urls=None):
        '''
        constructor for a Crawler object, takes an int directory name and starting urls
        '''
        #check manditory inputs
        if num is None:
            raise NumPageNotProvidedException
        self.num_page_to_fetch = int(num)
        
        if directory is None:
            raise DestFolderNotProvidedException
        self.dest_folder = directory
        
        if urls is None:
            raise UrlNotProvidedException
        self.start_urls = urls.split(',')
        
        # set container to a Queue for bfs
        self.container = Queue()
        
        return
    
    def write_graph(self,web_graph):
        try:
            fo = open('graph.dat','wb')
            pickle.dump(web_graph,fo,2)
            fo.close()
        except IOError:
            print 'Could not save graph'
    
    
    def search(self):
        '''
        performs a breadth-first search from the starting urls
        
        None -> None
        '''
        graph = dict()
        neighbors = list()
        
        # add all starting urls to the container
        for url in self.start_urls:
            self.container.add_element(url)
        
        # make a set for visited sites and start count at 1
        visited = set()
        count = 1
        
        # iterate while the container has urls
        while self.container:
            current = self.container.get_element()
            print current
            visited.add(current)
      
            # break break when number of pages gotten is over given
            #number to fetch if crawler  hasn't stopped
            if count > self.num_page_to_fetch:
                self.write_graph(graph)
                break
            
            # print count to the console
            print count
            
            # try opening the url and getting its contents/links
            try:
                req = urllib2.Request(current)
                response = urllib2.urlopen(req)
                source = response.read()
                response.close()
                
                self.save_file(source, current, count)
                count += 1
                
                parse_string = html.fromstring(source)
                
                base = current
                
                
                for link in parse_string.xpath('//a/@href'):
                    #print link
                    
                    
                    if urlparse.urljoin(base,link) not in visited:
                        if link[-4:] != ".pdf" or link[-4:] != ".jpg" or link[-4:] != ".png" or link[-4:] != ".txt":
                            if link[:4] != 'http' or link[:5] != 'https':
                                self.container.add_element(urlparse.urljoin(base,link))
                                neighbors.append(urlparse.urljoin(base,link))
                            else:
                                self.container.add_element(link)
                                neighbors.append(link)
                    #print neighbors
                graph[current] = neighbors
                neighbors = list()
                                
            
            # catch the possible errors and print bad link with current url                    
            except urllib2.HTTPError:
                print "bad link: " + current
            except urllib2.URLError:
                print "bad link: " + current
                
            time.sleep(2)
                
                
    def save_file(self,contents, website, count):
        '''
        saves the name of the file and url of the file to index.dat
        also saves the contents of the url to a file
        
        str str int -> None 
        '''
        # make filename something like "0.html" or "1.html" etc 
        filename = str(count)+".html"                

        # get the full path to save file and full path for index.dat file
        fullpath = os.path.join(os.getcwd() +"/"+ self.dest_folder, filename)
        datfile = os.path.join(os.getcwd() +"/"+ self.dest_folder, "index.dat")

        # create the file if it doesn't exist
        if not os.path.exists(self.dest_folder):
            os.makedirs(self.dest_folder)
        # open the filename path and write its contents
        try:
            direct = open(fullpath,"w")                                             
            direct.write(contents)                                                    
            direct.close()

            # open the index.dat file and append info. 
            datopen = open(datfile, "a")
            datopen.write(filename + "\t" + website + "\n")
            datopen.close() 
        except IOError:
            raise IOError('Could not save file')
    


def parse_args(args):
    '''
    Parses the inputted arguments
    
    input : [list]
    output : [list]
    '''
    
    if len(args) < 4:
        raise InvalidArgumentException('Wrong number of arguments entered')
        
    else:
        return args[1:]



if __name__ == '__main__':
    '''
    run the crawler when this file is main file called
    '''
    args = parse_args(sys.argv)
        
    crawler = Crawler(args[0],args[1],args[2])
    crawler.search()
    
    
    
    
