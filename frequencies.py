#!/usr/bin/env python2
'''frequencies.py letter frequency analysis & data

Author: Andrew Mattheisen

table data copied from "Secret History: The Story of Cryptography"

'''
from __future__ import print_function
import json

WORD_PATTERN_FILE = "word_patterns.json"

# Overall Frequency of letters (%)
letter_freq = {
  "a" : 8.2, 
  "b" : 1.5,
  "c" : 2.8,
  "d" : 4.3,
  "e" : 12.7,
  "f" : 2.2,
  "g" : 2.0,
  "h" : 6.1,
  "i" : 7.0,
  "j" : 0.2,
  "k" : 0.8,
  "l" : 4.0,
  "m" : 2.4,
  "n" : 6.7,
  "o" : 7.5,
  "p" : 1.9,
  "q" : 0.1,
  "r" : 6.0,
  "s" : 6.3,
  "t" : 9.0,
  "u" : 2.8,
  "v" : 1.0,
  "w" : 2.4,
  "x" : 0.2,
  "y" : 2.0,
  "z" : 0.1,
  }

# Frequency of Letters in inital and terminal positions for 1000 words
letter_pos_freq = {
  "a" : { "initial_pos" : 123.6, "term_pos" :  24.7 },
  "b" : { "initial_pos" :  42.2, "term_pos" :   0.9 },
  "c" : { "initial_pos" :  47.0, "term_pos" :   3.7 },
  "d" : { "initial_pos" :  20.6, "term_pos" : 111.0 },
  "e" : { "initial_pos" :  27.7, "term_pos" : 222.9 },
  "f" : { "initial_pos" :  41.9, "term_pos" :  49.3 },
  "g" : { "initial_pos" :  12.3, "term_pos" :  25.1 },
  "h" : { "initial_pos" :  47.5, "term_pos" :  34.2 },
  "i" : { "initial_pos" :  59.0, "term_pos" :   0.9 },
  "j" : { "initial_pos" :   7.0, "term_pos" :   0.0 },
  "k" : { "initial_pos" :   1.8, "term_pos" :   8.7 },
  "l" : { "initial_pos" :  22.4, "term_pos" :  24.7 },
  "m" : { "initial_pos" :  39.2, "term_pos" :  20.1 },
  "n" : { "initial_pos" :  21.6, "term_pos" :  67.6 },
  "o" : { "initial_pos" :  70.8, "term_pos" :  41.4 },
  "p" : { "initial_pos" :  40.9, "term_pos" :   6.4 },
  "q" : { "initial_pos" :   2.2, "term_pos" :   0.0 },
  "r" : { "initial_pos" :  31.2, "term_pos" :  47.5 },
  "s" : { "initial_pos" :  69.1, "term_pos" : 137.0 },
  "t" : { "initial_pos" : 181.3, "term_pos" :  98.1 },
  "u" : { "initial_pos" :  14.1, "term_pos" :   2.3 },
  "v" : { "initial_pos" :   4.1, "term_pos" :   0.0 },
  "w" : { "initial_pos" :  63.3, "term_pos" :   3.7 },
  "x" : { "initial_pos" :   0.4, "term_pos" :   1.4 },
  "y" : { "initial_pos" :   7.5, "term_pos" :  66.2 },
  "z" : { "initial_pos" :   0.4, "term_pos" :   0.0 }, 
  }

# Most Common Doubled Letters in 1000 words
double_letter_freq = {
 "ll" : 19,
 "ss" : 15,
 "ee" : 14,
 "oo" : 12,
 "tt" :  9,
 "ff" :  9,
 "rr" :  6,
 "nn" :  5,
 "pp" :  4.5,
 "cc" :  4,
 "mm" :  4,
 "gg" :  4,
 "dd" :  1.5,
 "aa" :  0.5,
 "bb" :  0.25,
  }


