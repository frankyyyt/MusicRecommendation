#correctProgression.py

'''
Once key is discovered and song is transposed to 0 (C), remove some obviously
incorrect chords/transitions in the original progression using knowledge of computer science

Metrics for corrections:
1. First, use key quality (major or minor) to determine most common chords:
    - major: 0,7,5,9m,2m,3m,7m -- I,V,IV,vi,ii,iii,viio
'''

import itertools

major_expected = ['0','2m','4m','5','7','9m','11m']
minor_expected = ['0m','2m','3','5m','7m','8','10']

progression = []
with open('progression.txt') as f:
    progression = [ line.strip() for line in f.readlines() ]
    progression = [ line.split() for line in progression ]


'''
Format for file:
line 1: bpm   key_quality   original_key
line 2-end: chord   number_of_occurences
'''
metadata,progression = progression[0],progression[1:]
bpm,key_quality,key = metadata[0],metadata[1],metadata[2]
progression = [ [line[0], int(line[1])] for line in progression ]

print 'Key:',key
print 'Major or minor?',key_quality
print 'BPM:',bpm
expected_chords = []
if key_quality == 'maj':
    expected_chords = major_expected
elif key_quality == 'min':
    expected_chords = minor_expected

def first_pass(progression):
    new_progression = []
    for chord in progression:
        chord = chord[0]
        if chord in expected_chords:
            print '%s is expected' % (chord)
        else:
            print '%s is not expected' % (chord)

    return progression

def second_pass(progression):
    return progression


progression = first_pass(progression)
progression = second_pass(progression)
