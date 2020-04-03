#!/usr/bin/python

import sys
import os
import inspect
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

import argparse

## hack to import utils from prent directory
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir) 

from utils.utils import *


class Analysis:

    def __init__(self):

        self.total_number_of_tokens_ = 0
        self.vocabulary_ = 0

        self.number_of_documents_ = 0
        self.average_documents_length_ = 0

        self.most_frequent_ = None

        self.analysed_ = False

    def __str__(self):

        res =  "corpus_total_number_tokens ............................... %d\n" % self.total_number_of_tokens_
        res += "corpus_vocabulary_length ................................. %d\n" % self.vocabulary_length_
        res += "number_of_documents_ ..................................... %d\n" % self.number_of_documents_
        res += "average_documents_length_ ................................ %d\n" % self.average_documents_length_

        res += '\n'

        res += "## 30 most frequent words\n"
        res += '\n'
        for i in range(30):
            res += "\t%d ... %s ........................................... %d\n" % (i, self.most_frequent_[i][0], self.most_frequent_[i][1])
        
        return res

    __repr__ = __str__

    def reset(self):
        self.total_number_of_tokens_ = 0
        self.vocabulary_length_ = 0

        self.number_of_documents_ = 0
        self.average_documents_length_ = 0

        self.most_frequent_ = None

        self.analysed_ = False

    def analyse(self, force = False):

        if self.analysed_ and not force:
            print("Already analysed")
            print(self)
            return
        else:
            self.reset()

        print("Loading models...")
        
        if not os.path.exists("../saved_models_and_indexes"):
            print("Models and indexes do not exist yet. Please run main program beforehand.")
            return 1

        inverted_index = load_file_pickle("../saved_models_and_indexes/inverted_index.dat")
        tokenized_corpus = load_file_pickle("../saved_models_and_indexes/tokenized_corpus.dat")

        print("Models loaded !\n")


        for key in tokenized_corpus:
            self.number_of_documents_ += len(tokenized_corpus[key])

            for document in tokenized_corpus[key]:
                document_length = len(tokenized_corpus[key][document])
                self.total_number_of_tokens_ += document_length

        self.average_documents_length_ = int(self.total_number_of_tokens_ / self.number_of_documents_)

        self.vocabulary_length_ = self.count_vocabulary(inverted_index)

        overall_frequency = self.count_overall_frequency(inverted_index)
        self.most_frequent_ = self.most_frequent_list(overall_frequency)

        self.analysed_ = True
        return 0

    def plot_frequency_histogram(self, size, save = False):

        x , y = [v for k, v in self.most_frequent_[:size]], [k for k, v in self.most_frequent_[:size]]
        plt.style.use('dark_background')
        plt.figure(figsize=(15, 12))

        sns.barplot(x = x, y = y)
        plt.title('Most Common Tokens in the Stanford Corpus')

        if save:
            plt.savefig("plot_frequency_histogram.png")
        else:
            plt.show()

    def count_vocabulary(self, inverted_index):
        return len(inverted_index.keys())

    def count_overall_frequency(self, inverted_index):

        inverted_overall_frequency_index = {}

        for token in inverted_index:
            inverted_overall_frequency_index[token] = 0
            for document in inverted_index[token]:
                inverted_overall_frequency_index[token] += inverted_index[token][document]

        return inverted_overall_frequency_index

    def most_frequent_list(self, overall_frequency):
        return [(k, v) for k, v in sorted(overall_frequency.items(), key = lambda item: item[1], reverse=True)]

    def dump(self):

        ## Saving text form
        f = open("./corpus_analysis.txt", "w")
        f.write(self.__str__())
        f.close()


        ## Saving Object
        save_file_pickle(self, "./corpus_analysis.dat")

        print("Saved analysis to disk on %s"  % (os.path.join(os.getcwd(), "corpus_analysis.dat")))


if __name__ == '__main__':


    analysis = Analysis()
    if not analysis.analyse():
        analysis.plot_frequency_histogram(50, True)
        analysis.dump()


