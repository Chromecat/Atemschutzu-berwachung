import re


def replacetag(word, tag, sentence):
    for x in range(len(sentence)):
        for y in range(len(sentence[x])):
            if re.search(word, sentence[x][y][0]):
                temp = list(sentence[x][y])
                temp[1] = tag
                sentence[x][y] = tuple(temp)


def replacetagtwo(word1, word2, tag, sentence):
    for x in range(len(sentence)):
        for y in range(len(sentence[x])):
            if re.search(word1, sentence[x][y][0]) and re.search(word2, sentence[x][y+1][0]):
                temp = list(sentence[x][y])
                temp[1] = tag
                sentence[x][y] = tuple(temp)


def replacetagtype(word1, word2, word3, tag, sentence):
    for x in range(len(sentence)):
        for y in range(len(sentence[x])):
            if re.search(word1, sentence[x][y][0]) \
                    and re.search(word2, sentence[x][y-1][1]) \
                    and re.search(word3, sentence[x][y+1][1]):
                temp = list(sentence[x][y])
                temp[1] = tag
                sentence[x][y] = tuple(temp)
