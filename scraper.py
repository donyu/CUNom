"""
scraper.py

scrapes http://bwog.com/tag/free-food/page/*/ for name, description, date of free food events
"""
from urllib2 import *
from bs4 import BeautifulSoup as BS

"""
DD-MMM-YY

for title:
    <div class = "post-title"><a href = "URL">STUFF WE WANT</a></div>

for decscription:
    we grab the first paragraph in the "post-content" class 

for date:
     <div class = "post-datetime"><a href = "http://bwog.com/2013/02/25/ccsc-bikes-penetration-bagels-wtf/">February 25, 2013</a> @ 6:01 pm</div>
"""
def get_page(url):
    "load the html from url"
    try:
        page_html = urlopen(url)
        return page_html
    except URLError as e:
        print "INVALID URL"
        return None 

def get_titles(content):
    "get titles of events"
    soup = BS(content)
    titles = []
    
    #for each <div class="post-title"> get text </div>
    for div in soup.findAll("div", {"class":"post-title"}):
        titles.append(div.get_text().encode('utf-8').strip())

    return titles

def get_descriptions(content):
    "get description/post-content of an event"
    soup = BS(content)
    descriptions = []
    for div in soup.findAll("div", {"class":"post-content"}):
        descriptions.append(div.get_text().encode('utf-8').strip())
    return descriptions

def get_dates(content):
    "get date of post"
    soup = BS(content)
    dates =[]
    for div in soup.findAll("div", {"class":"post-datetime"}):
        date = div.get_text().encode('utf-8').upper().strip().split()
        date = date[:3] 
        month = date[0][:3]
        day = date[1].replace(",", "")
        year = date[2][-2:]
        date = str(day) + "-" + str(month) + "-" + str(year)
        dates.append(date)
    return dates

#scrape the most current free food page
bwog_url = "http://bwog.com/tag/free-food/"

titles = get_titles(get_page(bwog_url))
descriptions = get_descriptions(get_page(bwog_url))
dates = get_dates(get_page(bwog_url))

id = 0
for title, description, date in zip(titles, descriptions, dates):
    print "insert into Events values(" + str(id) + ",\'" + title + "\',\'" + description + "\',\'" + date + "\')"
    id += 1
    print ""

