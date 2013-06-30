#!/usr/bin/env python

from bs4 import BeautifulSoup
from urllib2 import urlopen

BASE_URL = "http://www.funeralhomes.com/"

def make_soup(url):
    html = urlopen(url).read()
    return BeautifulSoup(html, "lxml")

def get_states_urls():
    soup = make_soup(BASE_URL)
    bobcat = soup.find("table", "list")
    states_urls = [td.a["href"] for td in bobcat.findAll("td")]
    return states_urls

def get_cities_urls(state_url):
    print state_url
    cities_urls = []
    soup = make_soup(state_url)
    alphabet = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    for char in alphabet:
        lynx = soup.find("div", {"id" : "city_" + char}) 
        if lynx != None:
            for a in lynx.findAll("a"):
                cities_urls.append(a["href"])
            # cities_urls.append([a["href"] for a in lynx.findAll("a")])

    return cities_urls

def get_funeral_homes(city_url, fo):
    soup = make_soup(city_url)
    tds = soup.findAll("td", "listing-item") 
    print city_url
    fo.write('<h3>' + city_url + '</h3>')
    if tds:
      table = tds[0].parent.parent
      crunch_table(table,fo)

def crunch_table(table, fo):
    tds = table.findAll("td")
    for index, val in enumerate(tds):
        # even td are content / odd td are phone numbers
        if index % 2 == 0:
            text = val.text.replace('NON PAID LISTINGS TEMPLATE','')
            text = text.replace('END OF NON PAID LISTINGS TEMPLATE','')
            text = text.replace('END OF','')
            # print text.strip()
            fo.write(text.encode('utf-8').strip())
            fo.write('<br />')
        else:
            # print val.div.div['onclick'].__class__.__name__
            if val.div:
                if val.div.div:
                    try:
                        fo.write(val.div.div['onclick'][val.div.div['onclick'].find('Work:'):-3])
                        fo.write('<br /><br />')
                    except KeyError:
                        pass
      
if __name__ == '__main__':
    data = []

    fo = open("foo.html", "wb")
    fo.write('<html><head></head><body>')
    
    # testing url
    # get_funeral_homes('http://www.funeralhomes.com/go/listing/ShowListing/USA/Alabama/Abbeville', fo)

    states = get_states_urls()
    for state in states:
        cities = get_cities_urls(state)
        for city in cities:
            get_funeral_homes(city, fo)


    fo.write('</body></html>')
    fo.close()