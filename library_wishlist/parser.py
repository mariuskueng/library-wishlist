import re
import urllib2
import urllib
from bs4 import BeautifulSoup
import mechanize

base_URL = 'http://stadtbibliothekbasel.ch:8080'

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
    # response = urllib2.urlopen(url).read()
    # print br.read()


    soup = BeautifulSoup(response.read())
    for r in soup.select('.data .t1'):
        r = br.open(base_URL + soup.select('.data .t1')[0]['href'])
        results.append(r.read())

    for r in results:
        soup = BeautifulSoup(r)
        setItem(soup)
    return

    return response

def getMultipleSearchResults(results):
    pass

def setItem(query):


def getLibrary(branch):
    for l in libraries:
        if l in branch:
            return l


def search_catalog(value):
    query = get_query_response(value)
    return
    soup = BeautifulSoup(query.read())
    # print soup
    # print soup.search('#hitlist')
    # return
    if (soup.select('#hitlist')): # if an artists list gets returned by query
        # TODO: return hitlist as recommandations to select
        return

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

# Browser
# value = 'Arbeit und Struktur'
# value = re.compile('\W+').sub(' ', value).strip()
# query = {'': '"%s"' % value}
# value = urllib.urlencode(query)
# url = '%s/InfoGuideClient.sisis/start.do?Login=opextern&Language=de&SearchType=2&Query=-1%s' % (base_URL, value)
# br = mechanize.Browser()
# print url
# # Open some site, let's pick a random one, the first that pops in mind:
# r = br.open(url)
# html = r.read()
# print html
# # print html
# soup = BeautifulSoup(html)

# results = []
# for r in soup.select('.data .t1'):
#     results.append({
#         'name': soup.select('.data .t1')[0].string.strip(),
#         'url': base_URL + soup.select('.data .t1')[0]['href']
#     })
#     r = br.open(results['url'])
#     print r.read()

# # print results
# print soup.select('p')

# Show the source
# print html
# or
# print br.response().read()


search_catalog('Arbeit und Struktur')
# print search_catalog('Black Keys Brothers')
# print search_catalog('White lies big tv')
