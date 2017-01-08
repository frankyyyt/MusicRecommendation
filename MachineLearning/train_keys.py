from sklearn import datasets
from sklearn.multiclass import OneVsOneClassifier
from sklearn.svm import LinearSVC
import os
import numpy as np

chords = []
for i in range(12):
    chords.append(str(i))
    chords.append(str(i) + 'm')

chord2val = {}
for i, chord in enumerate(chords):
    chord2val[chord] = i

class Song:
    def __init__(self, filename):
        self.name = filename
        with open('Progressions/' + filename) as f:
            lines = f.readlines()
            for i, line in enumerate(lines):
                lines[i] = line.strip()
            self.key = lines[0]
            self.distribution = lines[1 : ]
            self.frequencies = dict()
            for i, data in enumerate(self.distribution):
                data = data.split(',')
                self.frequencies[data[0]] = data[2]

        self.all_frequencies = []
        for chord in chords:
            frequency = 0
            try:
                frequency = float(self.frequencies[chord])
            except KeyError:
                pass

            self.all_frequencies.append(frequency)

        self.all_frequencies = np.array(self.all_frequencies)

    def Frequencies(self):
        return self.all_frequencies

    def Key(self):
        return self.key


    def Print(self):
        print 'Filename:', self.name
        print 'Key:', self.key
        print 'Frequencies:'
        for i, chord in enumerate(chords):
            print chord, self.all_frequencies[i]


songs = []
for file in os.listdir('Progressions/'):
    if file != '.DS_Store':
        song = Song(file)
        songs.append(song)

X = []
y = []
for song in songs:
    X.append(song.Frequencies())
    y.append(song.Key())

X = np.array(X)
y = np.array(y)
classifier = OneVsOneClassifier(LinearSVC(random_state=0))
classifier.fit(X,y)
to_predict = [ X[1], X[2] ]
print classifier.predict(to_predict)
