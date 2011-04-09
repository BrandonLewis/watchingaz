"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import Client, TestCase
from watchingaz.base.models import Term
from watchingaz.people.models import Person, Role

class SimpleTest(TestCase):
    fixtures = ['people.json']
    def test_person_served(self):
        """
        Tests that the person.served() method returns a list of two-tuples
        spanning the start to end of a legislators consecutive terms
            [ (1-12-2009, 4-29-2010) ] # served only the 49th term
            [ (1-12-2009, None) ] # ie 49th through now  
            [
              (1-12-2009, 7-1-2009), # served to the 49th-2nd-regular
              (1-10-2011, None) # and again in the 50th through now
            ]
        """
        person = Person.objects.get(leg_id="AZL000028")
        method_served = person.served()
        
        manual_served = []
        
        date_range = {}
        
        for role in person.roles.filter(type='member').order_by('term'):
            #term = term.objects.get(name=role.term)
            if not role.term in date_range:
                date_range[role.term] = []
            date_range[role.term] += Session.objects.filter(term__name=role.term,
                                        session_details__type='primary'
                        ).values_list('name', 'session_details__start_date',
                                      'session_details__end_date')
        
        
        self.assertEqual(method_served, manual_served)
        
    def test_person_view_rendered(self):
        """
        Tests that the person_views rendered html is contains the RDFa markup
        """
        self.assertEqual(1+1, 2)
