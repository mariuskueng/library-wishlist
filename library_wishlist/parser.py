import re
import urllib2
import urllib
from bs4 import BeautifulSoup
import mechanize

base_URL = 'http://stadtbibliothekbasel.ch:8080'

# TODO: check if django is around,
# if yes use db models

libraries = [
    'Zentrum',
    'Kirschgarten',
    'Neubad',
    'Gundeldingen',
    'Basel West',
]


def search_catalog(value):
    value = re.compile('\W+').sub(' ', value).strip()
    query = {'': '"%s"' % value}
    value = urllib.urlencode(query)
    url = '%s/InfoGuideClient.sisis/start.do?Login=opextern&Language=de&SearchType=2&Query=-1%s' % (base_URL, value)
    br = mechanize.Browser()
    response = br.open(url)
    parse_query(response, br)


def getMultipleSearchResults(soup, browser):
    # searchresults
    results = []

    # iterate through search results
    for i, r in enumerate(soup.select('.data .t1')):

        link = soup.select('.data .t1')[i]
        url = base_URL + link['href']

        # open detail view of search result
        detailContent = browser.open(url)
        html = detailContent.read()
        detailContent = BeautifulSoup(html)

        # append each search results
        results.append({
            'name': link.string.strip(),
            'url': url,
            'content': detailContent,
            'index': i,
            'copies': []
        })

    return results


def setItem(soup):
    copies_tags = soup.select('#tab-content tr')
    del copies_tags[0]

    copies = []

    image = BeautifulSoup(str(soup.select('.box-container img'))).find('img')
    if image:
        image = image['src']
    else:
        image = ''

    item = {
        'name': soup.select('.box-container td strong')[0].string.split(' [')[0],
        'author': soup.select('.box-container td a')[0].string,
        'copies': [],
        'status': False,
        'image': image
    }

    for copy in copies_tags:
        branch = getLibrary(str(copy.select('td')[3].contents))
        status = copy.select('td')[4].string
        location = BeautifulSoup(str(copy.select('td')[2])).get_text().strip()

        if not branch:
            continue

        if 'frei' in status:
            status = True
        elif 'ausleihbar' in status:
            status = True
        else:
            status = False

        if status == True:
            item['status'] = status

        copies.append({
            'branch': branch,
            'status': status,
            'signatute': None,
            'location': location
        })

        item['copies'] = copies

    return item


def getLibrary(branch):
    for l in libraries:
        if l in branch:
            return l


def getStatus(statusString):
    pass


def parse_query(query, browser):
    soup = BeautifulSoup(query.read())

    if (soup.select('#hitlist')): # if an artists list gets returned by query
        results = getMultipleSearchResults(soup, browser)

        for r in results:
            r['copies'].append(setItem(r["content"]))

    else:
        setItem(soup)


# search_catalog("Arbeit und Struktur")
# get_query_response('Black Keys Brothers')

# search_catalog('Arbeit und Struktur')
# print search_catalog('Black Keys Brothers')
# print search_catalog('White lies big tv')
