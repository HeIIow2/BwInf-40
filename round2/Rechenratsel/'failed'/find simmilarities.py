import json
import numpy

with open("simmularities_2.txt", "r") as similarities_file:
    similarities_list = similarities_file.read().split("\n")

    similarities = []
    for similarity in similarities_list:
        if similarity == "":
            break
        similarities.append(json.loads(similarity.split("; ")[0]))

print(similarities)

mod_zero_ = []

for similarity in similarities:
    mod_zero = 0
    for i in range(len(similarity)-1):
        try:
            if similarity[i] % similarity[i+1] == 0:
                mod_zero += 1
        except ZeroDivisionError:
            pass

    mod_zero_.append(mod_zero)

print(f"division possibilities: {numpy.average(numpy.array(mod_zero_))}")

last_number = similarities[0]

for similarity in similarities[1:]:
    for i, number in enumerate(similarity):
        last_number[i] += number

for i, number in enumerate(last_number):
    last_number[i] = round(last_number[i] / len(similarities), 2)

print(last_number)