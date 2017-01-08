#compare.py
#module for finding distance between 2 chord progressions
'''
def GetConditionalProbabilities(progression, k):
    probs = { }
    current = 0
    while current < len(progression) - k:
        alreadySeen = tuple(p1[current : current + k])
        nextChord = p1[current + k]
        try:
            probs[alreadySeen]
        except KeyError:
            probs[alreadySeen] = {}
            probs[alreadySeen]['total'] = 0

        #    probs[alreadySeen][-1] = 0

        condProbs = probs[alreadySeen]

        try:
            condProbs[nextChord] += 1
        except KeyError:
            condProbs[nextChord] = 1
        condProbs['total'] += 1
        current += 1

    #convert counts to probability
    for alreadySeen in probs:
        probStr = alreadySeen.__str__() + '\n  '
        for nextChord in probs[alreadySeen]:
            if nextChord == 'total':
                continue
            probs[alreadySeen][nextChord] /= float(probs[alreadySeen]['total'])
    return probs

def #printCondProbs(probs):
    for alreadySeen in probs:
        probStr = alreadySeen.__str__() + '\n  '
        for nextChord in probs[alreadySeen]:
            if nextChord == 'total':
                continue
            probStr += str(nextChord) + ' : ' + str(probs[alreadySeen][nextChord])
            probStr += '\n  '
        #print probStr
condProbs1 = GetConditionalProbabilities(p1, 4)
#print 'Progressions 1: '
#printCondProbs(condProbs1)
condProbs2 = GetConditionalProbabilities(p2, 4)
#print 'Progression 2: '
#printCondProbs(condProbs2)
'''

def GetSubProgressions(progression, subLength):
    subprogressions = dict()
    current = 0
    while current <= len(progression) - subLength:
        subprogression = tuple(progression[current : current + subLength])
        try:
            subprogressions[subprogression] += 1
        except KeyError:
            subprogressions[subprogression] = 1
        current += 1

    return subprogressions

def GetCommonIndices(progression, common, subLength):
    commonIndices = set()
    current = 0
    while current <= len(progression) - subLength:
        subprogression = tuple(progression[current : current + subLength])
        if subprogression in common:
            commonIndices.update(tuple(range(current, current + subLength, 1)))
        current += 1
    return commonIndices

def EditDistance(X,Y):
    n = len(X)
    m = len(Y)

    # Create a table to store results of subproblems
    dp = [[0 for x in range(m+1)] for x in range(n+1)]

    # Fill d[][] in bottom up manner
    for i in range(n+1):
        for j in range(m+1):
            # If first string is empty, only option is to
            # isnert all characters of second string
            if i == 0:
                dp[i][j] = j    # Min. operations = j

            # If second string is empty, only option is to
            # remove all characters of second string
            elif j == 0:
                dp[i][j] = i    # Min. operations = i

            # If last characters are same, ignore last char
            # and recur for remaining string
            elif X[i-1] == Y[j-1]:
                dp[i][j] = dp[i-1][j-1]

            # If last character are different, consider all
            # possibilities and find minimum
            else:
                dp[i][j] = 1 + min(dp[i][j-1],        # Insert
                                 dp[i-1][j],        # Remove
                                 dp[i-1][j-1])      # Replace

    return dp[n][m], dp

def printDistances(distances, sub1Dist, sub2Dist):
    for d in sorted(distances):
        print 'Edit Distance',d
        for pair in distances[d]:
            print '  s1: ',pair[0], sub1Dist[pair[0]]
            print '  s2: ',pair[1], sub2Dist[pair[1]]

def RemoveEmpty(d):
    new_dict = dict()
    for elem in d:
        if d[elem]:
            new_dict[elem] = d[elem]
    return new_dict

