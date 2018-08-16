'''
This file's purpose is to get the tf-idf scores of the pages that were built with the index.py script

It assumes that the files docs.dat, invindex.dat are in the same directory as this file.

how to run :
    python retrieve2.py word1 ... wordn
'''


# imports used

import math
import os
import sys
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from re import sub
from collections import deque
from collections import OrderedDict


# constants so they don't have to be created every time they are used in a function
STOPWORDS = set([s.lower() for s in stopwords.words('english')])
STEMMER = PorterStemmer()



class InvalidArgumentException(Exception):
    '''
    class that handles Invalid Arguments passed
    '''
    def handle(self):
        self.message


def args_is_valid(args):
    '''
    Checks whether the arguments passed are valid
    
    input : [list of words]
    output : [list of words]
    '''
    
    # return false right away if no args passed
    if args is None:
        return False
    
    # check that all words in args do not contain something other than a letter
    for token in args:
        if token != sub(r'[0-9]','',token):
            return False
    return True
    
    
def parse_args(args):
    '''
    Parses the arguments passed
    output : a list of words
    '''

    if (len(args)<2):
        #print 'Not enough arguments'
        raise InvalidArgumentException('Invalid arguments')
    output = args[1:]
    return output
            
            
def mode_most(words,d):
    '''
    Calculates the files with most of the tokens in words and its filename and count
    words: a list of strings
    d : a dictionary of {word : {filename : count}}
        
    return value : a dictionary of {word : {filename : count}}
    '''
            
    ls = list()
        
    store = dict()
    most = math.ceil(float(len(words))/2)
            
    for token in words:
        for pair in d[token].items():
            if token not in store:
                store[token] = {pair[0]:pair[1]}
                ls.append(pair[0])
            else:
                store[token].update({pair[0]:pair[1]})
                ls.append(pair[0])
   
    # keep the files that appeard >= to most
    sets = set([item for item in ls if ls.count(item) >= most])
    final = dict()

    # loop throught he words again and only keep the files that appeared more than most in the new dictionary
    for token in words:
        for pair in store[token].items():
            if token not in final:
                if pair[0] in sets:
                    final[token] = {pair[0]:pair[1]}
            else:
                if pair[0] in sets:
                    final[token].update({pair[0]:pair[1]})
            
    return final
            
            
def tf_score(docs,most_words):
    '''
    Gets the term frequency of word in every document it appeared it
    docs : a list of lists containing the Title,Length,Url of an html file
    most_words : a dict with {word: {file:count}...}
    return value : a dict of {word: {file:term_frequency}}
    '''
    for word in most_words:
        for fo in most_words[word]:
            most_words[word][fo] = float(float(most_words[word][fo])/float(docs[int(sub(r'[^0-9]',"",fo))-1][1]))
    return most_words


#Calculates the idf score by taking the total number of documents
#and most_words. For each word, the function calculates the number
#of documents that contain said word, and the total number of documents.
#It then divides them to obtain the idf score for that word's webpage
#and puts it in a new dictionary called idfs.

def idf_score(num_docs,most_words):
    '''
    Calculates the IDF score for each word
    num_docs: total number of documents in collection
    most_words: {word: {file:count} ...}
    return value : a dict of {word : IDF_score} where IDF score is a decimal value
    '''
    idfs = dict()
    for word in most_words:
        idfs[word] = math.log(float(num_docs)/float(len(most_words[word])))
   
    return idfs

#Takes the tfs and idfs dictionary and calculates the TFIDF score. 
#Takes each word in the tfs and then each webpage in tfs, checks
#to see if it has been calculated, and if not, takes the tf and 
#idf for each webpage and calculates the TFIDF score which is
#then saved to a dictionary, tf_idf score.

def tf_idf_score(tfs,idfs):
    '''
    Calculates the TF-IDF score for each document
    tfs : a dictionary of dictionary {word: {file:tf_score}...}
    idfs : a dictionary of {word: IDF_score}
    return value: {filename: TF-IDF_score,...}
    '''
    
    tf_idf = dict()

    for word in tfs:
        for fo in tfs[word]:
            if fo not in tf_idf:
                tf_idf[fo] = tfs[word][fo]*idfs[word]
            else:
                tf_idf[fo] += tfs[word][fo]*idfs[word]

    return tf_idf



#Sorts the TFIDF scores by the top 25 web pages then formats the
#output to "title, url, TFIDF score".

