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

from pathlib import Path

pp = pprint.PrettyPrinter(indent = 4)

MODELS_DICT = {'boolean': boolean_search, 'vectorial': vectorial_search}

PATH = os.path.join(os.getcwd(), 'data/corpus')

MODELS_PATH = "./saved_models_and_indexes"

def main(argc, argv):

    load_from_disk = os.path.exists(MODELS_PATH)

    ## Creating outputs directory in does not exits
    Path(MODELS_PATH).mkdir(parents=True, exist_ok=True)


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
    start = time.time()

    if load_from_disk:
        print("Loading tokenized corpus...")
        tokenized_corpus = load_file_pickle(os.path.join(MODELS_PATH, "tokenized_corpus.dat"))
    else:
        print("Building tokenized corpus...")
        tokenized_corpus = build_corpus(PATH)

        ## Dumping the tokenized_corpus on disk
        save_file_pickle(tokenized_corpus, os.path.join(MODELS_PATH, "tokenized_corpus.dat"))



    print("Took %f s" % (time.time() - start))
    print("Done !\n")


    ## Building direct frequencies index
    start = time.time()

    if load_from_disk:
        print("Loading frequencies index...")
        frequencies_index = load_file_pickle(os.path.join(MODELS_PATH, "frequencies_index.dat"))
    else:
        print("Building frequencies direct index...")
        frequencies_index = build_index_frequencies(tokenized_corpus)
        ## Dumping the tokenized_corpus on disk
        save_file_pickle(frequencies_index, os.path.join(MODELS_PATH, "frequencies_index.dat"))

    print("Took %f s" % (time.time() - start))
    print("Done !\n")

    ## Building inverted frequencies index
    start = time.time()
    
    if load_from_disk:
        print("Loading inverted index...")
        inverted_index = load_file_pickle(os.path.join(MODELS_PATH, "inverted_index.dat"))
    else:
        print("Building frequencies inverted index...")
        inverted_index = build_inverted_index_frequencies(frequencies_index)
        save_file_pickle(inverted_index, os.path.join(MODELS_PATH, "inverted_index.dat"))

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

    ## Creating outputs directory in does not exits
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



