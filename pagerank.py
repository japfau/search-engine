import sys
import cPickle as pickle

class InvalidArgumentsException(Exception):
    def handle(self):
        self.message


def read_graph(graph_file):
    ''' Opens the graph file and pickles it. This was used for testing purposes only '''
    try:
        fo = open(graph_file,'rb')
        graph = pickle.load(fo)
        fo.close()
        
    except IOError:
        raise IOError("graph file not found")
        
    return graph
        

def get_inlinks(graph):
    ''' Takes in a graph and stores each webpages inlinks in a dictionary '''
    inlinks_graph = {}
    
    for key in graph:
        inlinks_graph[key] = []
     
    for key in graph:
        for value in graph[key]:
            if value not in inlinks_graph:
                inlinks_graph[value] = [key]
            else:
                inlinks_graph[value].append(key)
                
    return inlinks_graph
        
'''
sigma portion of iteration algorithm:
    for current node:
        get all nodes that are inlinks to current node
            for each inlink node:
                get length of all outgoing links
                divide node's pagerank by number of outgoing links
            add all inlink node totals together
    new_pg_rank = (d / n) + (1 - d) * (all inlink node totals)
'''

def pagerank(graph):
    ''' Sets the initial page rank value for each webpage to 1/n. It then iterates
    until the program reaches the max number of iterations defined. While
    this is true, the loop will get the inlinks of each node, calculate the 
    outlink for the inlink nodes and divide by the pagerank for each inlink page.
    The new pagerank will then be calculated for the webpage, and the process
    will continue for each webpage, then iterate once all webpages have been updated. '''    

    pranks = dict()
    n = len(graph)
    d = 0.85
        
    for page in graph:
        pranks[page] = 1.0 / n
    
    total = 0
    inlinks = get_inlinks(graph)
    iterations = 1000   

    while iterations > 0:
   # for i in range(100):    
	for node in graph:
	    for link in inlinks.get(node):
	    	outlinks = len(graph.get(link))
	    	pr = pranks[link] / outlinks
	    	total += pr
    	    new_pg_rank = (d / n) + (1 - d) * total
   	    total = 0
    	    pranks[node] = new_pg_rank
        iterations -= 1
    return pranks


def args_is_valid(args):
    if len(args) != 2:
	raise InvalidArgumentsException("Invalid Arguments")
    return True


def main():

    if args_is_valid(sys.argv):
	graph = sys.argv[1:]
   
          
    #test_graph = {'0' : ['1','2'], '1' : ['2'], '2' : ['1'], '3' : ['2']} 
    #test_graph = {'1' : ['2','3'], '2' : ['3'], '3' : ['1'], '4' : ['3']}
    #nums = get_inlinks(test_graph)
    #print nums
    #print nums.values()
    #ind = nums.values().index(max(nums.values()))
    #print nums.values()[ind]
    pr = pagerank(graph)
    
    print pr

if __name__ ==  '__main__':

    main()
   

