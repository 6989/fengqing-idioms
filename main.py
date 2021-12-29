# 风情 FengQing: 成语接龙 game
# Kiara Liu
# Winter 2021

# TO DO:
# skip round/get help function
# fanti??
# modify dictionary to add terms (kinda difficult haha)
# maybe create a discord bot.... we'll see

import json
import random
from pypinyin import pinyin, lazy_pinyin, Style, load_phrases_dict

idiomsFile = open('chinese-xinhua-master/data/idiom.json', 'r')
idiomsData = idiomsFile.read()
idioms = json.loads(idiomsData)
load_phrases_dict({'乍暖还寒': [['zhà'], ['nuǎn'], ['huán'], ['hán']]})

def isKeyword(word):
    # Detects keywords from user.
    if word == 'exit':
        return 'exit'
    elif word == 'skip':
        return 'skip'
    else:
        return False

def isZh(word):
    # Detects if the user input is in Chinese.
    if isKeyword(word) != False:
        return isKeyword(word)
    else:
        for c in word:
            if c < u'\u4e00' or c > u'\u9FFF':
                return False
        return True

def promptForZh(word, lastSound):
    # Prompts for idioms until the user enters Chinese characters.
    while isZh(word) == False:
        print("Please enter an idiom in Chinese.")
        word = input("Enter an idiom that begins with '{}': ".format(lastSound))
    return word

def getSound(word, pos):
    # Gets the sound of character in a word: pos = 0 for the first sound and -1 for the last
    return lazy_pinyin(word)[pos]

def idiomDef(word):
    # Returns a formatted definition of a word or 'no definition found'.
    idiom = searchIdiom(word)
    if idiom == None:
        return "{word}（{pinyin}）：no definition found.".format(word=word, 
            pinyin=' '.join(lazy_pinyin(word, style=Style.TONE)))
    else:
        return "{word} （{pinyin}）：{explanation}".format(word=idiom["word"], 
                pinyin=' '.join(lazy_pinyin(idiom["word"], style=Style.TONE)), 
                explanation=idiom["explanation"])

def searchIdiom(word, lastSound = None):
    # Searches the dictionary for an idiom that meets the criteria. Returns the dictionary entry
    # (the idiom) if found and None if not found.
    for idiom in idioms:
        if idiom["word"] == word:
            return idiom
    return None

def validateIdiom(word, lastSound):
    # Validates that a word that the user inputs is in the dictionary. If not, user can choose 
    # whether or not to come up with a new word. Returns the user's word or None.
    if isKeyword(word) != False:
        return isKeyword(word)
    else: #if the user didn't enter 'exit' previously
        word = promptForZh(word, lastSound)
        idiom = searchIdiom(word, lastSound)
        while idiom == None:
                print(word + " was not found in the dictionary.")
                yn = input("Would you like to enter another word? (Y/N) ")
                if isKeyword(yn) != False:
                    return isKeyword(yn)
                elif yn == 'Y':
                    word = input("Enter an idiom that begins with '{}': ".format(lastSound))
                    if isKeyword(word) != False:
                        return isKeyword(word)
                    else:
                        word = promptForZh(word, lastSound)
                        idiom = searchIdiom(word, lastSound)
                elif yn == 'N':
                    idiom = word
                    return word
        return idiom['word']

def generateIdiom(word, history):
    # Computer generates new idiom from user input. Finds word with a first sound
    # that matches userWord's last sound. A history list is used to make sure there 
    # are no repeated words. Returns an idiom or None.
    if word == None:
        return random.choice(idioms)
    else:
        lastSound = getSound(word, -1)
        matchingIds = []
        for idiom in idioms:
            firstSound = lazy_pinyin(idiom["word"])[0]
            if firstSound == lastSound:
                matchingIds.append(idiom)
        random.shuffle(matchingIds) # so that the list is in a random order
        computerId = matchingIds.pop()
        while computerId["word"] in history: # if a word has already been played before
            if len(matchingIds) != 0: # pops random words until no more matching idioms
                random.shuffle(matchingIds)
                computerId = matchingIds.pop()
            else: # when there are no more matching idioms in the dictionary
                return None
        return computerId

def play():
    print("The game has started.")
    print("Enter 'exit' anytime to quit the game.")
    histList = []
    userWord = None
    computerId = None
    end = False
    while end == False:
        skip = False
        computerId = generateIdiom(userWord, histList) # computer generates an idiom
        if computerId == None: # in the rare case that there are no more idioms
            print('The dictionary has run out of matching idioms.')
            end = True
        else:
            histList.append(computerId["word"])
            lastSound = getSound(computerId["word"], -1)
            print()
            print("Computer:")
            print(idiomDef(computerId["word"]))
            print()
            userWord = input("Enter an idiom that begins with '{}': ".format(lastSound))
            while isZh(userWord) != True and end == False and skip == False:
                if isKeyword(userWord) == 'exit':
                    end = True
                elif isKeyword(userWord) == 'skip':
                    skip = True
                    userWord = computerId["word"]
                else:
                    print("Please enter an idiom in Chinese.")
                    userWord = input("Enter an idiom that begins with '{}': ".format(lastSound))
            if skip == False:
                userWord = validateIdiom(userWord, lastSound)
                if userWord == 'exit':
                    end = True
                elif userWord == 'skip':
                    userWord = computerId["word"]
                else:
                    print()
                    histList.append(userWord)
                    print("Player:")
                    print(idiomDef(userWord))
    print()
    print('The game has ended.')
    print('Idioms played in this game: ' + '、'.join(histList))

if __name__ == "__main__":
    play()
    print(generateIdiom('天官赐福', [])["word"])