def display_results(docs_list,scores):
    '''
    Prints the title,URL and TF-IDF score of every page that had most of the given words
    docs_list: list of lists of [[Title,Length,Url],...]
    scores: a dictionary of {filename:TF-IDF_score}
    return value: void
    '''
            
    sorted_pages = sorted(scores.items(),key = lambda x : x[1],reverse=True)
    if len(sorted_pages) > 25:
        sorted_pages = sorted_pages[:25]

    print 'Pages ranked on TF-IDF scores'
    print '{0:70} {1:55} {2}'.format('Title','URL','Score')
    print "-"*150
    for fname in sorted_pages:
        position = docs_list[int(sub(r'[^0-9]',"",fname[0]))-1]
        print "{title:70} {url:55} {score}".format(title=position[0],url=position[2],score=fname[1])
            

#Creates the inverted index file
def make_invindex():
    '''
    Reads in the inverted index file invindex.dat
    return value: a dictionary of {word: {filename:word_count},...}
    '''
    
    last_word = ""
    invindex = OrderedDict()
    try:
        fo = open('invindex.dat','r')
        for line in fo:
            current = line.strip().split()
            if current[0] == 'word':
                invindex[current[2]] = {}
                last_word = current[2]
            elif 'html' in current[0]:
                page = current[0]
                count = int(current[2])
                new = {page:count}
                invindex[last_word].update(new)
        fo.close()

    except IOError:
        raise IOError("Could not find invindex.dat file")

    return invindex


#opens docs.dat and pulls the title, url, and length
def get_doc_file():
    '''
    Reads in the docs.dat file
    return value: a list of lists [[Title,Length,URL],...]
    '''
    pairs = deque()
    tu = ""
    try:
        fo = open('docs.dat','r')
        lines = fo.readlines()
        lines = [line for line in lines if line[:5] == 'Title' or line[:3] == 'URL' or line[:6] == 'Length']
        for i in xrange(0, len(lines), 3):
            title = lines[i].strip().split(" : ")
            length = lines[i+1].strip().split(" : ")
            url = lines[i+2].strip().split(" : ")
            pairs.append([title[1],length[1],url[1]])
        fo.close()

    except IOError:
        print "Could not find docs.dat file"

    return pairs


def main():
    '''
    Main function that runs above code
    '''
    args = parse_args(sys.argv)
       
    if  not args_is_valid(args):
        print 'Usage: python retrieve2.py word1 word2 ... wordn'
        print 'words must not contain numbers'
        return 

    index_map = make_invindex()                                # variable to hold the inverted index dictionary
    tokens = args                                     # variable to hold all the inputted words
    tokens = [STEMMER.stem(word.lower()) for word in tokens if word not in STOPWORDS and STEMMER.stem(word) in index_map]   # stems and lowers each word in arguments
    mosts = mode_most(tokens,index_map)                        # calls mode_most on inputted arguments and the inverted index 
    docs = get_doc_file()                                      # gets the docs.dat file
    total_files = len(docs)                                    # total number of files in our set
    tf_scores = tf_score(docs,mosts)                           # gets the term frequency score for each every file that matched to a word
    idfs = idf_score(total_files,mosts)                        # gets the IDF score for each word that matched
    tf_idf = tf_idf_score(tf_scores,idfs)                      # computes the full TF-IDF score with given tf and idf scores
    display_results(docs,tf_idf)                               # displays the files in order of highest tf-idf score to lowest

    
    
def main_search(*args):
    '''
    main function that was created to be used in the cgi page
    '''
    #args = parse_args()
    args = args
    if not args_is_valid(args):
        print 'Usage: python retrieve2.py word1 word2 ... wordn'
        print 'words must not contain numbers'
        return 

    index_map = make_invindex()                                # variable to hold the inverted index dictionary
    tokens = parse_args(args)                                    # variable to hold all the inputted words
    tokens = [STEMMER.stem(word.lower()) for word in tokens if word not in STOPWORDS and STEMMER.stem(word) in index_map]   # stems and lowers each word in arguments
    mosts = mode_most(tokens,index_map)                        # calls mode_most on inputted arguments and the inverted index 
    docs = get_doc_file()                                      # gets the docs.dat file
    total_files = len(docs)                                    # total number of files in our set
    tf_scores = tf_score(docs,mosts)                           # gets the term frequency score for each every file that matched to a word
    idfs = idf_score(total_files,mosts)                        # gets the IDF score for each word that matched
    tf_idf = tf_idf_score(tf_scores,idfs)                      # computes the full TF-IDF score with given tf and idf scores
    #display_results(docs,tf_idf)                               # displays the files in order of highest tf-idf score to lowest
    return tf_idf




# call the main function when ran
if __name__ == '__main__': 
    main()

