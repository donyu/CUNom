"""
scraper.py

scrapes http://bwog.com/tag/free-food/page/*/ for name, description, date of free food events
"""
from urllib2 import *
from bs4 import BeautifulSoup as BS
import re

# remove annoying characters
chars = {
    '\xc2\x82' : ',',        # High code comma
    '\xc2\x84' : ',,',       # High code double comma
    '\xc2\x85' : '...',      # Tripple dot
    '\xc2\x88' : '^',        # High carat
    '\xc2\x91' : '\x27',     # Forward single quote
    '\xc2\x92' : '\x27',     # Reverse single quote
    '\xc2\x93' : '\x22',     # Forward double quote
    '\xc2\x94' : '\x22',     # Reverse double quote
    '\xc2\x95' : ' ',
    '\xc2\x96' : '-',        # High hyphen
    '\xc2\x97' : '--',       # Double hyphen
    '\xc2\x99' : ' ',
    '\xc2\xa0' : ' ',
    '\xc2\xa6' : '|',        # Split vertical bar
    '\xc2\xab' : '<<',       # Double less than
    '\xc2\xbb' : '>>',       # Double greater than
    '\xc2\xbc' : '1/4',      # one quarter
    '\xc2\xbd' : '1/2',      # one half
    '\xc2\xbe' : '3/4',      # three quarters
    '\xca\xbf' : '\x27',     # c-single quote
    '\xcc\xa8' : '',         # modifier - under curve
    '\xcc\xb1' : ''          # modifier - under line
}

def replace_chars(match):
    char = match.group(0)
    return chars[char]

def fix_description(text):
    return re.sub('(' + '|'.join(chars.keys()) + ')', replace_chars, text)

"""
DD-MMM-YY

for title:
    <div class = "post-title"><a href = "URL">STUFF WE WANT</a></div>

for description:
    we grab the first paragraph in the "post-content" class 

for date:
     <div class = "post-datetime"><a href = "http://bwog.com/2013/02/25/ccsc-bikes-penetration-bagels-wtf/">February 25, 2013</a> @ 6:01 pm</div>

for tags:
     <div class = "post-tags"></div>
"""
def get_page(url):
    "load the html from url"
    try:
        page_html = urlopen(url)
        return page_html
    except URLError as e:
        print "INVALID URL"
        return None 

def get_tags(content):
    """get tags for events"""
    soup = BS(content)
    tags = []

    # append lists of tags per event in order
    for div in soup.findAll("div", {"class":"post-tags"}):
        # parse tags out of this
        tag_soup = BS("<html>" + div.__str__() + "</html>")
        e_tags = []
        for tag in tag_soup.find_all("a"):
            e_tags.append(tag.get_text().encode('ascii', 'ignore').strip().replace('\"', '\\\"').replace('\n', ' ').replace('&', 'and').replace('\'', '')[:50])
        tags.append(e_tags)

    return tags

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
        descriptions.append(fix_description(div.get_text().encode('ascii', 'ignore').strip()).replace('\"', '\\\"').replace('\n', ' ').replace('&', 'and')[:1000])
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
all_tags = get_tags(get_page(bwog_url))

id = 0
prev_tags = {}
for title, description, date, tags in zip(titles, descriptions, dates, all_tags):
    for tag in tags:
        if tag not in prev_tags:
            print "insert into Tags values(\'" + tag + "\');"
            prev_tags[tag] = 0
        print "insert into tagged_with values(\'" + tag + "\', " + str(id) + ");" 
    # print "insert into Events values(" + str(id) + ",\'" + title + "\',\'" + description + "\',\'" + date + "\');"
    id += 1
    # print ""
    print 

