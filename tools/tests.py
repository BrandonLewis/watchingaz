"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from watchingaz.tools.models import Tracker

class SimpleTest(TestCase):
    def setUp(self):
        me = User.objects.create(username='someguy', password='password')
        me.save()
        
    def test_trackable_constraint(self):
        """
        Tests that Trackers can only be added if they are in the trackable table
        """
        def add_tracker():
            not_trackable = ContentType.objects.get(model='user')
            any_user = User.objects.all()[0]
            try:
                tracker = Tracker.objects.get_or_create(content_type=not_trackable,
                                                    tracked_id=any_user.id)
            except ValidationError:
                return ValidationError
            return tracker 
        self.assertEqual(add_tracker(), ValidationError)
        
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 2)
