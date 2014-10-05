# mechanize Browser
import re
import urllib2
import urllib
from bs4 import BeautifulSoup
import mechanize

base_URL = 'http://stadtbibliothekbasel.ch:8080'

# search value
value = 'Arbeit und Struktur'

# encode value
value = re.compile('\W+').sub(' ', value).strip()
query = {'': '"%s"' % value}
value = urllib.urlencode(query)

# build url
url = '%s/InfoGuideClient.sisis/start.do?Login=opextern&Language=de&SearchType=2&Query=-1%s' % (base_URL, value)
print url

# open new browser
br = mechanize.Browser()
# open url
r = br.open(url)
# read html output
html = r.read()
# soup it
soup = BeautifulSoup(html)

# searchresults
results = []

# iterate through search results
for r in soup.select('.data .t1'):

    url = base_URL + soup.select('.data .t1')[0]['href']

    # open detail view of search result
    detailContent = br.open(url)
    html = detailContent.read()
    detailContent = BeautifulSoup(html)

    # append each search results
    results.append({
        'name': soup.select('.data .t1')[0].string.strip(),
        'url': url,
        'content': soup
    })

print results
print len(results)
