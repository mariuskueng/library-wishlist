import re
import urllib
from bs4 import BeautifulSoup
import mechanize

base_URL = 'http://katalog.stadtbibliothekbasel.ch/'

libraries = [
    'Zentrum',
    'Kirschgarten',
    'Neubad',
    'Gundeldingen',
    'Basel West',
]


def search_catalog(value):
    '''
        @param value: string, search value
        @param local: string, 'single' or 'multiple' to determine if the search
                        term returns a single or multiple search results
    '''

    # set encoding to utf-8
    value = value.encode("utf-8")

    # clean up string
    re.compile('\W+', re.UNICODE).sub(' ', value).strip()
    query = {'': '"%s"' % value}
    value = urllib.urlencode(query)

    # combine base_URL with search parameters and value
    url = '%sggg/webopac/direct.aspx?SearchField=W&view=SHORT&SearchTerm=%s' % (base_URL, value)

    # init mechanize browser
    br = mechanize.Browser()

    # open url
    response = br.open(url)

    # return parse_query response
    return parse_query(response, br)


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
    if len(soup.select('ul')) == 5:  # if item is not available in library return
        return None

    image = soup.select('.coverimg')
    if image:
        image = image[0]['src']
    else:
        image = ''

    author = soup.select('.menu')[1]
    author_text = ''

    if len(author.select('span')) > 0:
        for s in author:
            author_text += str(s.string)
    else:
        author = author.string

    if author_text:
        author = author_text

    item = {
        'name': soup.select('#marc_title')[0].string,
        'author': author,
        'copies': [],
        'status': False,
        'image': image
    }

    copies = []
    copies_tags = soup.select('#tblItems tr')  # bs tags

    if soup.select('.extdatagrid_navig'): # if single copy there's an extra row
        del copies_tags[0]

    del copies_tags[0]

    for copy in copies_tags:

        branch = ''
        status = ''
        location = ''
        signature = ''

        for i in range(1, 3):
            if not branch:
                branch = getLibrary(copy.select('td')[i].string)

        if not branch:
            continue

        for i in range(2, 4):
            if not status:
                status = getStatus(copy.select('td')[i + 2].string)
            if not location:
                location = BeautifulSoup(copy.select('td')[i].string)
            if not signature:
                signature = BeautifulSoup(copy.select('td')[i + 1].string)

        copies.append({
            'branch': branch,
            'status': status,
            'signature': signature,
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
