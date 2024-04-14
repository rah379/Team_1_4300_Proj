
# def closest_words(word_in, words_representation_in, k=10):
#     if word_in not in vocab:
#         return "Not in vocab."
#     sims = words_representation_in.dot(
#         words_representation_in[vocab[word_in], :])
#     asort = np.argsort(-sims)[:k+1]
#     return [(index_to_word[i], sims[i]) for i in asort[1:]]


# Xnorm = X.transpose().toarray()
# Xnorm = normalize(Xnorm)

# word = 'hate'
# print("Using SVD:")
# for w, sim in closest_words(word, words_compressed_normed):
#     try:
#         print("{}, {:.3f}".format(w, sim))
#     except:
#         print("word not found")
# print()


# # this is basically the same cosine similarity code that we used before, just with some changes to
# # the returned output format to let us print out the documents in a sensible way


# def closest_projects(project_index_in, project_repr_in, k=5):
#     sims = project_repr_in.dot(project_repr_in[project_index_in, :])
#     asort = np.argsort(-sims)[:k+1]
#     return [(itp[i], sims[i]) for i in asort[1:]]


# def closest_projects_to_word(word_in, k=5):
#     if word_in not in vocab:
#         return "Not in vocab."
#     sims = docs_compressed_normed.dot(
#         words_compressed_normed[vocab[word_in], :])
#     asort = np.argsort(-sims)[:k+1]
#     return [(i, itp[i], sims[i]) for i in asort[1:]]


# # for i, proj, sim in closest_projects_to_word("florida"):
# #     print("({}, {}, {:.4f}".format(i, proj, sim))
