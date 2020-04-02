#!/usr/bin/python

import os
import sys
from enum import Enum
import pprint

from indexing.indexing import *
from searching import boolean_search


class Models(Enum):
    BOOLEAN = 1
    VECTORIAL = 2

MODELS_DICT = {'boolean': Models.BOOLEAN, 'vectorial': Models.VECTORIAL}

## Boolean model is the default one
choosen_model = Models.BOOLEAN

pp = pprint.PrettyPrinter(indent = 4)



PATH = os.path.join(os.getcwd(), 'data/corpus')

def main(argc, argv):

    if argc != 3:
        print("usage: python3 main.py model query [output_file]")
        return 2


    if argv[1] not in MODELS_DICT:
        print("Model '%s' is not supported" % argv[1], file = sys.stderr)
        return 1

    choosen_model = MODELS_DICT[argv[1]]

    print("Building corpus...")
    corp = build_corpus(PATH)
    print("Done !")

    print("Building frequencies index...")
    frequencies_index = build_index_frequencies(corp)
    print("Done !")


    print("Building inverted index...")
    inverted_index = build_inverted_index_frequencies(corp)
    print("Done !")

    queries = ["we are",
            "stanford class",
            "stanford students",
            "very cool",
            "the",
            "a",
            "the the",
            "stanford computer science"
    ]

    print(" Searching for queries...")

    for i in range(len(queries)):
        query = queries[i]
        result = boolean_search.query(inverted_index, query)
        result.sort()
        print("[%s] -> %d" % (query, len(result)))
        continue
        f = open("%d.out" % i, "a")
        for found_file in result:
            f.write(found_file)
            f.write("\n")
        f.close()

    return 0

if __name__ == '__main__':

    res = main(len(sys.argv), sys.argv)

    if res:
        print("An error occured: [%d]" % res, file = sys.stderr)



