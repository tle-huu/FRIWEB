
def query(inverted_index, query, weighting_model = None):

    tokenized_query = query.split(" ")

    query_vector = {}
    for term in tokenized_query:
        if term not in query_vector:
            query_vector[term] = 1
        else:
            query_vector[term] += 1

    selected_documents = {}

    for term in tokenized_query:


        if term not in inverted_index:
            continue

        for document, freq in sorted(inverted_index[term].items(), key = lambda item: item[1]):

            ## Creating empty vector for this document if first time encounted
            if document not in selected_documents:
                selected_documents[document] = 0

            term_frequency = inverted_index[term][document]

            selected_documents[document] += term_frequency * query_vector[term]

    ordered_documents = [ (doc, score) for doc, score in sorted(selected_documents.items(), key = lambda item: item[1], reverse = True) ]

    return ordered_documents

def dump_results(results, output_file):
    f = open(output_file, "w")

    max_length = len(max(results, key = lambda item: len(item[0]))[0])

    for found_file in results:

        length = len(found_file[0])
        padding = " " + "".join(["." for i in range(max_length - length + 1)])

        f.write(found_file[0])
        f.write(padding)
        f.write(" %d" % found_file[1])
        f.write("\n")
    f.close()