def CompareSongs(song1, song2, subLength):
    p1 = []
    p2 = []
    #print song1,song2
    with open(song1) as f:
        p1 = [ elem.strip() for elem in f.readlines() ]
    with open(song2) as f:
        p2 = [ elem.strip() for elem in f.readlines() ]

    #normalize subprogression length
    if subLength > len(p1) or subLength > len(p2):
        subLength = min(len(p1), len(p2))
    if subLength < 1:
        subLength = 1

    #print 'Checking common subprogressions of length', subLength

    #subprogressions of length subLength from song1 : frequencies of those subprogressions
    sub1Dist = GetSubProgressions(p1, subLength)
    sub2Dist = GetSubProgressions(p2, subLength)

    sub1 = { sub for sub in sub1Dist }
    sub2 = { sub for sub in sub2Dist }

    distances1 = dict()
    distances2 = dict()

    #compute edit distances between all pairs of subprogessions, p1 vs p2
    for s1 in sub1Dist:
        for s2 in sub2Dist:
            d,table = EditDistance(list(s1),list(s2))
            try:
                distances1[d].append((s1,s2))
                distances2[d].append((s2,s1))
            except KeyError:
                distances1[d] = [(s1,s2)]
                distances2[d] = [(s2,s1)]

    #Fill in distances between 0 and max that were not represented
    for d in range(max(distances1)):
        try:
            distances1[d]
        except KeyError:
            distances1[d] = []
            distances2[d] = []

    '''
    For each subprogression that is common in more than 1 edit distance, only keep
    in lowest distance
    '''
    for d in sorted(distances1):
        for d2 in range(d+1,max(distances1)+1):
            firsts1 = [ pair[0] for pair in distances1[d] ]
            firsts2 = [ pair[0] for pair in distances2[d] ]
            distances1[d2] = [ pair for pair in distances1[d2] if pair[0] not in firsts1 ]
            distances2[d2] = [ pair for pair in distances2[d2] if pair[0] not in firsts2 ]

    #Check to make sure same subprogressions in distance d are removed from all d2 > d
    for d in distances1:
        for d2 in range(d+1,max(distances1) + 1):
            setD = set([pair[0] for pair in distances1[d]])
            setD2 = set([pair[0] for pair in distances1[d2]])
            intersection = setD.intersection(setD2)
            if intersection:
                print 'Subprogression is in distances %d and %d. Must Fix.' % (d,d2)

    #If no pair of subprogressions has certain distance, remove from dictionary
    distances1 = RemoveEmpty(distances1)
    distances2 = RemoveEmpty(distances2)


    #print 'Max Distance: ',subLength
    #print 'Distances1'
    #printDistances(distances1, sub1Dist, sub2Dist)
    #print
    #print 'Distances2'
    #printDistances(distances2,sub2Dist,sub1Dist)
    #print

    common1 = dict()
    seen = set()
    for d in distances1:
        subprogressions = [ pair[0] for pair in distances1[d] ]
        common = list(GetCommonIndices(p1, subprogressions, subLength))
        common1[d] = [ index for index in common if index not in seen ]
        seen.update(common1[d])

    common2 = dict()
    seen = set()
    for d in distances2:
        subprogressions = [ pair[0] for pair in distances2[d] ]
        common = list(GetCommonIndices(p2,subprogressions, subLength))
        common2[d] = [ index for index in common if index not in seen ]
        seen.update(common2[d])


    common1 = RemoveEmpty(common1)
    common2 = RemoveEmpty(common2)

    #print 'p1,distances1 Common'
    #for d in common1:
        #print d,common1[d]

    #print 'p2,distances2 Common'
    #for d in common2:
        #print d,common2[d]

    progression1Distance = 0
    progression2Distance = 0

    for d in common1:
        progression1Distance += d * len(common1[d])

    for d in common2:
        progression2Distance += d * len(common2[d])

    distance1 = round(1.0 * progression1Distance / (len(p1) * min(len(p1),len(p2))),5)
    distance2 = round(1.0 * progression2Distance / (len(p2) * min(len(p1),len(p2))),5)
    #print 'Distance1:',progression1Distance,distance1
    #print 'Distance2:',progression2Distance,distance2

    return (distance1 + distance2) / 2

'''
common = sub1.intersection(sub2)

#print 'Number of subprogressions in common:',len(common)
for sub in common:
    #print sub, 'count in progression 1:', sub1Dist[sub]
    #print sub, 'count in progression 2:', sub2Dist[sub]
    #print

difference = sub1.symmetric_difference(sub2)

unique1 = sub1.intersection(difference)
unique2 = sub2.intersection(difference)

#print 'Number of distinct subprogressions:',len(difference)
#print 'Distinct in progressions 1:', len(unique1)
for sub in unique1:
    #print sub,':',sub1Dist[sub]
#print 'Distinct in progressions 2:', len(unique2)
for sub in unique2:
    #print sub,':',sub2Dist[sub]

#print

commonIndices1 = GetCommonIndices(p1, common)
#print
commonIndices2 = GetCommonIndices(p2, common)
#print 'Common indices 1:', commonIndices1
#print 'Common indices 2:', commonIndices2

totalIndicesInCommon = len(commonIndices1) + len(commonIndices2)
totalChords = len(p1) + len(p2)

percentMatch1 = float(len(commonIndices1)) / len(p1)
percentMatch2 = float(len(commonIndices2)) / len(p2)

avgMatch = (percentMatch1 + percentMatch2) / 2
avgMatch2 = float(totalIndicesInCommon) / totalChords
#print 'Percent of 1 in common:', round(percentMatch1,3)
#print 'Percent of 2 in common:', round(percentMatch2,3)
#print 'Average percentage in common:', round(avgMatch,3)
#print 'Average percentage 2 in common:',round(avgMatch2,3)
'''
'''
X = p1
Y = p2
editDistance,table = EditDistance(X,Y)
#print 'Edit Distance:',editDistance

Yspaced = ''.join([str(c) + ' ' for c in Y])

#print '   ', str(Yspaced)
first = [ str(elem) for elem in table[0] ]
#print '  ' + ' '.join(first)
for i, row in enumerate(table[1:]):
    row = [ str(elem) for elem in row ]
    out = '%s %s' % (X[i], ' '.join(row))
    #print out

def MinMove(i,j,left,up,diag):
    minVal = min([diag,left,up])
    move = ''
    if minVal == diag: #diag
        i -= 1
        j -= 1
        move = 'diag'
    elif minVal == left: #left
        j -= 1
        move = 'left'
    elif minVal == up: #up
        i -= 1
        move = 'up'
    return i,j,move


Xcopy = X
Ycopy = Y
i = len(table) - 1
j = len(table[0]) - 1
#print '(%d,%d)' % (i,j),'start'
while i != 0 or j != 0:
    move = ''
    if i == 0:
        j -= 1
        move = 'left'
    elif j == 0:
        i -= 1
        move = 'up'
    else:
        left = table[i][j-1]
        up = table[i-1][j]
        diag = table[i-1][j-1]
        i,j,move = MinMove(i,j,left,up,diag)
    #print '(%d,%d)' % (i,j), move
'''
