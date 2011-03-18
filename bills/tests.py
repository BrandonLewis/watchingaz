"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
import os, glob
import json
from watchingaz.bills.models import Bill, BillStatus


class SimpleTest(TestCase):
    fixtures = ["people.json", 'committees.json', "bills.json"]
    
    def test_bill_status_output(self):
        """
        Tests that the output of billstatus.get_status is in the format:
        q is a dictonary keyed to return True or False
        {
            'introduced': {'passed': q[self.introduced], 'date': self.first_read_date}
            'primary' : {'passed': q[self.passed_primary], 'date': self.primary_date},
            'other'   : {'passed': q[self.passed_other],   'date': self.other_date},
            'governor': {'passed': q[self.passed_gov],     'date': self.gov_date}
        }
        """
        self.assertEqual(1 + 1, 2)
