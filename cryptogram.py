#!/usr/bin/env python
"""Cryptogram.

Description:
  This script statistically analyses a line of text to help solve a cryptogram

Author: 
  Andrew Mattheisen

Usage:
  cryptogram.py <cyphertext>...
  cryptogram.py (-h | --help)
  cryptogram.py --version

Options:
  -h --help     Show this screen.
  --version     Show version.

Additional features to implement: 
    Look for prefixes
      {ex-, over-, un-, or up-}
    Look for suffexes
      {-ed, -er, -man or -men, or -ful}
    Look for 1 letter words (If spaces are provided)
      These are most likely {I, a}
    Identify the vowels
      1 letter words
      double vowels are usually {ee, aa}
      the most common vowell is 'e' and the least common is 'u'

cyphertext of interest: 
  tpfccdlfdtte pcaccplircdt dklpcfrp?qeiq lhpqlipqeodf gpwafopwprti izxndkiqpkii krirrifcapnc dxkdciqcafmd vkfpcadf.

cyphertext source: 
  tweet from NSA https://twitter.com/NSACareers/status/463321993878994945
    
source of strategies: 
  http://www.bigfishgames.com/blog/cryptogram-tips-tricks-and-strategies/

"""
from __future__ import print_function
from docopt import docopt
import string
VERSION='1.0'
DATE='2014-05-06'
NAME='Cryptogram'

def main(args):
    # BUILD CYPHERTEXT
    cyphertext = ""
    for cypher in args['<cyphertext>']:
        cypher = cypher.upper()
        cyphertext += cypher
    print("")
    prettyprint_text('INPUT TEXT', cyphertext)

    # COUNTS
    cypher_char_counts = count_chars(cyphertext)
    prettyprint_counts(cypher_char_counts)

    # DOUBLES
    highlight_doubles(cyphertext)
    return

def highlight_doubles(text):
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
    

def prettyprint_counts(counts):
    print("== COUNTS ==")
    sorted_keys = sorted(counts.iteritems(), key=lambda (k,v): (v,k), reverse=True)
    for ii,(key,value) in enumerate(sorted_keys):
        if ii !=0 and ii%10 == 0:
            print("")
        print("  %1s:%3d"%(key, value), sep='', end=''),
    print("\nThe most common English letters are {e, t, s, d, n, r, y}",'\n')
    return

def prettyprint_text(title, text):
    print("== %s =="%title)
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

if __name__ == '__main__':
    args = docopt(__doc__, version='%s %s:%s'%(NAME, VERSION, DATE))
    main(args)
