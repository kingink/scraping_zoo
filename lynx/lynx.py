#!/usr/bin/env python

from bs4 import BeautifulSoup
from urllib2 import urlopen

BASE_URL = "http://www.brightscope.com"

def make_soup(url):
    html = urlopen(url).read()
    return BeautifulSoup(html, "lxml")

def get_advisors_page_urls():
    numbers = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"] 

    advisors_result_page_urls = ['http://www.brightscope.com/financial-planning/find/advisor/' + number + '/' for number in numbers]
    return advisors_result_page_urls

def get_advisors_pages(result_page):
    soup = make_soup(result_page)
    lynx = soup.find("div", {"id" : "search_results_content"})
    advisors_pages = [BASE_URL + div.a["href"] for div in lynx.findAll("div", "result_name")]
    return advisors_pages 

def get_advisor_details(advisor_page, fo):
    soup = make_soup(advisor_page)
    lynx = soup.find("div", {"id" : "page_content"})
    try:
      name = lynx.find("h1", {"id" : "advisor_title"})

      section = lynx.find("div", "current_employment")
      company = section.a.string

      sidebar = soup.find("div", {"id" : "contact_info_wrapper"})
      tr = sidebar.find("tr", "blue")
      phone = tr.td.string

      fo.write(name.string.encode('utf-8'))
      fo.write('<br />')
      fo.write(company.encode('utf-8'))
      fo.write('<br />')
      fo.write(phone.string)
      fo.write('<br /><hr>')
      print name.string
      print company
      print phone
    except AttributeError:
      pass

if __name__ == '__main__':
    data = []
    # inline tests
    # print get_advisors_page_urls()
    # print get_advisors_pages('http://www.brightscope.com/financial-planning/find/advisor/1/')
    # get_advisor_details('http://www.brightscope.com/financial-planning/advisor/32187')

    
    fo = open("foo.html", "wb")
    fo.write('<html><head></head><body>')
    result_pages = get_advisors_page_urls()
    for result_page in result_pages:
        avdisors_pages = get_advisors_pages(result_page)
        for advisor_page in avdisors_pages:
            get_advisor_details(advisor_page, fo)

    fo.write('</body></html>')
    fo.close()
