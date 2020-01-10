import heapq
import pathlib
from collections import Counter, namedtuple

class Node(namedtuple("Node", ["left", "right"])):
    #Class for the nodes of the character tree
    def walk(self, codeDictionary, acc): # Walks through the tree
        self.left.walk(codeDictionary, acc+"0")
        self.right.walk(codeDictionary, acc+"1")

class Leaf(namedtuple("Leaf", ["character"])):
    # Class for the leaves in the character tree
    def walk(self, codeDictionary, acc): #Walks through the tree
        codeDictionary[self.character] = acc or "0"

def code_building_module(charFreqs):
    #Returns a Huffman code for each character
    heap = []

    for character, frequency in charFreqs.items():
        heap.append((frequency, len(heap), Leaf(character)))

    heapq.heapify(heap)

    totalCount = len(heap)

    while len(heap) > 1: 
        frequency1, _totalCount, left = heapq.heappop(heap)
        frequency2, _totalCount, right = heapq.heappop(heap)

        heapq.heappush(heap,(frequency1+frequency2, totalCount, Node(left, right)))
        totalCount += 1

    codeDictionary = {}

    if heap:
        [(_frequency, _totalCount, root)] = heap
        root.walk(codeDictionary,"")

    return codeDictionary

def write_codes(textFile):
    # Loads in the text file and builds the code dictionary.
    snIn = open(textFile,"r")
    collection = snIn.read()
    snIn.close()
    frequency = Counter(collection) #Finds the frequency of each charactter
    # Add all zero frequencies
    for i in range(32,127):
        val = frequency.get(chr(i))
        if not val:
            frequency[chr(i)] = 0

    file = open("codeDictionary.txt","w")
    codeDictionary = code_building_module(frequency)
    print ()
    for key, val in codeDictionary.items():
        file.write(str(ord(key))+" "+str(val) + "\n")
    file.close()

def decode(code):
    # Takes in the code dictionary and decodes the text file.
    while True:
        encodedFile = input("Please enter the file you'd like to decode:")
        checkFile = pathlib.Path(encodedFile) # Checking if the file exists.
        if checkFile.exists ():
            break
        else:
            print (encodedFile+" doesn't exist. Please try again.")

    snIn = open(encodedFile,"r")
    content = snIn.read()
    snIn.close()
    decodedFileName = encodedFile.replace("_encoded.txt","_decoded.txt")

    pointer = 0
    decoded_text = ""
    while pointer < len(content):
        for ch in code.keys():
            if content.startswith(code[ch], pointer):
                decoded_text += ch
                pointer += len(code[ch])

    decodedFile = open(decodedFileName,"w")
    decodedFile.writelines(decoded_text)
    decodedFile.close()
    print ("Successfully decoded "+str(encodedFile)+" and stored it in " +decodedFileName)
    print ()

def encode(code):
    #Takes in the code dictionary and uses it to encode a text file that the user provides
    while True:
        file = input("Please enter the file you'd like to encode:")
        checkFile = pathlib.Path(file)
        if checkFile.exists ():
            break
        else:
            print (file+" doesn't exist. Please try again.")
    snIn = open(file, "r")
    content = snIn.read()
    snIn.close()
    encodedText = "".join(code[ch] for ch in content)
    encodedFileName = file.replace(".txt","_encoded.txt")
    encodedFile = open(encodedFileName,"w")
    encodedFile.write(encodedText)
    encodedFile.close()
    print ("Successfully encoded "+str(file)+" and stored it in "+str(encodedFileName))
    print ()

def main():
    write_codes("words1ASCII.txt") # Writes codes to text file

    file = open("codeDictionary.txt","r") # Reads the text
    code = {}
    for line in file:
        key, value = line.split()
        code[chr(int(key))] = value
    file.close()
    print ("Welcome to Huffman's Compression Software")
    while True:
        print ("Menu:")
        print ("1. Encode")
        print ("2. Decode")
        print ("3. Close Program")
        print ("")
        option = str(input("Please select a menu option: "))

        if option == "1":
            print ()
            encode(code)

        elif option == "2":
            print ()
            decode(code)

        elif option == "3":
            print ("Closing Program!")
            break

        else:
            print ("Incorrect menu option, please try again.")

main()
