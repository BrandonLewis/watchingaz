from django.core.management.base import BaseCommand, CommandError, make_option
from django.conf import settings
from watchingaz.utils import number_to_leg
from watchingaz.base.models import Session
from watchingaz.bills.models import Bill, Version, VersionText

import os, re
from BeautifulSoup import UnicodeDammit
from lxml import etree, html
import pymongo
import gridfs
import pymongo.errors
MONGO_HOST = 'localhost'
MONGO_PORT = 27017
MONGO_DATABASE = 'fiftystates'
CONN = pymongo.Connection(MONGO_HOST, MONGO_PORT)
DB = CONN[MONGO_DATABASE]
FS = gridfs.GridFS(DB, collection="documents")
FS_SUM = gridfs.GridFS(DB, collection="summaries")

SESSION = 'Forty-ninth Legislature - Second Regular Session'
STATE = 'az'

__metadata = {}

SOLR_URL = 'http://localhost:8080/solr-openstates/select/?q=%s'

word_key = (
    ('fiftieth', '50'),
    ('fifty', '50'),
    ('forty', '40'),
    ('first', '1'),
    ('second', '2'),
    ('third', '3'),
    ('fourth', '4'),
    ('fifth', '5'),
    ('sixth', '6'),
    ('seventh', '7'),
    ('eighth', '8'),
    ('ninth', '9'),
    ('tenth', '10'),
    ('eleventh', '11'),
    ('twelth', '12'),
    ('regular', 'r'),
    ('special', 's'),
)

def legislature_to_number(leg):
    """
    Takes a full session and splits it down to the values for
    FormatDocument.asp.

    session = 'Forty-ninth Legislature - First Special Session'
    legislature_to_number(session) --> '49Leg/1s'
    """
    new_style = re.match(r'^(\d\d)\w+-(\d\d?)\w+-(regular|special)', leg)
    if new_style:
        return '%sLeg/%s%s' % (new_style.group(1), new_style.group(2), new_style.group(3)[0])

    l = leg.lower().replace('-', ' ').split()
    session = [x[1] for y in l for x in word_key if x[0] == y]
    if len(session) == 4:
        return '%dLeg/%s%s' % (int(session[0]) + int(session[1]), session[2], session[3])
    else:
        return '%sLeg/%s%s' % (session[0], session[1], session[2])


def getNodePrefix(name, session, bill_id):
    strToReturn = ''
    strToReturn += legislature_to_number(session).replace('/', ':').replace('Leg', '') + ":"
    strToReturn += bill_id.replace(' ', ':')
    strToReturn += getVersionAbbrev(name)
    return strToReturn

def getVersionAbbrev(name):
    """
    this is a pretty basic version scheme and doesnt include ammendments
    etc that I havent yet integrated into the system
    """
    names = ('House Engrossed', 'Introduced', 'Senate Engrossed',
             'Conference Engrossed')
    choices = ('I', 'H', 'S', 'C', 'T', 'J')
    if 'Chaptered Version' in name:
        return 'C'
    elif 'Transmitted Version' in name:
        return 'T'
    elif 'House Engrossed' in name:
        return 'H'
    elif 'Senate Engrossed' in name:
        return 'S'
    elif 'Introduced Version' in name:
        return 'I'
    elif 'Conference Engrossed' in name:
        return 'J'

def transform(doc, stylesheet=None):
    s = doc.metadata['bill']['session']
    try:
        session = Session.objects.get(name=s)
    except Session.DoesNotExist:
        s = legislature_to_number(doc.metadata['bill']['session'])
        term, s = s.split('/')
        s = number_to_leg(term, s)
        session = Session.objects.get(name=s)
    version = Version.objects.get(bill__number=doc.metadata['bill']['bill_id'],
                                     bill__session=session,
                                     name=doc.metadata['name'])
    if version.document_id != doc._id:
        version.document_id = doc._id
        version.save()

    def getNid(context, nodes):
        getNid.node_count += 1
        nid = '%s:%s' % (getNid.prefix , str(getNid.node_count))
        text_node, created = VersionText.objects.get_or_create(node_id=nid, version=version)
        if created:
            text_node.save()
        return nid
    getNid.node_count = 0
    getNid.prefix = getNodePrefix(version.name, s, doc.metadata['bill']['bill_id'])

    ns = etree.FunctionNamespace('http://watchingaz.us/utilities')
    ns.prefix = 'mygov'
    ns['getNid'] = getNid
    style_path = os.path.abspath(os.path.join(settings.DATA_DIR, 'xsl'))
    stylesheet = open(style_path + '/bill_clean.xsl', 'rb')
    xsl = etree.parse(stylesheet)
    trans = etree.XSLT(xsl)
    page_name = doc.metadata['url'].split('/')[-1]
    folder = legislature_to_number(doc.metadata['bill']['session']).split('/')
    doc = doc.read().decode("ISO-8859-2", "xmlcharrefreplace").encode("UTF-8", "xmlcharrefreplace")
    #doc = UnicodeDammit(doc.read(), isHTML=True).unicode
    elem = html.fromstring(doc)
    changed = trans(elem)
    stylesheet.close()

    fragment = ''
    for div in changed.xpath('//div[contains(@class, "Section")]'):
        fragment +=  etree.tostring(div)

    path = os.path.abspath(os.path.join(settings.DATA_DIR, 'bill_text'))
    if not os.path.exists(path):
        os.mkdir(path)
    path = os.path.abspath(os.path.join(path, folder[0]))
    if not os.path.exists(path):
        os.mkdir(path)
    path = os.path.abspath(os.path.join(path, folder[1]))
    if not os.path.exists(path):
        os.mkdir(path)
    path += '/%s' % page_name
    newfile = open(path, 'wb')
    newfile.write(fragment)
    newfile.close()
    return path

def transform_session(session=SESSION, state=STATE):
    for bill in db.bills.find( dict(state=state.lower(), session=session) ):
        for version in bill['versions']:
            if 'document_id' not in version:
                continue
            transform(version['document_id'])
            print "Processed: " + version['document_id']
            
def transform_documents_db(session, state):
    docs = DB.documents.files.find()
    doc_ids = []
    for doc in docs:
        doc_ids.append(doc['_id'])

    for doc_id in doc_ids:
        doc = FS.get(doc_id)
        path = transform(doc)
        print "saved %s" % path
    
class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('--state', action='store_true', dest='state',
                    default='AZ', help='Two char state abbreviation'),
        make_option('--session', action='store_true', dest='session',
                    default='Fiftieth Legislature - First Regular Session',
                    help='import bills from the openstates project'),
        make_option('--transform-db', action='store_true', dest='trans_db',
                    default=False,
                    help='transform all the documents in the database'),
    )

    def handle(self, *args, **options):

        trans_db = options.get('trans_db')

        if trans_db:
            transform_documents_db(session=options.get('session'),
                                   state=options.get('state'))
        else:
            transform_session(state=options.get('state'),
                              session=options.get('session'))
