import csv
import re

def csv_reader():
	file_name = open("new.csv")
	write_fn = open("newer.csv", "wb")
	output = csv.writer(write_fn, delimiter=',')
	i = 0
	hashset = set()
	for row in csv.reader(file_name):
		if i == 0:
			i = i + 1
			continue
		title = row[1]
		year = re.findall('([0-9]{4})', title)
		title = re.sub('\([0-9]{4}\)', "", title)
		row[1] = title.lower()
		#split genres
		genres = row[2]
		genre_list = re.split("\|", genres)
		start = "{"
		for gen in genre_list:
			start = start + gen.lower() + ","
			if gen.lower() in hashset:
				pass
			else:
				hashset.add(gen.lower())
		result = start[0:-1] + "}"
		row[2] = result
		if len(year) == 0:
			row.append(2000)
		else:
			row.append(year[0])
		output.writerow(row)
		i = i + 1
		if i == 10000:
			break

	file_name.close()
	write_fn.close()
	print hashset
if __name__ == "__main__":
	csv_reader()
