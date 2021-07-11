import urllib.parse
import re
from urllib.request import urlopen

PAGES = [
    u"List of popular music genres",
    u"List of styles of music: A\u2013F",
    u"List of styles of music: G\u2013M",
    u"List of styles of music: N\u2013R",
    u"List of styles of music: S\u2013Z"
]
BASE_URL = u"http://en.wikipedia.org/w/index.php"

START_PAT = re.compile('==.*==', re.M)
END_STRING = u'==References=='
ITEM_PAT = re.compile('\[\[(?:[^\]\|]*\|)?([^\]\|]*)\]\]')
BAD_NAME_PAT = re.compile('^[A-Z][a-z]?(-[A-Z][a-z]?)?$')  # Letter ranges.
INTERNAL_LINK_PAT = re.compile('[a-z][a-z]:')
DROP_PART_PAT = re.compile('\(.*\)$')


def getwiki(name):
    name = name.replace(' ', '_').encode('utf8')
    params = {
        'title': name,
        'action': 'raw',
    }
    # url = "%s?%s" % (BASE_URL, urllib.urlencode(params))
    url = "%s?%s" % (BASE_URL, urllib.parse.urlencode(params))
    return urlopen(url).read().decode('utf8')


def genres_for(page):
    text = getwiki(page)

    # Strip off top and bottom cruft.
    if END_STRING in text:
        text, _ = text.split(END_STRING, 1)
    parts = START_PAT.split(text, 1)
    if len(parts) == 2:
        text = parts[1]

    for line in text.split(u'\n'):
        m = ITEM_PAT.search(line)
        if m:
            name = m.group(1)
            # Filter some non-genre links.
            if name.startswith('Section') or BAD_NAME_PAT.match(name) or \
                    INTERNAL_LINK_PAT.match(name):
                continue
            name = DROP_PART_PAT.sub('', name)
            name = name.strip().lower()
            if name:
                yield name


def getgenres():
    genres = set()
    for page in PAGES:
        genres.update(genres_for(page))
    return genres


if __name__ == '__main__':
    f = open('genres.txt', 'w')
    for genre in sorted(getgenres()):
        f.write(genre + '\n')
