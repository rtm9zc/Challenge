#a solution implementing a trie structure
#takes string to find network as command line arg
import sys

class Node(object):
    def __init__(self, parent, value, end=False):
        self.children = {}
        self.value = value
        self.parent = parent
        self.end = end
        self.inSoln = False #flag if we have used this word before in the solution

    def add(self, string):
        if len(string) == 0:
            self.end = True
            return
        else:
            char = string[0]
            if char in self.children:
                self.children[char].add(string[1:])
            else:
                n = Node(self, char)
                self.children[char] = n
                n.add(string[1:])

    def resetSoln(self): #wipes inSolns back to False for a new query
        self.inSoln = False
        for node in self.children:
            self.children[node].resetSoln()
    def buildString(self):
        if self.parent: #a child
            return self.parent.buildString() + self.value
        else: #root, has no parent
            return ''
    def setInSoln(self, string): #sets a string as in the soln, 
                                 #used for starting word
        if len(string) == 0:
            self.inSoln = True
            return
        else:
            if string[0] in self.children:
                self.children[string[0]].setInSoln(string[1:])
            else:
                return

def buildTrie(filename): #goes through each line of file, 
                         #adding to trie, returns root
    root = Node(None, None) #root has no parent or value for trie
    with open(filename, 'r') as f:
        for line in f:
            root.add(line[:-1])
    return root

def getNeighbors(node, string, off=False): #off is a flag indicating if the 
                                           #L-distance has been accounted for
    out = []
    if len(string) == 0: #if at end of string
        if off: #if off, check if end is valid and not in solution, build string
            if node.end and not node.inSoln:
                node.inSoln = True
                return [node.buildString()]
            else:
                return []
        else: #if not off, can still add a char
            for char in node.children:
                child = node.children[char]
                out.extend(getNeighbors(child, string, True))
            return out
    nextChar = string[0]
    if not off: #cases that add a char, delete a char, or go down wrong path
                #add one to the L-distance, can't be used if already off one
        #case 1: go down wrong path => add one to distance
        for char in node.children:
            child = node.children[char]
            if child.value is not nextChar:
                out.extend(getNeighbors(child, string[1:], True))
        #case 2: delete character => stay at same node
        out.extend(getNeighbors(node, string[1:], True))
        #case 3: add a character => go down any path, reuse string
        for char in node.children:
            child = node.children[char]
            out.extend(getNeighbors(child, string, True))
    if nextChar in node.children: #path for correct continuation
        out.extend(getNeighbors(node.children[nextChar], string[1:], off))
    return out

if __name__ == '__main__':
    if len(sys.argv) is not 2:
        print 'Please provide a single string as a command line argument!'
    root = buildTrie('randomlist.txt')
    root.setInSoln(sys.argv[1])
    nextlist = [sys.argv[1]] 
    outlist = []
    for i in range (0, 3): #0 => friends, 1 => friendsoffriends, 
                           #2 => friendsoffriendsoffriends
        templist = []
        for word in nextlist:
            templist.extend(getNeighbors(root, word))
        nextlist = templist
        outlist.extend(templist)
    print outlist
    root.resetSoln() #some cleanup, doesn't do anything here, but is nice! :)
