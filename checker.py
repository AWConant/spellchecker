from collections import Counter
from string import ascii_lowercase#as lowers
from itertools import chain
from operator import itemgetter

def readCorpus(filename):
    """
    Return a Counter containing the count of every word in file denoted by
    filename.
    """
    word_counts = Counter()
    with open(filename, 'r') as f:
        for line in f:
            word_counts += Counter(line.split())

    return word_counts

def getDeletions(s):
    """
    Return a generator for all strings that can be produced by removing a 
    single letter from s.
    """
    return (s[:i] + s[i+1:] for i in range(len(s)))

def getAlterations(s):
    """
    Return a generator for all strings that can be produced by changing a 
    single letter in s.
    """
    return chain.from_iterable( ((s[:i]+ch+s[i+1:] for ch in ascii_lowercase)
                                 for i
                                 in range(len(s))) )

def getInsertions(s):
    """
    Return a generator for all strings that can be produced by inserting a 
    single letter in s.
    """
    return chain.from_iterable( ((s[:i]+ch+s[i:] for ch in ascii_lowercase)
                                 for i
                                 in range(len(s))) )

def getTranspositions(s):
    """
    Return a generator for all strings that can be produced by swapping two 
    adjacent letters in s.
    """
    return (s[:i] + s[i+1] + s[i] + s[i+2:] for i in range(len(s)-1))

def closestMatch(word, word_counts):
    """
    Return the most common string in word_counts that is a single edit away 
    from word.
    """
    # If the queried word is already a word, return it immediately.
    if word_counts[word] > 0:
        return word

    # Generate the set of strings that are a single edit away from word.
    edit_getters = [getDeletions, getAlterations,
                    getInsertions, getTranspositions]
    candidates = chain.from_iterable( (getter(word) for getter in edit_getters) )

    # Remove adjacencies that are not real words according to word_counts.
    candidates = filter(lambda c: word_counts[c] > 0, candidates)

    # Return the most common neighbor. If there are no valid neighbors, say so.
    return max(candidates, key=word_counts.get, default='No close matches')

def main():
    word_counts = readCorpus('10k.txt')

    print('Input a blank string to quit.')
    while True:
        to_check = input('>>> ')
        if to_check == '':
            break
        fixed = ''
        for word in to_check.split():
            fixed += closestMatch(word, word_counts) + ' '
        print(fixed)

if __name__ == '__main__':
    main()
