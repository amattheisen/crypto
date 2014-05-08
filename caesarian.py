#!/usr/bin/env python
"""Caesarian.

Description:
  This script performs the ROT13 operation (or any other ROT) to a line of text.

Author: 
  Andrew Mattheisen

Usage:
  caesarian.py [--rot ROT] <cyphertext>...
  caesarian.py (-h | --help)
  caesarian.py --version

Options:
  -h --help     Show this screen.
  --version     Show version.
  --rot=<rot>   Number of Characters to rotate cyphertext [default: 13].

Notes:
  Used to solve http://decodeingress.me/category/code-breaking-101/

"""
from __future__ import print_function
from docopt import docopt
import string
VERSION='1.0'
DATE='2014-05-06'
TITLE='Caesarian'

def caesarian(args):
    if args['--rot'] == 0:
        for rot in range(1,26):
            (cypher_text, clear_text) = rot_encode(args['<cyphertext>'], rot)
            if rot == 1:
                print("INPUT:  ", cypher_text)
            print("ROT%02d:  "%rot, clear_text)
            
    else:
        (cypher_text, clear_text) = rot_encode(args['<cyphertext>'], args['--rot'])
        print("INPUT:  ", cypher_text)
        print("ROT%2d:  "%args['--rot'], clear_text)
    return


def rot_encode(words, rot):
    clear_text = ""
    cypher_text = ""
    for cypher in words:
        cypher_text += cypher
        cypher = cypher.upper()
        for c in cypher:
            if not c in string.ascii_letters:
                clear_text += c
                continue
            new_c = chr((ord(c) - 65 + rot ) % 26 + 65 )
            #print(c, ' -> ', new_c)
            clear_text = ''.join([clear_text, new_c])
        clear_text += ' '
        cypher_text += ' '
    return (cypher_text, clear_text)


if __name__ == '__main__':
    args = docopt(__doc__, version='%s %s:%s'%(TITLE, VERSION, DATE))
    args['--rot'] = int(args['--rot'])
    caesarian(args)
