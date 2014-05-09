#!/usr/bin/env python
"""Affine.

Description:
  This script performs the specified affine operation to a line of text.

  Affine cyphers have two variable keys.
    Cyphertext = (Cleartext * A + B ) mod 26
        where A {1, 3, 5, 7, 9, 11, 15, 17, 19, 21, 23, 25},
              B {0-25}

  The suite of ROTx (Caesarian) cyphers is the subset of Affine cyphers where 
  A = 1.  If keys A and B are not specified, this script performs the Caesarian
  (ROT13) operation.

Author: 
  Andrew Mattheisen

Usage:
  affine.py [-a AKEY] [-b BKEY] [-d] <cyphertext>...
  affine.py (-h | --help)
  affine.py --version

Options:
  -h --help     Show this screen.
  --version     Show version.
  -a=<akey>     Number of Characters to multiply cyphertext [default: 1].
                'a' must be both less than and coprime to 26.
  -b=<bkey>     Number of Characters to rotate cyphertext [default: 13].
  -d            Use the decypher algorithm instead of the encypher algorithm.

"""
from __future__ import print_function
from docopt import docopt
import string
VERSION='1.0'
DATE='2014-05-09'
TITLE='Affine'
ALLOWED_A_VALUES=[1,3,5,7,9,11,15,17,19,21,23,25]
INVERSE_A={
   1 : 1  ,  
   3 : 9  ,  
   5 : 21 ,
   7 : 15 ,
   9 : 3  ,
  11 : 19 ,
  15 : 7  ,
  17 : 23 ,
  19 : 11 ,
  21 : 5  ,
  23 : 17 ,
  25 : 25 , }


def affine(words, a, b, decypher=False):
    if b == 0: # perform 25 encode iterations
        for b in range(1,26):
            (cypher_text, clear_text) = affine_(words, a, b, decypher)
            prettyprint_affine(cypher_text, a, b, clear_text, decypher, header=(b == 1))
    else: # encode just once
        (cypher_text, clear_text) = affine_(words, a, b, decypher)
        prettyprint_affine(cypher_text, a, b, clear_text, decypher)
    return


def affine_(words, a, b, decypher=False):
    if decypher:
        a = INVERSE_A[a]
        f = affine_decode
    else:
        f = affine_encode
    clear_text = ""
    cypher_text = ""
    for cypher in words:
        cypher_text += cypher
        cypher = cypher.upper()
        for c in cypher:
            if not c in string.ascii_letters:
                clear_text += c
                continue
            new_c = f(a, b, c)
            #print(c, ' -> ', new_c)
            clear_text = ''.join([clear_text, new_c])
        clear_text += ' '
        cypher_text += ' '
    return cypher_text, clear_text


def affine_decode(a, b, char):
    return chr(((ord(char) - 65 - b ) * a ) % 26 + 65 )


def affine_encode(a, b, char):
    return chr(((ord(char) - 65) * a + b ) % 26 + 65 )


def prettyprint_affine(cypher_text, a, b, clear_text, decypher=False,
  header=True):
    operation = "DE-AFFINE" if decypher else "AFFINE"
    spaces = " " * ( len(operation) + 4 )
    if header:
        print("INPUT:%s"%spaces, cypher_text)
    print("%s(%2d,%-2d):  "%(operation, a, b), clear_text)
    return


def check_inputs(args):
    passed = True
    if int(args['-a'].strip('=')) not in ALLOWED_A_VALUES:
        print("ERROR: A not in %s"%ALLOWED_A_VALUES)
        passed = False
    if int(args['-b'].strip('=')) not in range(26):
        print("ERROR: B not in %s"%range(26))
        passed = False
    return passed


if __name__ == '__main__':
    args = docopt(__doc__, version='%s %s:%s'%(TITLE, VERSION, DATE))
    if check_inputs(args):
        affine(args['<cyphertext>'], int(args['-a'].strip('=')), 
          int(args['-b'].strip('=')), args['-d'])
