import sys
import re
import random

# An array of all different kinds of words
global wordType
# An array of all ngrams
global ngram
# A 2D array of frequencies
global freq



# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# getFreq1Given2
# Get the frequency of word 1 given word 2
def getFreq1Given2(word1,word2):
    return freq[search(ngram," "+word2.lower())][search(wordType,word1.lower())]



# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# sumRow
# Return the sum of all elements in an array
def sumRow(someList):
    total=0
    for i in someList:
        total+=i
    return total



# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# sub
# This method finds and replaces a string within a string
def sub(find, replace, line):
    line=re.sub(find,replace,line)
    return line



# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# search
# Search an array for a specific word. Return -1 if failed
def search(line,char):
    count=0
    for tokens in line:
        if tokens == char:
            return count
        count=count+1
    return -1
        


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# replaceSpecialCharacters
# Remove all special characters
def replaceSpecialCharacters(line):
    line=sub("“","",line)
    line=sub("”","",line)
    line=sub("‘","",line)
    line=sub("’","",line)
    line=sub("\"","",line)
    line=sub("\*","",line)
    line=sub("\^","",line)
    line=sub("\(","",line)
    line=sub("\)","",line)
    line=sub("\[","",line)
    line=sub("\]","",line)
    line=sub("\{","",line)
    line=sub("\}","",line)
    line=sub("\,","",line)
    line=sub("\:","",line)
    line=sub("\;","",line)
    line=sub("\'","",line)
    line=sub("…","",line)
    line=sub("💜","",line)
    line=sub("<","",line)
    line=sub(">","",line)
    line=sub("- ","",line)
    line=sub("/","",line)    
    return line



# # # # # # # # # # # # # # # #
# Read command line arguments #
# # # # # # # # # # # # # # # #
# n - number of grams
n=int(sys.argv[1])
# m - amount of characters to read in
m=int(sys.argv[2])
# files - .txt files to read
files=sys.argv[3:len(sys.argv)]

# megaWords is all input from files
megaWords=""

print("Reading file...")

# Read in file and add to megaWords
for tokens in files:
    file=open(tokens,'r',encoding = 'utf-8')
    megaWords=megaWords+file.read().lower()
    file.close()

count=0
startStopTokens=""

# Add <start> tokens to the beginning, depending on n
while count < n:
    startStopTokens=startStopTokens+ " <start> "
    count=count+1

print("Replacing special characters...")

megaWords=startStopTokens+replaceSpecialCharacters(megaWords)
startStopTokens=" <end> " + startStopTokens

# Replace puncutation
megaWords=sub("\.",startStopTokens,megaWords)
megaWords=sub("\!",startStopTokens,megaWords)
megaWords=sub("\?",startStopTokens,megaWords)

# Split megaWord by space into an array
megaWords=str.split(megaWords)

# Add one of each word used in the file to wordType
wordType=[]
ngram=[]
skip=0
i=n
ngramTotal=[]
freq=[[]]

print("Calculating ngrams...")

while i < len(megaWords):
    # Add one of each word used in the file to wordType
    #if search(wordType,megaWords[i])==-1:
    wordType.append(megaWords[i])
    previous=n
    previousGram=""

    while previous > 0:
        previousGram=previousGram+" "+megaWords[i-previous]
        previous=previous-1
    i=i+1

    location=search(ngram,previousGram)

    if location==-1:
        ngram.append(previousGram)
        ngramTotal.append(1)
    else:
        ngramTotal[location]+=1

print("Calculating matrix...")

rows,cols=(len(ngram),len(wordType))
freq=[[0 for i in range(cols)] for j in range(rows)]

i=n

print("Calculating frequency...")

while i < len(megaWords):
    previous=n
    previousGram=""
    while previous > 0:
        previousGram=previousGram+" "+megaWords[i-previous]
        previous=previous-1
    ngramLocation=search(ngram,previousGram)
    wordTypeLocation=search(wordType,megaWords[i])
    freq[ngramLocation][wordTypeLocation]=freq[ngramLocation][wordTypeLocation]+1/ngramTotal[ngramLocation]
    i+=1

i=0
j=0

#print("Calculating probability...")
#
#while i < len(freq):
#    while j < len(freq[0]):
#        freq[i][j]=freq[i][j]/ngramTotal[i]
#        j+=1
#    i+=1
#    j=0


numOfSentences=0
sentence=""
currentWord=[]

print("Generating sentences...")

while numOfSentences<m:

    beginningTokens=sub("<end>","",startStopTokens)
    for tokens in str.split(beginningTokens):
        currentWord.append(tokens)


    while currentWord[len(currentWord)-1] != "<end>":
        previous=n
        previousGram=""
        while previous > 0:
            previousGram=previousGram+" "+currentWord[len(currentWord)-previous]
            previous=previous-1
        

        i=search(ngram,previousGram)
        j=0
        total=0
        randy=random.random()
        go=1
        while go:
            if (total+freq[i][j]) <= randy:
                total+=freq[i][j]
                j+=1
            else:
                go=0
        currentWord.append(wordType[j])

    randomSentence=""
    for tokens in currentWord:
        if tokens != "<start>" and tokens != "<end>":
            randomSentence=randomSentence+" "+tokens

    randomSentence=randomSentence[1:len(randomSentence)]

    print(randomSentence)
    print()
    randomSentence=""
    currentWord=[]
    numOfSentences+=1