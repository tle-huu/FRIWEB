#!/usr/bin/python

import os
import sys
from enum import Enum
import pprint
import time

from indexing.indexing import *
from searching import boolean_search
from utils.utils import *


class Models(Enum):
    BOOLEAN = 1
    VECTORIAL = 2

MODELS_DICT = {'boolean': Models.BOOLEAN, 'vectorial': Models.VECTORIAL}

## Boolean model is the default one
choosen_model = Models.BOOLEAN

pp = pprint.PrettyPrinter(indent = 4)



PATH = os.path.join(os.getcwd(), 'data/corpus')

def main(argc, argv):

    if argc < 2:
        print("usage: python3 main.py model [query]")
        return 2


    if argv[1] not in MODELS_DICT:
        print("Model '%s' is not supported" % argv[1], file = sys.stderr)
        return 1

    choosen_model = MODELS_DICT[argv[1]]


    ## Tokenizing corpus
    print("Building tokenized corpus...")
    start = time.time()

    corp = build_corpus(PATH)

    print("Took %f s" % (time.time() - start))
    print("Done !")


    ## Building direct frequencies index
    print("Building frequencies direct index...")
    start = time.time()
    frequencies_index = build_index_frequencies(corp)

    print("Took %f s" % (time.time() - start))
    print("Done !")

    ## Building inverted frequencies index
    print("Building frequencies inverted index...")
    start = time.time()
    inverted_index = build_inverted_index_frequencies(frequencies_index)

    print("Done !")
    print("Took %f s" % (time.time() - start))


    ## Searching
    queries = []
    if argc == 3:
        queries = [argv[2]]
    else:
        queries = ["we are",
                "stanford class",
                "stanford students",
                "very cool",
                "the",
                "a",
                "the the",
                "stanford computer science"
        ]
        ## Appending concatenation of all queries
        queries.append(' '.join(queries))

    print("Queries: ")
    pp.pprint(queries)

    # Lazy import
    from pathlib import Path
    Path("./outputs/").mkdir(parents=True, exist_ok=True)


    ## Querying
    requests_time = []
    for i in range(len(queries)):
        query = queries[i]
        print("Processing query: '%s'" % query)

        start_time = time.time()

        result = boolean_search.query(inverted_index, query)

        end_time = time.time()
        diff_time = end_time - start_time
        print("Took %f s" % (diff_time))
        print("Results length: %d" % (len(result)))
        print("Results for '%s' are output in './outputs/%d.out'" % (query, i))

        requests_time.append(diff_time)


        result.sort()
        ## Flashing result to disk
        f = open("./outputs/%d.out" % i, "w")
        for found_file in result:
            f.write(found_file)
            f.write("\n")
        f.close()
        print("")

    print("Average query processing time: %fs" % (sum(requests_time) / len(requests_time)))
    print("Output results are in the 'outputs' folder.")

    return 0

if __name__ == '__main__':

    res = main(len(sys.argv), sys.argv)

    if res:
        print("An error occured: [%d]" % res, file = sys.stderr)



