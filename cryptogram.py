#!/usr/bin/env python
"""Cryptogram.

Description:
  This script statistically analyses a line of text to help solve a cryptogram

Author: 
  Andrew Mattheisen

Usage:
  cryptogram.py analyze <cyphertext>...
  cryptogram.py analyze -i <cyphertext>...
  cryptogram.py sub -f <file> <cyphertext>...
  cryptogram.py sub -i -f <file> <cyphertext>...
  cryptogram.py <cyphertext>...
  cryptogram.py -i <cyphertext>...
  cryptogram.py (-h | --help)
  cryptogram.py --version

Options:
  -h --help     Show this screen.
  --version     Show version.
  -i            Ignore spaces. Use this when spaces are not provided between words.

"""
from __future__ import print_function
"""
Additional features to implement: 
    Look for prefixes
      {ex-, over-, un-, or up-}
    Look for suffexes
      {-ed, -er, -man or -men, or -ful}
    Look for 1 letter words (If spaces are provided)
      These are most likely {I, a}
    Identify the vowels - use sukhotin's Method
      1 letter words
      double vowels are usually {ee, aa}
      the most common vowell is 'e' and the least common is 'u'
      
    Look for digraphs
    Look for trigrams
      http://en.wikipedia.org/wiki/Trigram#cite_note-1
    Look for words / Autosolve
      Use words file. Difficult to do if spaces are not provided. Algorithm needed
      Bruit force - look through 26! possibilities of letter maps
        and count #words in solution.  display solutions containing the most words
      

cyphertext of interest: 
  tpfccdlfdtte pcaccplircdt dklpcfrp?qeiq lhpqlipqeodf gpwafopwprti izxndkiqpkii krirrifcapnc dxkdciqcafmd vkfpcadf.

cyphertext source: 
  tweet from NSA https://twitter.com/NSACareers/status/463321993878994945
    
source of strategies: 
  http://www.bigfishgames.com/blog/cryptogram-tips-tricks-and-strategies/
  http://www.gtoal.com/wordgames/cryptograms.html
  http://www.muth.org/Robert/Cipher/substitution/
  http://www.quipqiup.com/howwork.php
"""
from docopt import docopt
import string
from termcolor import colored
import re

VERSION='1.0'
DATE='2014-05-06'
NAME='Cryptogram'



def substitute(args):
    """This Function prints the result of a requested substitution
    
    In the substitution,  
        Uppercase blue is CLEARTEXT, 
        lowercase green is CYPHERTEXT """
    # BUILD & PRINT CYPHERTEXT
    cyphertext = build_cyphertext(args)
    prettyprint_text('INPUT TEXT', cyphertext)

    filename = args['<file>']
    decodes = read_guess_file(filename)

    # PERFORM SUBSTITUTION
    print("")
    for c in cyphertext:
        if c in decodes.keys():
            print(colored(decodes[c], 'blue', attrs=['bold']), end="")
        else:
            if c in string.uppercase:
                c = c.lower()
            print(colored(c, 'green', attrs=['underline']), end="")
    print("\n")

    return


def read_guess_file(filename):
    """ This Function parses the guess file """
    is_decode = re.compile("^\s*(?P<cypher>[a-zA-Z])\s*=\s*(?P<clear>[a-zA-Z])[\s$#]")
    decodes = {}
    fd = open(filename, 'r')
    for line in fd:
        m = is_decode.search(line)
        if not m:
            continue
        #print(line, m.group('cypher'), m.group('clear'))
        if m.group('cypher') in decodes.keys():
            print("WARNING: Cypherchar \'%s\'"%m.group('cypher'), " specified multiple times in guess file - using last occurance.")
        decodes[m.group('cypher')] = m.group('clear')
    return decodes


def analyze(args):
    # BUILD & PRINT CYPHERTEXT
    cyphertext = build_cyphertext(args)
    prettyprint_text('INPUT TEXT', cyphertext)

    # CHARACTER COUNTS
    cypher_char_counts = count_chars(cyphertext)
    prettyprint_counts('CHARACTER', cypher_char_counts)

    # DOUBLES
    highlight_doubles(cyphertext)

    # CHARACTER SEQUENCES
    sequence_counts = count_sequences(cyphertext)
    prettyprint_counts('SEQUENCE', sequence_counts)

    # IDENTIFY POTENTIAL VOWELLS
    sukhotin(cyphertext)

    return

