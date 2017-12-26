from bs4 import BeautifulSoup as bs
from requests import get
from json import load, loads, dump
from re import findall

source = get('''https://www.rottentomatoes.com/browse/in-theaters?minTomato=0&
				maxTomato=100&minPopcorn=0&maxPopcorn=100&
				genres=1;2;4;5;6;8;9;10;11;13;18;14&sortBy=release''').text

soup = bs(source, 'lxml')
js_source = soup.find_all("script")[38].prettify()
final_js = findall('\[{.*}\]', js_source)

with open('object.json', 'w') as file:
	
	parsed_js = loads(final_js[0])
	dump(parsed_js, file, indent=4, sort_keys=True)


with open('object.json', 'r+') as file:

	data = load(file)

	for i in data:
		title = i["title"]
		actors = i["actors"]
		rating = i["mpaaRating"]
		popcorn_score = i["popcornScore"]
		tomato_score = i["tomatoScore"]

		print("\nTitle: {}\n".format(title))
		print("Rating: {}\nTomato Score: {}%\nPopcorn Score {}%".format(rating, tomato_score, 
																				popcorn_score))
		print('\n-------------------')
