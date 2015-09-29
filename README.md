crypto
======

A collection of scripts to perform cryptographic analysis

Development notes:  I develop using vim and a python shell.  To test module
changes to module foo, I type the following in the python shell:

    import sys
    reload(sys.modules['foo'])
    from foo import *

Words list: Pattern recognition requires a words list.  There are several words
lists available.  I'm using the official 2of12inf list from 
http://wordlist.aspell.net/12dicts/ . Note that I strip out words ending in % 
(the uncountable plurals, e.g. 'abandonments%').


