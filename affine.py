#!/usr/bin/env python
"""Affine.

Description:
  This script performs the specified affine operation to a line of text.

  Affine cyphers have two variable keys.
    Cyphertext = (Cleartext * A + B ) mod 26
        where A {1-25}, B{0-25}

  The suite of ROTx (Caesarian) cyphers is the subset of Affine cyphers where 
  A = 1.  If keys A and B are not specified, this script performs the Caesarian
  operation.

Author: 
  Andrew Mattheisen

Usage:
  affine.py [-a AKEY] [-b BKEY] <cyphertext>...
  affine.py (-h | --help)
  affine.py --version

Options:
  -h --help     Show this screen.
  --version     Show version.
  -a=<akey>     Number of Characters to multiply cyphertext [default: 1].
  -b=<bkey>     Number of Characters to rotate cyphertext [default: 13].

"""
from __future__ import print_function
from docopt import docopt
import string
VERSION='1.0'
DATE='2014-05-09'
TITLE='Affine'


def affine(words, a, b ):
    if b == 0: # perform 25 encode iterations
        for b in range(1,26):
            (cypher_text, clear_text) = affine_encode(words, a, b)
            #if b == 1:
            #    prettyprint_affine(cypher_text, a, b, clear_text)
            #else:
            #    prettyprint_affine(cypher_text, a, b, clear_text, header=(b == 1))
            prettyprint_affine(cypher_text, a, b, clear_text, header=(b == 1))
            
    else: # encode just once
        (cypher_text, clear_text) = affine_encode(words, a, b)
        prettyprint_affine(cypher_text, a, b, clear_text)
    return


def affine_encode(words, a, b):
    clear_text = ""
    cypher_text = ""
    for cypher in words:
        cypher_text += cypher
        cypher = cypher.upper()
        for c in cypher:
            if not c in string.ascii_letters:
                clear_text += c
                continue
            new_c = chr(((ord(c) - 65) * a + b ) % 26 + 65 )
            #print(c, ' -> ', new_c)
            clear_text = ''.join([clear_text, new_c])
        clear_text += ' '
        cypher_text += ' '
    return cypher_text, clear_text


def prettyprint_affine(cypher_text, a, b, clear_text, header=True):
    if header:
        print("INPUT:          ", cypher_text)
    print("AFFINE(%2d,%-2d):  "%(a,b), clear_text)
    return


if __name__ == '__main__':
    args = docopt(__doc__, version='%s %s:%s'%(TITLE, VERSION, DATE))
    affine(args['<cyphertext>'], int(args['-a'].strip('=')), int(args['-b'].strip('=')))
