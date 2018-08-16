'''
This file creates the inverted index and doc files that will be used for retrieval

We assume that the pages/ directory is in the same directory where this file is located.
It also assumes that index.dat file in also in the pages/ directory.

how to run:
    python index.py dir/ index_file
'''


# imports used

import sys
from nltk.corpus import stopwords
from bs4 import BeautifulSoup as bs
import os
from nltk import PorterStemmer
from re import sub
import collections
import urlparse
import cPickle as pickle

# class for handling invalid arguments given
class InvalidArgumentsException(Exception):
    '''
    class that handles wrong arguments passed
    '''
    def handle(self):
        self.message

# Contants used for filter words
STEMMER = PorterStemmer()
STOPWORDS = stopwords.words('english')


def format_words(ls):
    '''
    removes stopwords and stems the other words
        
    [list of words] -> [list of words]
    '''
    rest = [STEMMER.stem(word) for word in ls if word not in STOPWORDS]
    return rest


def parse(string):
    '''
    parses the contents of a string 
        
    str -> [list of words]
    '''
    #contents = string.get_text(' ')
    contents = sub(r'[^A-Za-z\s]','',string.get_text(' '))
    contents = [word.lower() for word in format_words(contents.strip().split())]    
    return contents


def remove_junk(contents):
    '''
    removes all the script and style contents from an html string
        
    str -> str
    '''
    #soup = contents
    for script in contents.find_all(['script','style','a']):
        script.extract()
        
    return contents

def read_mapping_file(index_file):
    '''
    reads in the index.dat file created from the webcrawler
    if applicable
        
    str -> {filename : url}
    '''
    indexes = {}
    try:
        fo = open(index_file,'r')
        for line in fo:
            (name,url) = line.split()
            indexes[name] = url
        fo.close()
    except IOError:
        print 'Could not find file'
    return indexes


def write_inv_index(invindex):
    '''
    writes a dictionary of an inverted index to a file
        
    {word : {filename : word_count}} -> None
    '''
    
    # try to open the file and then write the contents of the inverted index to a file 
    
    try:
        fo = open('invindex.dat','w')
        for word in invindex:
            fo.write('word : ' + word.encode('utf-8') + '\n')
            pairs = invindex.get(word)
            for item in pairs.items():
                fo.write(item[0]+" : "+str(item[1]) + "\n")
            fo.write("-"*20 + "\n")
        fo.close()
    except IOError:
        raise IOError('Could not write to invindex.dat')
            
    return True
 

def write_docs_file(contents,title,url):
    '''
    writes title, length, url of a file to docs.dat
        
    str, str, str -> None
    '''
    
    try:
        fo = open('docs.dat','a')
        fo.write('Title : ' + title.strip().encode('utf-8') + '\n')
        fo.write('Length : ' + str(len(contents)) + '\n')
        fo.write('URL : ' + url + '\n')
        fo.write('-' * 50 + '\n')
        fo.close()
    except IOError:
        raise IOError('could not append to docs.dat file')
            
    return True


def get_files(folder):
    '''
    returns a list of files in the given folder
        
    str -> [list of files]
    '''
    path = os.path.join(os.getcwd(),folder)
    files = os.listdir(path)
    
    for f in files:
        if sub(r'[^0-9]','',f) == '':
            files.remove(f)
    files = sorted(files,key=lambda x: int(sub(r'[^0-9]',"",x)))
    return files


def main():
    '''
    Main function that runs when this script is called.
    builds the invindex.dat and docs.dat file from the html files in the pages directory
    '''
    
    args = sys.argv
    
    final = collections.defaultdict(list)
    
    
    if (len(args) != 3):
        raise InvalidArgumentsException('Not corrent number of arguments')
        
    directory = args[1]
    index_file = args[2]
    
    files = get_files(directory)
    
    for fo in files:
    
        temp = collections.defaultdict(list)
        
        mapping_file = read_mapping_file(os.path.join(os.getcwd(),directory,index_file))
    
        current_file = os.path.join(os.getcwd(),directory,fo)
        
        filename = open(current_file,'r')
        source = filename.read()
        filename.close()
        soup = bs(source,'lxml')
        
        contents = remove_junk(soup)
        contents = parse(contents)
        title = soup.title.string
        
        for word in contents:
            if word not in temp:
                temp[word] = {fo : contents.count(word)}
                
        for item in temp:
            if item in final:
                final[item].update(temp[item])
            else:
                final[item] = temp[item]
                
        write_docs_file(contents,title,mapping_file[fo])
    write_inv_index(final)
    
    return True


if __name__ == '__main__':
    main()










