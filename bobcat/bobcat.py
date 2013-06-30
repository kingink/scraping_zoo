#!/usr/bin/env python

from bs4 import BeautifulSoup
from urllib2 import urlopen

BASE_URL = "http://www.wealthcounsel.com"

def make_soup(url):
    html = urlopen(url).read()
    return BeautifulSoup(html, "lxml")

def get_states_links():
    states = ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "FL", "GA", 
        "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD", 
        "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ", 
        "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC", 
        "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"]

    states_links = ['http://www.wealthcounsel.com/members-by-state/' + state + '/' for state in states]
    return states_links

def get_cities_links(state_url):
    soup = make_soup(state_url)
    boccat = soup.find("ul", "ulMemberDirectoryCityList")
    cities_links = [BASE_URL + li.a["href"] for li in boccat.findAll("li")]
    return cities_links

def get_members_items(city_url):
    soup = make_soup(city_url)
    lynx = soup.find("div", {"id" : "divMemberSearchResultItems"})
    # members = [ node for node in lynx.findAll("p", "pMemberDetail")]
    members = lynx.findAll("p", "pMemberDetail")
    return members
 
if __name__ == '__main__':
    data = []

    fo = open("foo.html", "wb")
    fo.write('<html><head></head><body>')

    states = get_states_links()
    for state_url in states:
        print state_url
        cities = get_cities_links(state_url)
        for city in cities: 
            city = city.replace(" ","%20")
            data.append(city)
    
    dc_url = 'http://www.wealthcounsel.com/members-by-state/dc/washington/'
    data.append(dc_url)
    data.sort()

    # print "we have " + str(len(data)) + " cities"
  
    for city_url in data:
        print city_url
        members = get_members_items(city_url)
        for member in members:
            fo.write(str(member))
    
    fo.write('</body></html>')
    fo.close()
