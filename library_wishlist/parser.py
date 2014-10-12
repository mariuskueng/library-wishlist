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
    # set encoding to utf-8
    value = value.encode("utf-8")

    # clean up string
    re.compile('\W+', re.UNICODE).sub(' ', value).strip()
    query = {'': '"%s"' % value}
    value = urllib.urlencode(query)

    # combine base_URL with search parameters and value
    url = '%s/InfoGuideClient.sisis/start.do?Login=opextern&Language=de&SearchType=2&Query=-1%s' % (base_URL, value)

    # init mechanize browser
    br = mechanize.Browser()

    # open url
    response = br.open(url)

    # return parse_query response
    return parse_query(response, br)


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
    if len(soup.select('.left')) == 0: # if item is not available in library return
        return None

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
        if len(copy.select('td')) == 0: # if table row is no copy i.e "Neuerscheinungen"
            continue

        branch = getLibrary(str(copy.select('td')[3].contents))

        if not branch:
            continue

        status = getStatus(copy.select('td')[4].string)
        location = BeautifulSoup(str(copy.select('td')[2])).get_text().strip()

        copies.append({
            'branch': branch,
            'status': status,
            'signature': None,
            'location': location
        })

        item['status'] = status
        item['copies'] = copies

    return item


def getLibrary(branch):
    # only return if branch of result is in libraries list
    for l in libraries:
        if l in branch:
            return l


def getStatus(statusString):
    status = False
    if "frei" in statusString:
        status = True
    elif "ausleihbar" in statusString:
        status = True
    return status


def parse_query(query, browser):
    # make a BeautifulSoup object from passed query
    soup = BeautifulSoup(query.read())

    # if a list of multiple search results gets returned by query
    if (soup.select('#hitlist')):

        # pass BeautifulSoup object and browser instance
        results = getMultipleSearchResults(soup, browser)

        # create a new item for each result
        for r in results:
            r['item'] = setItem(r["content"])
            # reset html content
            r['content'] = ""

        return results

    # or a single search result
    else:
        # create item from BeautifulSoup object
        return setItem(soup)