def sukhotin(text):
    freq = [ [ 0 for ii in range(26) ] for jj in range(26) ]
    for letter in string.uppercase:
        c = "@"
        last_c = "@"
        for next_c in text+"@":
            if c == letter:
                #print("DEBUG: ", "last_c=%s, "%last_c, "c=%s, "%c, "next_c=%s."%next_c)
                if last_c in string.uppercase:
                    freq[(ord(c)-65)][(ord(last_c)-65)] += 1
                    freq[(ord(last_c)-65)][(ord(c)-65)] += 1
                if next_c in string.uppercase:
                    freq[(ord(c)-65)][(ord(next_c)-65)] += 1
                    freq[(ord(next_c)-65)][(ord(c)-65)] += 1
            last_c = c
            c = next_c
    # zero diagonal
    for ii in range(26):
        freq[ii][ii] = 0

    # Determine SUMS:
    sums = [0 for ii in range(26)]
    letter_types = ["C" for ii in range(26)]
    for ii in range(26):
        sums[ii] = sum(freq[ii])

    # Identify Vowells 
    vowels = []
    for round_num in range(1,6):
        if round_num > 1:
            # reduce sums for letters connected to last round's winner
            for ii in range(26):
                sums[ii] -= freq[ii][ord(max_letter)-65]*2
        # get max sum
        max_sum = 0
        for ii in range(26):
            if letter_types[ii] == "C" and sums[ii] > max_sum:
                max_sum = sums[ii]
        # get letter
        max_letters = [chr(ii+65) for ii,value in enumerate(sums) if (
          value == max_sum and letter_types[ii] == "C")]
        max_letter = max_letters[0] # pick lowest letter if there is a tie
        letter_types[ord(max_letter)-65] = "V"
        # debugging
        #print_sukhotin_state_debug(freq, sums, letter_types)
        vowels.append(max_letter)
    print ("\n== SUKHOTIN ==")
    print("Vowell(s) in order of confidence are ", vowels)
    return 

def print_sukhotin_state_debug(freq, sums, letter_types):
    print ("== SUKHOTIN ==")
    print ("    ", end="")
    for letter in string.uppercase:
        print("%3s"%letter, end = "")
    print("  SUM  C/V")
    for ii,letter in enumerate(string.uppercase):
        print("%3s  "%letter, end = "")
        for value in freq[ii]:
            print("%2d "%value, end="")
        print(" %3d   "%sums[ii], "%s"%letter_types[ii])
    return


def count_sequences(text):
    ''' Count recurring sequences of characters '''
    counts = {}
    last_c = ""
    second_last_c = ""
    for c in text:
        sequence2chars = last_c + c
        sequence3chars = second_last_c + last_c + c
        # check if sequence2chars contains punctuation or space
        sequence2chars_valid = True
        for char in sequence2chars:
            if char not in string.letters and char not in string.digits:
                sequence2chars_valid = False
                break
        # check if sequence3chars contains punctuation or space
        sequence3chars_valid = True
        for char in sequence3chars:
            if char not in string.letters and char not in string.digits:
                sequence3chars_valid = False
                break
        if sequence2chars_valid:
            if sequence2chars not in counts.keys():
                counts[sequence2chars] = 1
            else:
                counts[sequence2chars] += 1
        if sequence3chars_valid:
            if sequence3chars not in counts.keys():
                counts[sequence3chars] = 1
            else:
                counts[sequence3chars] += 1
        second_last_c = last_c
        last_c = c
    # remove all counts that only occured once
    for key, value in counts.items():
        if value == 1:
            del counts[key]
    return counts


def highlight_doubles(text):
    ''' Show where doubles occur in text '''
    print("== DOUBLES ==")
    last_c = ""
    doubles = ""
    for ii,c in enumerate(text):
        if ii !=0 and ii%80 == 0:
            print('\n', doubles)
            doubles = ""
        if c == last_c:
            doubles = doubles[:-2] + '^^ '
        else:
            doubles += ' '
        print(c, sep='', end='')
        last_c = c   
    if len(doubles)>0:
        print('\n', doubles)
    print("The most common English doubles are {ll, tt, ss, ee, pp, oo, rr, ff, cc, dd, nn}", '\n')
    return
    

def prettyprint_counts(title, counts):
    ''' print counts with formatting '''
    print("== %s COUNTS =="%title)
    sorted_keys = sorted(counts.iteritems(), key=lambda (k,v): (v,k), reverse=True)
    for ii,(key,value) in enumerate(sorted_keys):
        if ii !=0 and ii%10 == 0:
            print("")
        print("%4s:%3d"%(key, value), sep='', end=''),
    if title == 'CHARACTER':
        print("\nThe most common English letters are {e, t, a, o, i, n, s, h} in that order",'\n')
    if title == 'SEQUENCE':
        print("") # TODO: Are there a list of most common sequences?
    return


def prettyprint_text(title, text):
    print("\n== %s =="%title)
    for ii,c in enumerate(text):
        if ii !=0 and ii%80 == 0:
            print("")
        print(c, sep='', end='')
    print("\n")
    return


def count_chars(cyphertext):
    counts = {}
    for c in cyphertext:
        if not c in string.ascii_letters:
            # excludes numbers, symbols, spaces, and punctuation
            continue
        if c not in counts.keys():
            counts[c] = 1
        else:
            counts[c] += 1
    return counts


def build_cyphertext(args):
    input_text = ""
    cyphertext = ""
    for ii, cypher in enumerate(args['<cyphertext>']):
        cypher = cypher.upper()
        if ii == 0 or args['-i']: # remove spaces
            input_text += cypher
        else: # preserve spaces
            input_text += ' %s'%cypher
    for c in input_text:
        if c in string.uppercase:
            cyphertext += c
            args['has_letters'] = True
        elif c in string.whitespace and not args['-i']:
            cyphertext += c
            args['has_whitespace'] = True
        elif c in string.punctuation:
            cyphertext += c
            args['has_punctuation'] = True
        elif c in string.digits:
            cyphertext += c
            args['has_digits'] = True
        else:
            # ignore non printable characters
            continue
    return cyphertext


if __name__ == '__main__':
    args = docopt(__doc__, version='%s %s:%s'%(NAME, VERSION, DATE))
    if args['sub']:
        substitute(args)
    else:
        analyze(args)
