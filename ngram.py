# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# ngram
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Jackson Hambridge
#
# This program will read in .txt files, as many as it is given, and use them to train a random
# sentence generator.  Based on the probability of ngrams in the input data, sentences are
# created and outputted.  The ngram is a 'phrase' of words, and can be selected by the user.
# For example, in the sentence "My name is Jackson." the bigrams are "my name" "name is" "is Jackson"
# and for each bigram, such as "my name" there is 100% chance of "is" being the next word.
# For the sentence "My name is Jackson and his name is Jackson." there is 100% chance of "Jackson"
# occurring after "name is" and a 50% chance of "and" or "." appearing after "is Jackson"
#
# Inputted data is stored in a 'history' dictionary which stores dictionaries of 'frequencies'.
# From there, sentences are randomly generated with the random.choices() method.
#
# Input: ngramSize numOfSentences files
# 
# Example Input: 2 1 "Purple Guy.txt"
# Example Output: Sean asked questions things that happened.
#
# Example Input: 3 3 "Purple Guy.txt" "The Neighbor.txt"
# Example Output: Ashley grimaced at the sight of the bells on the way sean found it difficult to clean his room and watch tv.
#                 Why.
#                 For sure sean says trying to think twice. 

import sys
import re
import random



# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# sub
# This method finds and replaces a string within a string
def sub(find, replace, line):
    line=re.sub(find,replace,line)
    return line



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
    line=sub("-"," ",line)
    line=sub("—"," ",line)
    line=sub("/","",line)
    line=sub("\\ufeff","",line)
    line=sub("_","",line)
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

print("This program will generate random sentences based on the way words appear sequentially in the input file(s).")
print()
print("ngram.py arguments")
print("ngram size: " + str(n))
print("Number of sentences: " + str(m))
print("Files: " + str(files))
print()

# megaWords is all input from files
megaWords=""

# Read in file and add to megaWords
for tokens in files:
    file=open(tokens,'r',encoding = 'utf-8')
    megaWords=megaWords+file.read().lower()
    file.close()

count=0
startStopTokens=""

# Add <start> tokens to the beginning, depending on n
while count < n-1:
    startStopTokens=startStopTokens+ " <start>"
    count=count+1

megaWords=startStopTokens+" "+replaceSpecialCharacters(megaWords)
startStopTokens=" <end>" + startStopTokens + " "

# Replace puncutation
megaWords=sub("\.",startStopTokens,megaWords)
megaWords=sub("\!",startStopTokens,megaWords)
megaWords=sub("\?",startStopTokens,megaWords)

# Split megaWord by space into an array
megaWords=str.split(megaWords)

# Add one of each word used in the file to wordType
i=n-1

# Prepare size dictionary (# of times an ngram is used)
ngramSizeDictionary={

}

# Prepare ngram dictionary (ngram:wordFrequency)
ngramDictionary={

}

# Loop through all input
while i < len(megaWords):
    # Add one of each word used in the file to wordType
    #if search(wordType,megaWords[i])==-1:
    currentWord=megaWords[i]
    previous=n-1
    history=""        

    # Calculate ngram (history)
    while previous > 0:
        history=history+" "+megaWords[i-previous]
        previous=previous-1
    i=i+1

    # If ngram is not already dictionary, add a word frequency of 1
    if history not in ngramDictionary:
        wordDict={
            currentWord: 1
        }
        ngramDictionary[history]=wordDict
        ngramSizeDictionary[history]=1
    # If ngram is in dictionary but word is not in frequency, add a word frequency of 1
    elif currentWord not in ngramDictionary[history]:
        ngramDictionary[history][currentWord]=1
        ngramSizeDictionary[history]+=1
    # Otherwise, increment frequency
    else:
        ngramDictionary[history][currentWord]+=1
        ngramSizeDictionary[history]+=1



# Prepare variables
numOfSentences=0
sentence=""
currentWord=[]

ngramFrequencyArray=[]
ngramNameArray=[]

# Store ngramFrequency and ngramNames as arrays
for tokens in ngramSizeDictionary:
    ngramFrequencyArray.append(ngramSizeDictionary[tokens])
    ngramNameArray.append(tokens)

# Generate m sentences
while numOfSentences<m:

    # Calculate starting token
    currentNGram=sub("<end>","",startStopTokens)

    sentence=str.split(currentNGram)

    while "<end>" not in sentence:
        previous=n-1
        history=""
        while previous > 0:
            history=history+" "+sentence[len(sentence)-previous]
            previous=previous-1

        frequencyArray=[]
        wordArray=[]
        # If unigram, calculate a random word from the history

        for tokens in ngramDictionary[history]:
            wordArray.append(tokens)
            frequencyArray.append(ngramDictionary[history][tokens])
        nextWord=random.choices(wordArray,frequencyArray)[0]

        sentence.append(nextWord)


    # Turn the sentence array into a randomSentence string
    randomSentence=""
    for tokens in sentence:
        if tokens != "<start>" and tokens != "<end>":
            randomSentence=randomSentence+" "+tokens

    randomSentence=randomSentence[1:len(randomSentence)]

    # Print random sentences
    print(randomSentence.capitalize()+".")
    print()

    # Reset variables
    randomSentence=""
    currentWord=[]

    # Increment count
    numOfSentences+=1