import re
import urllib2
import urllib
from bs4 import BeautifulSoup

libraries = [
    'Zentrum',
    'Kirschgarten',
    'Neubad',
    'Gundeldingen',
    'Basel West',
]

def get_query_response(value):
    value = re.compile('\W+').sub(' ', value).strip()
    query = {'': '"%s"' % value}
    value = urllib.urlencode(query)
    url = 'http://stadtbibliothekbasel.ch:8080/InfoGuideClient.sisis/start.do?Login=opextern&Language=de&SearchType=2&Query=-1%s' % value
    response = urllib2.urlopen(url).read()
    return BeautifulSoup(response)


def getLibrary(branch):
    for l in libraries:
        if l in branch:
            return l


def search_catalog(value):
    soup = get_query_response(value)

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

search_catalog('Black Keys Brothers')
# print search_catalog('Black Keys Brothers')
# print search_catalog('White lies big tv')
