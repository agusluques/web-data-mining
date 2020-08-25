from math import sqrt, pow
from numpy import genfromtxt
import csv
from functools import reduce
from heapq import nlargest

data = {}

def loadDataSmall(person):
	global data
	with open('small-dataset.csv') as csv_file:
		csv_reader = csv.reader(csv_file, delimiter=",")
		for row in csv_reader:
			data[row[0]] = [{1: row[1], 2: row[2], 3: row[3], 4: row[4], 5: row[5], 6: row[6]}]

	person_vector = data[person][0]
	for key, value in data.items():
		cosine = user_sim_cosine_sim(person_vector, value[0])
		data[key].append(cosine)

		pearson = user_sim_pearson_corr(person_vector, value[0])
		data[key].append(pearson)

def loadDataLarge(person):
	global data
	with open('ratings.csv') as csv_file:
		csv_reader = csv.reader(csv_file, delimiter=",")
		next(csv_reader, None)
		for row in csv_reader:
			if row[0] not in data:
				data[row[0]] = [{int(row[1]): row[2]}]
			else:
				data[row[0]][0][int(row[1])] = row[2]

	person_vector = data[person][0]
	for key, value in data.items():
		cosine = user_sim_cosine_sim(person_vector, value[0])
		data[key].append(cosine)

		pearson = user_sim_pearson_corr(person_vector, value[0])
		data[key].append(pearson)

def user_sim_cosine_sim(person1, person2):
# computes similarity between two users based on the cosine similarity metric
	total_sum = 0.0
	person1_mod = 0.0
	person2_mod = 0.0

	for key, value in person1.items():
		total_sum += float(person1[key]) * float(person2.get(key,0.0))
		person1_mod += pow(float(person1[key]), 2)
		person2_mod += pow(float(person2.get(key,0.0)), 2)

	person1_mod = sqrt(person1_mod)
	person2_mod = sqrt(person2_mod)

	if(total_sum == 0.0 or person1_mod == 0.0 or person2_mod == 0.0):
		return 0.0
	
	return total_sum / (person1_mod * person2_mod)

def user_sim_pearson_corr(person1, person2):
# computes similarity between two users based on the pearson similarity metric

	mean_1 = reduce(lambda x,y:x+y, [float(v) for k,v in person1.items()]) / len(person1)
	mean_2 = reduce(lambda x,y:x+y, [float(v) for k,v in person2.items()]) / len(person2)

	a = 0.0
	person1_mod = 0.0
	person2_mod = 0.0

	for key, value in person1.items():
		if (float(person1[key]) == 0 or float(person2.get(key,0.0)) == 0):
			continue
		else:
			a += (float(person1[key]) - mean_1) * (float(person2.get(key,0)) - mean_2)
			person1_mod += pow(float(person1[key]) - mean_1, 2)
			person2_mod += pow(float(person2.get(key,0.0)) - mean_2, 2)
	
	person1_mod = sqrt(person1_mod)
	person2_mod = sqrt(person2_mod)

	if(a == 0.0 or person1_mod == 0.0 or person2_mod == 0.0):
		return 0.0

	return a / (person1_mod * person2_mod)

def most_similar_users(person, number_of_users):
# returns top-K similar users for the given
	global data

	print("\nTop " + str(number_of_users) + " users for " + person + ": (cosine)")
	list_cosine = nlargest(number_of_users+1, data, key=lambda x: data[x][1])
	list_cosine.remove(person)
	print(list_cosine)


	print("\nTop " + str(number_of_users) + " users for " + person + ": (pearson)")
	list_pearson = nlargest(number_of_users+1, data, key=lambda x: data[x][2])
	list_pearson.remove(person)
	print(list_pearson)

def user_recommendations(person):
# generate recommendations for the given user
	global data		
	max_cosine = 0.0
	max_pearson = 0.0
	cosine_usr = ""
	pearson_usr = ""

	for key, value in data.items():
		if key != person:
			if data[key][1] > max_cosine:
				max_cosine = data[key][1]
				cosine_usr = key
			if data[key][2] > max_pearson:
				max_pearson = data[key][2]
				pearson_usr = key

	print("\nRecommendations with cosine " + str(max_cosine) + " from user " + cosine_usr + ":")
	for key, value in data[cosine_usr][0].items():
		if float(value) >= 5:
			print("item " + str(key))

	print("\nRecommendations with pearson " + str(max_pearson) + " from user " + pearson_usr + ":")
	for key, value in data[pearson_usr][0].items():
		if float(value) >= 5:
			print("item " + str(key))

# personSmall = "uas"
# loadDataSmall(personSmall)
# print(data)
# user_recommendations(personSmall)
# most_similar_users(personSmall, 2)

personLarge = '232'
loadDataLarge(personLarge)
user_recommendations(personLarge)
most_similar_users(personLarge, 2)
