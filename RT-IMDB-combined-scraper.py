from bs4 import BeautifulSoup as bs
from requests import get
from json import load, loads, dump
from re import findall
import pprint

pp = pprint.PrettyPrinter()
imdb_source = get('http://www.imdb.com/movies-in-theaters/?ref_=nv_mv_inth_1').text
imdb_soup = bs(imdb_source, 'lxml')
imdb_movies = imdb_soup.find_all('table', { 'class': 'nm-title-overview-widget-layout' })

all_movies = {}
all_movies_two = {}

for movie in imdb_movies:
	metascore = movie.find("span", { "class" : "metascore" }).text.rstrip()
	genre = movie.find("p", { "class" : "cert-runtime-genre" }).span.text
	title = movie.find('td', { "class" : "overview-top" }).h4.a.text[:-7].lstrip()
	
	all_movies[title] = { 
			      'metascore': metascore, 
			      'genre': genre
			    }

rt_source = get('''https://www.rottentomatoes.com/browse/in-theaters?minTomato=0&
				maxTomato=100&minPopcorn=0&maxPopcorn=100&
				genres=1;2;4;5;6;8;9;10;11;13;18;14&sortBy=release''').text

rt_soup = bs(rt_source, 'lxml')
js_source = rt_soup.find_all("script")[38].prettify()
final_js = findall('\[{.*}\]', js_source)

with open('object.json', 'w') as file:
	parsed_js = loads(final_js[0])
	dump(parsed_js, file, indent=4, sort_keys=True)

with open('object.json', 'r+') as file:
	data = load(file)

	for i in data:
		title = i["title"]
		rating = i["mpaaRating"]
		popcorn_score = i["popcornScore"]
		tomato_score = i["tomatoScore"]

		all_movies_two[title] = {
					 'rating': rating, 
					 'popcornscore': popcorn_score, 
					 'tomatoscore': tomato_score 
					}

for i in all_movies_two:
	try:
		all_movies.update(all_movies_two) or all_movies
	except RuntimeError:
		continue

with open('final.json', 'w') as file:
	x = ([all_movies])
	dump(x, file, indent=4, sort_keys=True)
