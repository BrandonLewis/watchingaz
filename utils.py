import re
from django.contrib.humanize.templatetags.humanize import ordinal

def legislature_to_number(leg):
    """
    Takes a full session and splits it down to the values for
    FormatDocument.asp.

    session = '50th-1st-regular'
    legislature_to_number(session) --> '50Leg/1s'
    """
    groups = re.match(r'^(\d\d)\w+-(\d\d?)\w+-(regular|special)', leg)
    if groups:
        return '%sLeg/%s%s' % (groups.group(1), groups.group(2), groups.group(3)[0])

def number_to_leg(term, session):
    term = ordinal(term)
    session, stype = ordinal(session[0]), session[1]
    return '%s-%s-%s' % (term, session, {'r':'regular', 's':'special'}[stype])