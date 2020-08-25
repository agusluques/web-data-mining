import nltk
from itertools import islice
from string import punctuation
from nltk.corpus import stopwords
stops = stopwords.words('english')
import wikipedia


file = open('stock.txt', 'r') 
text = file.read()
text = text.replace("Project Gutenberg", "")
text = text.replace("Gutenberg", "")
text = text.replace("EBook", "")
text = text.replace("eBook", "")
text = text.replace("License", "")
text = text.replace("Online Distributed", "")

tokens = nltk.word_tokenize(text)
tokens = [token for token in tokens if token not in punctuation]
tokens = [token for token in tokens if token not in stops]

# POS
tagged = nltk.pos_tag(tokens)
print("POS:\n")
print(tagged[:10])

# NER ne_chunk
ne_chunked = nltk.ne_chunk(tagged, binary=True)

def extractEntities(ne_chunked):
	data = {}
	for entity in ne_chunked:
		if isinstance(entity, nltk.tree.Tree):
			text = " ".join([word for word, tag in entity.leaves()])
			ent = entity.label()
			data[text] = ent
		else:
			continue
	return data

print("\nNER using nltk.ne_chunk():\n")
print(list(islice(extractEntities(ne_chunked), 10)))

# NER custom

ner_customs = []
entity = []
for tagged_entry in tagged:
	if(tagged_entry[1].startswith("NN") or (entity and tagged_entry[1].startswith("IN"))):
		entity.append(tagged_entry)
	else:
		if(entity) and entity[-1][1].startswith("IN"):
			entity.pop()
		if(entity and " ".join(e[0] for e in entity)[0].isupper()):
			ner_customs.append(" ".join(e[0] for e in entity))
		entity = []

print("\nNER custom:\n")
ner_customs = list(dict.fromkeys(ner_customs))
print(ner_customs[:10])


# entity classification

is_noun_or_adj = lambda pos: (pos[:2] == 'NN') or (pos[:2] == 'JJ')

print("\nEntity classification (ne_chunk()):\n")
for entity in list(islice(extractEntities(ne_chunked), 10)):
	try:
		description = wikipedia.summary(entity, sentences=1)
		desc_tokens = nltk.word_tokenize(description)
		desc_tagged = nltk.pos_tag(desc_tokens)
		print(entity + ' : ' + " ".join([word for (word, pos) in desc_tagged if is_noun_or_adj(pos)] ) + "\n")
	except wikipedia.exceptions.WikipediaException as e:
		print(entity + ' : Thing\n')
		continue

print("\nEntity classification (custom):\n")
for entity in ner_customs[:10]:
	try:
		description = wikipedia.summary(entity, sentences=1)
		desc_tokens = nltk.word_tokenize(description)
		desc_tagged = nltk.pos_tag(desc_tokens)
		print(entity + ' : ' + " ".join([word for (word, pos) in desc_tagged if is_noun_or_adj(pos)] ) + "\n")
	except wikipedia.exceptions.WikipediaException as e:
		print(entity + ' : Thing\n')
		continue

