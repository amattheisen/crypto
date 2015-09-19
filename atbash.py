#!/usr/bin/env python
"""Atbash.

Description:
  This script performs the Atbash operation to a line of text.

Author: 
  Andrew Mattheisen

Usage:
  atbash.py <cyphertext>...
  atbash.py (-h | --help)
  atbash.py --version

Options:
  -h --help     Show this screen.
  --version     Show version.

"""
from __future__ import print_function
from docopt import docopt
import string
VERSION='1.1'
DATE='2015-09-19'
TITLE='Altbash'


def main(args):
    (cypher_text, clear_text) = altbash_encode(args['<cyphertext>'])
    print("INPUT:    ", cypher_text)
    print("ALTBASH:  ", clear_text)
    return


def altbash_encode(words):
    clear_text = ""
    cypher_text = ""
    for cypher in words:
        cypher_text += cypher
        cypher = cypher.upper()
        for c in cypher:
            if not c in string.ascii_letters:
                clear_text += c
                continue
            # A = 65, Z = 90
            new_c = chr( (90 - (ord(c) - 65)) )
            #print(c, ' -> ', new_c)
            clear_text = ''.join([clear_text, new_c])
        clear_text += ' '
        cypher_text += ' '
    return (cypher_text, clear_text)


if __name__ == '__main__':
    args = docopt(__doc__, version='%s %s:%s'%(TITLE, VERSION, DATE))
    main(args)
