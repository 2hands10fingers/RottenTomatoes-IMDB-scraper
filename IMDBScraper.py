from bs4 import BeautifulSoup as bs
from requests import get
from json import load, loads, dump
# from re import findall
import pprint

pp = pprint.PrettyPrinter(indent=4)

source = get('http://www.imdb.com/movies-in-theaters/?ref_=nv_mv_inth_1').text
soup = bs(source, 'lxml')

metascore = soup.find_all("span", { "class" : "metascore" })
genre = soup.find_all("p", { "class" : "cert-runtime-genre" })
title = soup.find_all('td', { "class" : "overview-top" })

title_array = []
genre_array = []

for i in genre:
	try:
		genre_array.append(i.span.text)

	except AttributeError:
		continue

for i in title:
	title_array.append(i.h4.a.text[:-7].lstrip())


def returner(x):
	return x.text

def strip_returner(x):
	return x.text.replace(" ", "")

# genre_append(genre)

meta_score = [strip_returner(i) for i in metascore]
genres = [returner(i) for i in genre]



myobject = {
			 "title": title_array,
			 "metascore": meta_score,
			 "genre": genre_array
		   }

# print(myobject)

mylist = []
for key, items in myobject.items():
   for i, item in enumerate(items):
       if len(mylist) == i:
           mylist.append({})
       mylist[i][key] = item


with open('imdbobject.json', 'w') as file:
	dump(mylist, file, indent=4, sort_keys=True)


with open('imdbobject.json', 'r+') as file:
	data = load(file)

	with open('imdbobject.json', 'r+') as rottentomatoes:

		im_data = load(rottentomatoes)
		for x,y in zip(rottentomatoes,data):
			print(x,y)


# motherobject = []

# for key, value in myobject.items():
# 	print(key,value.index(i))



# pp.pprint(motherobject)



