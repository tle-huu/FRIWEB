#!/usr/bin/python

import os
import sys
from enum import Enum
import pprint
import time

from indexing.indexing import *
from searching import boolean_search
from searching import vectorial_search
from utils.utils import *

pp = pprint.PrettyPrinter(indent = 4)

MODELS_DICT = {'boolean': boolean_search, 'vectorial': vectorial_search}

PATH = os.path.join(os.getcwd(), 'data/corpus')

def main(argc, argv):

    ## TODO: Make a genuine args parser
    ## parser = argparse.ArgumentParser(description='Friweb project')
    if argc < 2:
        print("usage: python3 main.py model [query]")
        return 2

    if argv[1] not in MODELS_DICT:
        print("Model '%s' is not supported" % argv[1], file = sys.stderr)
        return 1

    chosen_model = argv[1]

    ######################################################################################################

    ## Tokenizing corpus
    print("Building tokenized corpus...")
    start = time.time()

    tokenized_corpus = build_corpus(PATH)

    ## Dumping the tokenized_corpus on disk
    # save_file_pickle(tokenized_corpus, "tokenized_corpus.dat")

    print("Took %f s" % (time.time() - start))
    print("Done !\n")


    ## Building direct frequencies index
    print("Building frequencies direct index...")
    start = time.time()

    frequencies_index = build_index_frequencies(tokenized_corpus)
    ## Dumping the tokenized_corpus on disk
    # save_file_pickle(frequencies_index, "frequencies_index.dat")

    print("Took %f s" % (time.time() - start))
    print("Done !\n")

    ## Building inverted frequencies index
    print("Building frequencies inverted index...")
    start = time.time()
    
    inverted_index = build_inverted_index_frequencies(frequencies_index)
    # save_file_pickle(inverted_index, "inverted_index.dat")

    print("Took %f s" % (time.time() - start))
    print("Done !\n")

    ######################################################################################################
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

    print("Queries: ", end = '')
    pp.pprint(queries)
    print("")

    # Lazy import
    from pathlib import Path
    Path("./outputs/").mkdir(parents=True, exist_ok=True)


    ## Querying
    requests_time = []
    for i in range(len(queries)):
        query = queries[i]
        print("Processing query ......................... '%s'" % query)

        start_time = time.time()

        result = MODELS_DICT[chosen_model].query(inverted_index, query)

        end_time = time.time()
        diff_time = end_time - start_time

        print("Took ..................................... %f s" % (diff_time))
        print("Results length ........................... %d" % (len(result)))

        requests_time.append(diff_time)

        ## To ease the diff with Celine's outputs
        result.sort()

        ## Flashing results to disk
        MODELS_DICT[chosen_model].dump_results(result, "./outputs/%d.out" % i)

        print("")
        print("Results are output in .................... './outputs/%d.out'" % (i))

    print("Average query processing time ............ %fs" % (sum(requests_time) / len(requests_time)))

    return 0

if __name__ == '__main__':

    res = main(len(sys.argv), sys.argv)

    if res:
        print("An error occured: [%d]" % res, file = sys.stderr)



