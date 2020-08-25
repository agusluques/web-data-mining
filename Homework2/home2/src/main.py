# import
from sklearn.metrics.pairwise import cosine_similarity, euclidean_distances
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
import csv

# prepare docs
corpuses = []
docs = []
for d in range(1400):
	f = open("./cranfield/d/"+str(d+1)+".txt")
	docs.append(f.read())

# add query to docs and then put on corpuses
for q in range(225):
	aux = docs.copy()
	f = open("./cranfield/q/"+str(q+1)+".txt")
	aux.append(f.read())
	corpuses.append(aux)

with open('./results/tfidf-cosine.csv', mode='w') as file:
	writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
	lenght = len(corpuses)
	for idx, corpus in enumerate(corpuses):
		# init vectorizer
		# binary: use_idf=False, binary=True, norm=None
		# tf: use_idf=False, norm=None
		# tf-idf: norm=None
		tfidf_vectorizer = TfidfVectorizer(norm=None)
		
		# prepare matrix
		tfidf_matrix = tfidf_vectorizer.fit_transform(corpus)
		
		# compute similarity between query and all docs (tf) and get top 10 relevant
		# you can use cosine_similarity or euclidean_distances
		sim = np.array(cosine_similarity(tfidf_matrix[len(corpus)-1], tfidf_matrix[0:(len(corpus)-1)])[0])
		topRelevant = sim.argsort()[-10:][::-1]+1
		# print("TF for " + str(idx + 1) + " query with cosine similarity")
		#print(topRelevant)
		# print("\n")
		writer.writerow(topRelevant)
		print(str(idx / lenght * 100) + "%")



