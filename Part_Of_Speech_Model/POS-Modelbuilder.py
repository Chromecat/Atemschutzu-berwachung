import nltk
import random
from ClassifierBasedGermanTagger.ClassifierBasedGermanTagger import ClassifierBasedGermanTagger
import pickle
from datetime import datetime

# Anzeige der Zeit zum Überprüfen der Dauer
print(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

# Einlesen des Tiger Korpus
corp = nltk.corpus.reader.conll.ConllCorpusReader(
    '.', 'tiger_release_aug07.corrected.16012013.conll09',
    ['ignore', 'words', 'ignore', 'ignore', 'pos'], encoding='utf-8')

# Sätze mischen
tagged_sents = list(corp.tagged_sents())
random.shuffle(tagged_sents)

# Trainingsset definieren 10% für Test
split_perc = 0.1
split_size = int(len(tagged_sents) * split_perc)
train_sents, test_sents = tagged_sents[split_size:], tagged_sents[:split_size]

# Trainieren
tagger = ClassifierBasedGermanTagger(train=train_sents)

#Genauigkeit ausgeben
accuracy = tagger.evaluate(test_sents)
print(accuracy)

# Model abspeichern
with open('nltk_german_classifier_data.pickle', 'wb') as f:
    pickle.dump(tagger, f, protocol=2)

print(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
