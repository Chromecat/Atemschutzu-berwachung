import pickle
import nltk
import functions

with open('Part_Of_Speech_Model/nltk_german_classifier_data.pickle', 'rb') as f:
    tagger = pickle.load(f)

Funkkonversation = open("conversation.txt", "r")
Funkkonversation = Funkkonversation.read()

sentence = nltk.sent_tokenize(Funkkonversation)  # satz seperation
sentence = [nltk.word_tokenize(sent) for sent in sentence]  # wort seperation
sentence = [tagger.tag(word) for word in sentence]  # tagging

# Tags durch Grammatik ersetzen
functions.replacetagtype("für|von", "NE", "NE", "X-FÜR", sentence)
functions.replacetagtwo("kommen", "\.", "X-KOMMEN", sentence)
functions.replacetag("trupp|Atemschutzüberwachung", "TRUPP", sentence)
functions.replacetag("Hier", "X-HIER", sentence)
functions.replacetag("Frage", "X-FRAGE", sentence)
functions.replacetagtype("Druck", "NE", "CARD", "DRUCK", sentence)
functions.replacetagtwo("Verstanden", "Ende", "X-ENDE", sentence)

print(sentence[0][0][0])

grammar = """
            EINHEIT: {<TRUPP><NE>?}
            Ansprechen: {<EINHEIT><NE>?<X-FÜR><EINHEIT><NE>?}
            Ende des Funkspruchs:  {<X-KOMMEN><\$.>}
            Antwort auf Anfrage: {<X-HIER><EINHEIT>}
            Frage: {<X-FRAGE><APPR>?<NN>?}
            Ende des Dialogs: {<X-ENDE><NN><\$.>}
            Druckangabe: {<DRUCK><CARD>?<CARD>?<CARD>?<CARD>}

          """

# funktion schreiben die die Antwort auf die Frage erkennt
print()

cp = nltk.RegexpParser(grammar)
for x in range(len(sentence)):
    result = cp.parse(sentence[x])
    # result.draw()
    test = list(result)
    print(test)
