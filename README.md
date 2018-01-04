Lin Similarity
================================

NAME
----

sim.py - computes Lin similarity of a given noun and all other nouns in a given file

SYNOPSIS
--------

`python sim.py INPUTFILE INPUTWORD`

DESCRIPTION
-----------

`sim.py` is a simple program which computes the [Lin similarity](http://webdocs.cs.ualberta.ca/~lindek/papers/sim.pdf) of a given input noun and all others nouns in the given input file, whereby similarity is defined as

> the ratio between the amount of information in the commonality and the amount of information in the description of the two objects.

Dependency triples are extracted from the given input file and stored as features of the nouns. The amount of information contained in every single feature is calculated accordingly. Pairwise similarity is computed between the given input noun and nouns with at least one similar feature. The fifty most similar words are displayed in descending order of their similarity.

FILES
-----

**INPUTFILE**

The input file must be in [CoNLL09 format](http://nextens.uvt.nl/depparse-wiki/DataFormat).

**INPUTWORD**

The input word must be a noun.

EXAMPLE
-------

**INPUTFILE**

[tiger_ release_ aug07.corrected.16012013.conll09](http://www.ims.uni-stuttgart.de/forschung/ressourcen/korpora/tiger.html)


**INPUTWORD**

Mann


**COMMAND**

    $ python sim.py tiger_ release_ aug07.corrected.16012013.conll09 Mann
    

**OUTPUT**

    Mensch
    Frau
    Teil
    Regierung
    Million
    Prozent
    Land
    Experte
    Zahl
    Präsident
    ...

AUTHOR
------
Melanie Tosik, tosik@uni-potsdam.de
