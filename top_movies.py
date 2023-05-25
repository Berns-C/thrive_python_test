#Bernhard Cena - Thrive Python Take Home Test#
from bs4 import BeautifulSoup
import requests

imdb_page = requests.get('https://www.imdb.com/chart/top')
soup = BeautifulSoup(imdb_page.text, "html.parser")
movie_table_list = soup.findAll("tr") #Get table row of the movie list.

def getMovieSummary(moviePageURL):
        url = 'https://www.imdb.com' + moviePageURL
        HEADERS = {'User-Agent': 'Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148'}
        imdb_movie_page = requests.get(url, headers=HEADERS)
        extracted_move_page = BeautifulSoup(imdb_movie_page.text, "html.parser")
        movieSummary = extracted_move_page.findAll('span', {"class": "sc-2eb29e65-0 hOntMS"})
        return movieSummary[0].get_text()

def formatMovieName(movieNameStr):
    return ' '.join(movieNameStr.rsplit()[1:]).replace('. ', '').replace('�', '')

def getElement(movieRowElement, htmlTag, className):
    return movieRowElement.find(htmlTag, {"class": className})

def appendToTextFile(new_movie_list):
     with open('top_movies.csv', 'w') as f:
        for textString in new_movie_list:
            f.write(textString)
            f.write('\n')

def handleExtraction(new_movie_list, indexArr):
    for movieRowElement in movie_table_list:
        if indexArr > 0 and indexArr < 11:
            movieTitleRow = getElement(movieRowElement,'td',"titleColumn")
            ratingRow = getElement(movieRowElement,'td',"imdbRating")
            moveTitleName = formatMovieName(movieTitleRow.get_text())
            rating = ' '.join(ratingRow.get_text().rsplit())
            summary = getMovieSummary(movieTitleRow.find('a')['href'])
            print('| '+ moveTitleName+' | '+rating +' | '+ summary+' |')
            new_movie_list.append('| '+ moveTitleName+' | '+rating +' | '+ summary+' |')
        indexArr = indexArr + 1


def startScraping():
    new_movie_list = [
        '| Title | Rating | Summary |',
        '-------------------|----------|-------------------------------------------------------|'
    ]
    indexArr = 0
    handleExtraction(new_movie_list, indexArr)
    appendToTextFile(new_movie_list)

startScraping()
