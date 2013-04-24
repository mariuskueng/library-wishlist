import urllib2
import urllib
from bs4 import BeautifulSoup

def get_query_response(value):
    query = {'': '"%s"' % value}
    value = urllib.urlencode(query)
    url = 'http://stadtbibliothekbasel.ch:8080/InfoGuideClient.sisis/start.do?Login=opextern&Language=de&SearchType=2&Query=-1%s' % value
    response = urllib2.urlopen(url).read()
    return BeautifulSoup(response)

def search_catalog(value):
    soup = get_query_response(value)

    # query = 'Django Django'
    # soup = get_query_response(query)
    # soup = BeautifulSoup(open('library_wishlist/query.html'))

    name = soup.select('.box-container td strong')[0].string.split(' ')[0]
    author = soup.select('.box-container td a')[0].string

    copies_tags = soup.select('#tab-content tr')
    del copies_tags[0]

    copies = []

    for copy in copies_tags:
        branch = str(copy.select('td')[3].contents)
        status = copy.select('td')[4].string

        if 'frei' in status:
            status = True
        elif 'ausleihbar' in status:
            status = True
        else:
            status = False

        copies.append({
            'branch': branch,
            'status': status
        })

    # print copies
