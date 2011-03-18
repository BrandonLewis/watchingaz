import re
import os
import logging
import logging.handlers
from django.conf import settings
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
    if term.endswith('Leg'):
        term = term.replace('Leg', '')
    term = ordinal(term)
    session, stype = ordinal(session[0]), session[1]
    return '%s-%s-%s' % (term, session, {'r':'regular', 's':'special'}[stype])
    
def get_logger(name, **kargs):
    level = kargs.pop('log_level', None)
    log_file = os.path.abspath(os.path.join(settings.LOG_DIR, name + '.txt'))
    log_handler = logging.handlers.RotatingFileHandler(people_file,maxBytes=1024,
                                                        backupCount=5 )
    if level:
        if level == 'INFO':
            log_handler.setLevel(logging.INFO)
        elif level == 'DEBUG':
            log_handler.setLevel(logging.DEBUG)
        elif level == 'WARN':
            log_handler.setLevel(logging.WARN)
        elif level == 'ERROR':
            log_handler.setLevel(logging.ERROR)
        else:
            log_handler.setLevel(logging.CRITICAL)
    elif settings.DEBUG:
        log_handler.setLevel(logging.DEBUG)
    else:
        log_handler.setLevel(logging.WARN)
    logger = logging.getLogger(name)
    logger.addHandler(log_handler)
    return logger
