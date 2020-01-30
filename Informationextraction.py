import pickle
import nltk
import functions
import re
from termcolor import colored

# POS model laden
with open('Part_Of_Speech_Model/nltk_german_classifier_data.pickle', 'rb') as f:
    tagger = pickle.load(f)

# Konversation aus externer Datei laden
Funkkonversation = open("conversation.txt", "r")
Funkkonversation = Funkkonversation.read()

Timestamps = Funkkonversation.splitlines()
for x in range(len(Timestamps)):
    Timestamps[x] = re.findall("\[Time:\d+:\d+,\d+\]", Timestamps[x])
    # jeden Timestamp extrahieren um eine liste zu haben.
    # unten dann den jeweiligen Timestemp wieder aufgreifen  [Time:10:04,01]

Funkkonversation = re.sub("\[Time:\d+:\d+,\d+\]", "", Funkkonversation)

# NLTK operationen
sentence = nltk.sent_tokenize(Funkkonversation)  # satz seperation
sentence = [nltk.word_tokenize(sent) for sent in sentence]  # wort seperation
sentence = [tagger.tag(word) for word in sentence]  # tagging

# Tags durch Grammatik ersetzen
functions.replacetagtype("für|von", "NE", "NE", "X-VON", sentence)
functions.replacetagtwo("kommen", "\.", "X-KOMMEN", sentence)
functions.replacetag("trupp|Gruppenführer|Atemschutzüberwachung", "TRUPP", sentence)
functions.replacetag("Hier", "X-HIER", sentence)
functions.replacetag("Frage", "X-FRAGE", sentence)
functions.replacetagtype("Druck", "NE", "CARD", "DRUCK", sentence)
functions.replacetagtwo("Verstanden", "Ende", "X-ENDE", sentence)

#print(sentence[0][0][0])

grammar = """
            EINHEIT: {<TRUPP><NE>?}
            Ansprechen: {<EINHEIT><NE>?<X-FÜR><EINHEIT><NE>?}
            Ende des Funkspruchs:  {<X-KOMMEN><\$.>}
            Antwort auf Anfrage: {<X-HIER><EINHEIT>}
            Frage: {<X-FRAGE><APPR>?<NN>?}
            Ende des Dialogs: {<X-ENDE><NN><\$.>}
            Druckangabe: {<DRUCK><CARD>?<CARD>?<CARD>?<CARD>?}

          """

grammar_parser = nltk.RegexpParser(grammar)

Einheit1 = ""
Einheit2 = ""

# Schleife über alle Sätze
for x in range(len(sentence)):

    # Text wieder zusammenfügen
    Text = ''
    for words in range(len(sentence[x])):
        Text += str(sentence[x][words][0]) + " "

    # Grammatik anwenden
    sentence_grammar = grammar_parser.parse(sentence[x])

    print()
    if re.findall("EINHEIT", str(sentence_grammar)):
        if re.findall("X-VON", str(sentence_grammar)):
            try:
                Einheit1 = ("Einheit1: " + str(sentence_grammar[0][0][0]) + " " + str(sentence_grammar[0][1][0]))
            except IndexError:
                Einheit1 = ("Einheit1: " + str(sentence_grammar[0][0][0]))
            try:
                Einheit2 = ("Einheit2: " + str(sentence_grammar[2][0][0]) + " " + str(sentence_grammar[2][1][0]))
            except IndexError:
                Einheit2 = ("Einheit2: " + str(sentence_grammar[2][0][0]))

    if re.findall("DRUCK", str(sentence_grammar)):
        Druck = ("Druck: " + str(re.findall("[0-9]+", str(sentence_grammar))))
    else: Druck = ""

    #print(Timestamps[x][0] + " " + Einheit1 + " " + Einheit2 + " " + Druck + " " + Text)
    print(colored(Timestamps[x][0], 'yellow'), colored(" " + Einheit1, 'cyan'), colored(" " + Einheit2, 'magenta'), colored(" " + Druck, 'red'),
          colored(" " + Text, 'white'))