def write_pattern_file(patterns, filename):
    '''Write patterns dictionary to json file.'''
    with open(filename, 'w') as fdout:
        json.dump(patterns, fdout)
    return


def read_pattern_file(filename=WORD_PATTERN_FILE):
    '''Create patterns dictionary from json file.'''
    with open(filename, 'r') as fdin:
        patterns = json.load(fdin)
    for pattern in patterns:
        for position,word in enumerate(patterns[pattern]):
            patterns[pattern][position] = str(word) # string please, no unicode
    return patterns


def create_word_patterns(word_list_filename, verbose=False):
    '''Create a dictionary of word patterns from a word file.'''
    letters = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n',
      'o','p','q','r','s','t','u','v','w','x','y','z'] 
    with open(word_list_filename, 'r') as fd:
        patterns = {}
        for line in fd:
            word = line.strip().lower()
            if word[-1] == "%":
                # skip uncountable plurals
                continue
            if word[0] in letters:
                letters.remove(word[0])
                if verbose:
                    print("update: found first word starting with %s" % word[0])
            pattern = get_pattern(word)
            if not pattern in patterns.keys():
                patterns[pattern] = []
            if not word in patterns[pattern]:
                patterns[pattern].append(word)
    return patterns


def get_pattern(word):
    '''Determine the pattern for a word.'''
    # ASSUME: no more than 26 unique chars in a word
    PATTERN_CHARS = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N',
      'O','P','Q','R','S','T','U','V','W','X','Y','Z'] 
    # ASSUME: no distinction between uppercase and lowercase
    word = word.lower()
    # determine chars in word
    chars = []
    for char in word:
        if not char.lower() in chars:
            chars.append(char)
    # create pattern
    pattern = word
    for char_index, char in enumerate(chars):
        pattern = pattern.replace(char,PATTERN_CHARS[char_index])
    return pattern    


def get_words_for_pattern(pattern, patterns=read_pattern_file(WORD_PATTERN_FILE)):
    '''Retieve all words matching pattern from patterns.
    The default patterns is all words in the english language'''
    words = []
    for word in patterns[pattern]:
        words.append(word)
    words.sort()
    return words


def filter_words(words, indexes, chars, verbose=False):
    '''Filter word list to only words matching one or more known characters'''
    # allow lazy users
    if type(indexes) != type([]):
        indexes = [indexes]
    if type(chars) != type([]):
        chars = [chars]
    filtered_words = []
    for word in words:
        if word[indexes[0]] == chars[0]:
            filtered_words.append(word)
    if len(indexes) != 1:
        # multi-character guess
        for ii in range(1,len(indexes)):
            for word in filtered_words:
                if not word[indexes[ii]] == chars[ii]:
                    filtered_words.remove(word)
    if verbose:
        print("wordlist reduced from %d to %d words" % (
          len(words), len(filtered_words) ) )
    return filtered_words


# =============================================================================
# TESTS
# =============================================================================
def test_get_pattern():
    '''Test function get_pattern().'''
    test_pattern = get_pattern("AarDvarK")
    if test_pattern == "AABCDABE":
        return True # passed
    return False # failed


def test_create_word_patterns_list():
    '''Test function create_word_patterns().'''
    test_list = {
      "A"        : ['i', 'a'],
      "ABBCD"    : ['apple'],
      "ABB"      : ['add'],
      "ABC"      : ['the', 'why', 'car', 'bin', 'and', 'can', 'eat'],
      "ABCDAE"   : ['taiste'],
      "ABCCBCCB" : ['bannanna'],
      "ABCDA"    : ['going'],
      "ABCDC"    : ['these'],
      "ABCDE"    : ['thine', 'fruit'],
      "ABCDD"    : ['three'],
      "ABCD"     : ['more'],
      "ABCCA"    : ['yummy'],
      "AB"       : ['am', 'do', 'to', 'go'],
      "ABCCAD"   : ['little'],
      "ABCDEF"   : ['fruity', 'fruits'],
      }
    pattern_list = create_word_patterns("test_word_list.txt")
    for pattern in pattern_list:
        if not pattern in test_list.keys():
            print("pattern %s not found" % pattern)
            return False # failed
        for word in pattern_list[pattern]:
            if not word in test_list[pattern]:
                print("word %s not found for pattern %s" % (word, pattern) )
                return False # failed
    return True


