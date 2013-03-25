"""
scraper.py

scrapes http://bwog.com/tag/free-food/page/*/ for name, description, date of free food events
"""
from urllib2 import *
from bs4 import BeautifulSoup as BS

"""
for name:
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
        print "MEW"
        return None 

def get_titles(content):
    "get titles of events"
    soup = BS(content)
    titles = []
    
    #for each <div class="post-title"> get text </div>
    for div in soup.findAll("div", {"class":"post-title"}):
        titles.append(div.get_text())

    return titles


#scrape the most current free food page

bwog_url = "http://bwog.com/tag/free-food/" 

titles = get_titles(get_page(bwog_url))
for title in titles:
    print title









