import os
from django.conf import settings
from watchingaz.bills.models import Bill, Version, VersionText, BillPageView
from watchingaz.utils import number_to_leg, legislature_to_number

def getVersionAbbrev(name):
    """
    this is a pretty basic version scheme and doesnt include ammendments
    etc that I havent yet integrated into the system
    """
    names = ('House Engrossed', 'Introduced', 'Senate Engrossed')
    choices = ('I', 'H', 'S', 'C')
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

def getNodePrefix(metadata):
    strToReturn = ''
    strToReturn += legislature_to_number(metadata['bill']['session']).replace('/', ':').replace('Leg', '') + ":"
    strToReturn += metadata['bill']['bill_id'].replace(' ', ':')
    strToReturn += getVersionAbbrev(metadata['name'])
    return strToReturn



def get_bill_text(term, session, version, **kargs):
    data_dir = settings.DATA_DIR
    template_name = version.url.split('/')[-1]
    path = os.path.abspath(os.path.join(data_dir, 'bill_text', term[0:2] + "Leg", 
                                        session, template_name))
    try:
        template = open(path)
        template_string = template.read()
        template.close()
    except IOError:
        template_string = ""
    return template_string