def test_read_write():
    '''Test function write_pattern_file() and read_pattern_file().'''
    filename = "patterns_test_word_list.txt.json"
    patterns = create_word_patterns("test_word_list.txt")
    write_pattern_file(patterns, filename)
    read_patterns = read_pattern_file(filename)
    # compare read patterns to written ones
    for pattern in read_patterns:
        if not pattern in patterns:
            print("pattern %s not found" % pattern)
            return False # failed
        for word in read_patterns[pattern]:
            if not word in patterns[pattern]:
                print("word %s not found for pattern %s" % (word, pattern) )
                return False # failed
    return True # passed


def test_get_words_for_pattern():
    '''Test function get_words_for_pattern().'''
    result = True # start assuming test will pass
    # test specifying patterns
    pattern = "ABC"
    expected_words = ['the', 'why', 'car', 'bin', 'and', 'can', 'eat']
    patterns = create_word_patterns("test_word_list.txt")
    words = get_words_for_pattern(pattern, patterns)
    for word in expected_words:
        if not word in words:
            print("Error: missing word %s" %word)
            result = False # failed
    # test without specifying patterns
    pattern = "ABCDEFGHIDGB" 
    expected_words = ["recapitulate"]
    words = get_words_for_pattern(pattern)
    for word in expected_words:
        if not word in words:
            print("Error: missing word %s" %word)
            result = False # failed
    return result


def test_refine_words():
    '''Test function filter_words()'''
    result = True # start assuming test will pass
    words = ['pediatrics', 'pediculina', 'pedicurism', 'pedicurist']
    # test with lists
    chars = ['e', 'c']
    indexes = [1, 4]
    expected = ['pediculina', 'pedicurism', 'pedicurist']
    filtered_words = filter_words(words, indexes, chars) 
    if len(filtered_words) != len(expected):
        result = False # failed - wrong number of words
    for word in expected:
        if not word in filtered_words:
            result = False # failed - word missing
    # test lazy user
    chars = 'r'
    indexes = 6
    expected = ['pediatrics', 'pedicurism', 'pedicurist']
    filtered_words = filter_words(words, indexes, chars) 
    if len(filtered_words) != len(expected):
        result = False # failed - wrong number of words
    for word in expected:
        if not word in filtered_words:
            result = False # failed - word missing
    return result


def run_tests():
    '''Run all tests for this file.'''
    result = "passed" # start assuming tests will pass
    print("\n"+15*'=', "Testing module %s" % __file__, 15*'=')
    tests = [
      (test_get_pattern(),"Test get_pattern:"),
      (test_create_word_patterns_list(), "Test create_word_patterns:"),
      (test_read_write(), "Test read_pattern_file and write_pattern_file:"),
      (test_get_words_for_pattern(), "Test get_words_for_pattern:"),
      (test_refine_words(), "Test refine_words:")
      ]
    for test in tests:
        this_result = "passed" if test[0] else "failed"
        print("%-46s"%test[1], this_result)
        if not test[0]: 
            result = "failed"

    if result != "passed":
        print(15*'=',"Result: One or more tests failed.", 15*'=')
        return False # failed one or more tests
    print(15*'=', "Result: All tests passed.", 15*'=')
    return True # passed all tests


# =============================================================================
# Untested Functions
# =============================================================================
def print_words(words):    
    '''Print up to 25 words from a list of words.'''
    for counter,word in enumerate(words):
        if counter >= 25:
            print("%d more words not shown" % (len(words) - 25))
            break # don't print too many words
        print(word)
    return


if __name__ == "__main__":
    result = run_tests()
