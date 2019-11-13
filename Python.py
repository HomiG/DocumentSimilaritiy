import os
import math
from operator import attrgetter
from heapq import nlargest


#Ojcets of this class are used to tell what 2 documents are the most similar ones and what is the percentage of similarity. They store the index of the 2 compared files and the percentage of theor similarity
class  CompareStats:
    def __init__(self, doc1, doc2, cos):
        self.doc1=doc1
        self.doc2=doc2
        self.cos=cos #percentage of similarity

#Calculates the dotProduct.
def dotProduct(TwoDList, doc1, doc2): #D1 and D2 are actually integers that points out what row of the 2D list will be used for calculations, 0,1,2.. for the 1st,2nd,3rd.. document.
    dotResult=0
    for column in range(0, len(TwoDList[0])):
        dotResult = dotResult + TwoDList[doc1][column]*TwoDList[doc2][column]
    return dotResult

#Colculates the norms of 2 "files" and multiply them
def multipliedNorms(TwoDList, doc1, doc2):
    normD2=normD1=0
    for column in range(0, len(TwoDList[0])):
        normD1 = normD1 + TwoDList[doc1][column]*TwoDList[doc1][column]
        normD2 = normD2 + TwoDList[doc2][column]*TwoDList[doc2][column]
    return math.sqrt(normD1*normD2)

def cosFunc(TwoDList ,doc1, doc2):
    return dotProduct(TwoDList, doc1, doc2) / multipliedNorms(TwoDList, doc1, doc2)


fileList = [] # List that cointais locations of each file
fileListCounting = [] # List that cointais locations of each file
wordList = [] #list that contains each unique word

#open files
for filename in os.listdir(os.getcwd()):
    if filename.endswith('.txt'):
        fileList.append(open(filename))

#Create a list that includes the unique words of the files
for numberOfFiles, file in enumerate(fileList):
    for line in file:
        for word in line.replace('(', '').replace(')', '').replace(',', '').replace('.', '').replace('"', '').replace(':', '').replace(';', '').lower().split():    #I am ereasing every punctiation by replacing it with ''
            if word not in wordList:
                wordList.append(word)   #Add the word at the wordList which contains each UNIQUE word if this word doesn't exist in the list.

# This 2D list keeps count records for how many times each word appears in each file
#IMPORTANT NOTE! The Nth index of the row, represents the Nth file which was read from the project folder. So document0 is the first document that is read from the folder.. Documents 1 is the 2nd document htat is read from the folder and so on.
wordCounter = [[0 for i in range(len(wordList))] for j in range(numberOfFiles+1)]


#Reread the files
for filename in os.listdir(os.getcwd()):
    if filename.endswith('.txt'):
        fileListCounting.append(open(filename))

#That block of code increases the propper counts in the 2D list.
for idx, file in enumerate(fileListCounting):
    for line in file:
        for word in line.replace('(', '').replace(')', '').replace(',', '').replace('.', '').replace('"', '').replace(':', '').replace(';', '').lower().split():
            wordCounter[idx][wordList.index(word)] += 1 #Indrease the propper counter of the word.

k = int(input("TOP K MOST SIMILAR DOCUMENTS. How many?"))

#That block of codes generates the numbers that refer to the lines of the 2D array, which tells what documents to compare with one another.
#e.g. 0 with 1,2,3,4   1 with 2,3,4   2 with 3,4    3 with 4
start=0
comparedDocumentsList = []
for currentDocument in range(start, len(fileList)):
    for documentToCompareWith in range(currentDocument, len(fileList)):
        if currentDocument == documentToCompareWith:
            continue
        comparedDocumentsList.append(CompareStats(currentDocument, documentToCompareWith, cosFunc(wordCounter, currentDocument, documentToCompareWith))) #Calculate the similarity between the 2 files, and than create an oject that keeps the values of the number-ID of the 2 documents and the "Cos" similarity between them and pass it to the list.

largest = [] #List that saves the K largest objects. those objects keep info, what are the 2 documents and what is their percentage similarity.
largest = nlargest(int(k), comparedDocumentsList, key=attrgetter('cos')) #Find the K largest objects, comparing the cos attribute of the objects.

#print("Every single unique word in the txt files is:\n", wordList)

print("\n\n")
print("Most K =", k, "similar file pairs are:")
for i, counter in enumerate(largest[:k]):
    print("File:", largest[i].doc1, "and File: ", largest[i].doc2, "are similar by ", round(largest[i].cos*100, 2), "%")



