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

results = []

def get_query_response(value):
    value = re.compile('\W+').sub(' ', value).strip()
    query = {'': '"%s"' % value}
    value = urllib.urlencode(query)
    url = '%s/InfoGuideClient.sisis/start.do?Login=opextern&Language=de&SearchType=2&Query=-1%s' % (base_URL, value)
    br = mechanize.Browser()
    response = br.open(url)
    search_catalog(response, br)

    # response = urllib2.urlopen(url).read()
    # print br.read()


    # soup = BeautifulSoup(response.read())
    # for r in soup.select('.data .t1'):
    #     r = br.open(base_URL + soup.select('.data .t1')[0]['href'])
    #     results.append(r.read())
    #
    # for r in results:
    #     soup = BeautifulSoup(r)
    #     setItem(soup)
    # return


def getMultipleSearchResults(results):
    pass

def setItem(query):
    pass

def getLibrary(branch):
    for l in libraries:
        if l in branch:
            return l

def getStatus(statusString):
    pass


def search_catalog(query, browser):
    # query = get_query_response(value)

    soup = BeautifulSoup(query.read())

    # searchresults
    results = []

    if (soup.select('#hitlist')): # if an artists list gets returned by query
        # TODO: return hitlist as recommandations to select
        # iterate through search results
        for r in soup.select('.data .t1'):

            url = base_URL + soup.select('.data .t1')[0]['href']

            # open detail view of search result
            detailContent = browser.open(url)
            html = detailContent.read()
            detailContent = BeautifulSoup(html)

            # append each search results
            results.append({
                'name': soup.select('.data .t1')[0].string.strip(),
                'url': url,
                'content': soup
            })

    else :
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



get_query_response("Arbeit und Struktur")


# search_catalog('Arbeit und Struktur')
# print search_catalog('Black Keys Brothers')
# print search_catalog('White lies big tv')
