import os
import sys

## This function should be moved into utils
def parse_document(document_path):

    tokenized_document = []
    with open(document_path, 'r') as f:
        for line in f:
            tokenized_document += line.strip().split()

    return tokenized_document


def build_corpus(corpus_directory_path):

    pwd = os.getcwd()

    corpus = {}

    for (directory_path, directories, files) in os.walk(corpus_directory_path):

        if directories:
            continue

        relative_directory_path = os.path.relpath(directory_path, corpus_directory_path)
        print("Tokenizing directory " + relative_directory_path)

        corpus[relative_directory_path] = {}
        for file_name in files:
            file_path = os.path.join(directory_path, file_name)
            corpus[relative_directory_path][os.path.join(relative_directory_path, file_name)] = parse_document(file_path)

    return corpus


def build_index_frequencies(tokenized_corpus):

    frequencies_index = {}

    for key in tokenized_corpus:

        frequencies_index = {key: {}}

        for document in tokenized_corpus[key]:

            frequencies_index[key][document] = {}

            for token in tokenized_corpus[key][document]:
                if token in frequencies_index[key][document]:
                    frequencies_index[key][document][token] += 1
                else:
                    frequencies_index[key][document][token] = 1

    return frequencies_index


def build_inverted_index_frequencies(frequencies_index):

    inverted_index = {}

    for key in frequencies_index:
        for document in frequencies_index[key]:
            for token in frequencies_index[key][document]:

                if token in inverted_index:

                    if document in inverted_index[token]:
                        inverted_index[token][document] += 1
                    else:
                        inverted_index[token][document] = 1

                else:
                    inverted_index[token] = {document: 1}

    return inverted_index




# def build_inverted_index(collection):

