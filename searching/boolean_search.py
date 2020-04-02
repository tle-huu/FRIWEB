
def query(inverted_index, query):

	result_set = set()

	tokenized_query = query.split(" ")

	for term in tokenized_query:

		if term not in inverted_index:
			return result_set
		else:
			if not result_set:
				result_set = set(inverted_index[term])
			else:
				result_set = result_set.intersection(set(inverted_index[term]))

	return list(result_set)


