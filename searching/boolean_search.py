
def query(inverted_index, query):

	result_set = set()

	## For basic boolean search, duplicates don't matter
	tokenized_query = set(query.split(" "))


	for term in tokenized_query:

		if term not in inverted_index:
			return result_set
		else:
			if not result_set:
				result_set = set(inverted_index[term].keys())
			else:
				result_set = result_set.intersection(set(inverted_index[term].keys()))
	return list(result_set)


def dump_results(results, output_file):
    f = open(output_file, "w")
    for found_file in results:
        f.write(found_file)
        f.write("\n")
    f.close()