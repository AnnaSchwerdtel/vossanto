#!/usr/bin/python2
# -*- coding: utf-8 -*-

#
# Finds Vossanto's in text.
#
# Usage:
#
# Author: rja
#
# Changes:
# 2017-02-17 (rja)
# - added output of match
# 2016-06-12 (rja)
# - initial version

from __future__ import print_function
import re
import sys

#from nltk.tokenize import wordpunct_tokenize
import nltk
from nltk.corpus import treebank
from nltk.tokenize import wordpunct_tokenize, sent_tokenize, word_tokenize
from nltk.sem.relextract import tree2semi_rel, semi_rel2reldict
from nltk.tree import Tree


####
# pre-compiled regular expressions

# To match
#
# (S
#    Everybody/NN
#    knows/VBZ
#    that/IN
#    (PERSON Helmut/NNP Kohl/NNP)
#    is/VBZ
#    the/DT
#    (ORGANIZATION Shakespeare/NNP)
#    of/IN
#    politics/NNS
#    ./.)
#
# and other patterns
vossanto_re_str = """
(                                         # an entity
  \((PERSON|ORGANIZATION|GPE)\ (?P<x10>[^)]*?)\)
  (\ \((PERSON|ORGANIZATION)\ (?P<x11>[^)]*?)\))?
  (\ (?P<x12>[^/()]*?)/NNP?)?
)

\ 
(                                         # is 
(is|has|are)/VBZ (\ (often|sometimes)/RB)? (\ been/VBN)? (\ called/VBN)?|
-/:|
,/,
)

\ the/DT                                  # the

\ 
(                                         # entity
  \((PERSON|ORGANIZATION|GPE)\ (?P<y11>[^)]*?)\) 
  (\ (?P<y12>[^/()]*?)/NNP?)?
|
  (?P<y31>[^/()]*?)/NNP
)

\ (of|among|from)/IN                      # of

\ (                                       # another entity
  ((?P<z10>[^/()]*?)/(CD|DT|JJ|IN))? 
  (?P<z11>[^/()]*?)/(NNS?|DT)
  (\ (?P<z12>[^/()]*?)/(IN|JJ))? 
  (\ (?P<z13>[^/()]*?)/NNS?)?
|
  (?P<z31>[^/()]*?)/NNP
|
  ((?P<z40>[^/()]*?)/(CD|DT|JJ)\ )? 
  \((ORGANIZATION|PERSON|GPE)\ (?P<z41>[^)]*?)\)
  (\ (?P<z43>[^/()]*?)/NN[SP]?)?
)

\ [\.,-]/[\.,:]
"""
vossanto_re = re.compile(vossanto_re_str, re.VERBOSE)

# convert parse tree generated by nltk.chunk.ne_chunk() into a string
def tags2str(tags):
    parts = []
    for tag in tags:
        if isinstance(tag, Tree):
            parts.append("(" + tag.label() + " " + " ".join([t[0] for t in tag.leaves()]) + ")")
        else:
            parts.append(tag[0] + "/" + tag[1])
    return " ".join(parts)

def vossanto(sentence, verbose=False):
    # split into words
    words = word_tokenize(sentence)

    # POS
    tagged = nltk.pos_tag(words)

    # NER
    entities = nltk.chunk.ne_chunk(tagged)

    # prepare for matching
    ttext = tags2str(entities)

    # debug
    #if "Mozart" in sentence:
    if verbose:
        print(ttext)


    #print(ttext)
    # match
    m = vossanto_re.search(ttext)
    if m:
        d = m.groupdict()
        x = d["x10"]
        if d["x11"]:
            x += " " + d["x11"]
        if d["x12"]:
            x += " " + d["x12"]
        # y
        y = d["y11"]
        if d["y12"]:
            y += " " + d["y12"]
        if not y:
            y = d["y31"]        
                
        # z CD? NN* NNS*?
        z = d["z11"]
        if d["z10"]:
            z = d["z10"] + z
        if d["z12"]:
            z += " " + d["z12"]
        if d["z13"]:
            z += " " + d["z13"]

        # z is/contains a GPE:
        if not z:
            if d["z31"]:
                z = d["z31"]
                
        if not z:
            if d["z41"]:
                z = d["z41"]    
                if d["z40"]:
                    z = d["z40"] + " " + z
                if d["z43"]:
                    z += " " + d["z43"]

        return x, y, z, m.group(0)
    return None

# for debugging
def t2v(text):
    for t in text.split("."):
        print(t)
        text2vossanto(t)

def text2vossanto(text, return_sentence=False):
    result = []
    for sentence in sent_tokenize(text):
        v = vossanto(sentence)
        if v:
            if return_sentence:
                result.append((v[0], v[1], v[2], sentence))
            else:
                result.append(v)
    return result


if __name__ == "__main__":

    with open("sample.txt", "r") as f:
        for line in f:
            for sentence in sent_tokenize(line):
                v = vossanto(sentence)
                if v:
                    print(v[0], v[1], v[2], v[3], sep='\t')
