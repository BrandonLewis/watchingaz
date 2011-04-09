from django.core.management.base import BaseCommand, CommandError, make_option
from django.conf import settings
from django.db.models.query import QuerySet
from watchingaz.tools.models import Tracker
from watchingaz.dashboard.models import Profile
import json
import datetime, calendar

def run_trackers(state):
    """For each user, checks if there are any updates to their tracked items
    and builds and sends an email if there are."""
    # lets get trackers updated today
    today = datetime.date.today() # - datetime.timedelta(days=1)
    weekly = []
    monthly = []
    all = set()
    daily = Tracker.objects.filter(last_updated=today)
    if daily:
        all.update(daily)
    if today.isoweekday() == 5:
        last_week = today - datetime.timedelta(days=7)
        weekly = Tracker.objects.filter(last_updated__gte=last_week)
        if weekly:
            all.update(weekly)
        
    last_day = calendar.monthrange(today.year, today.month)[-1]
    if today.day == last_day:
        since_month = today - datetime.timedelta(days=last_day)
        monthly = Tracker.objects.filter(last_updated__gte=since_month)
        if monthly:
            all.update(monthly)
    # there's no point in sending a person more than one email if daily and weekly
    # monthly tracked items happen to fall on the same day
    all_users = Profile.objects.filter(user__is_active=True)
    for user in all_users:
        user_tracking = user.tracked_items.filter(tracker__in=all)

class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
    make_option('--state', action='store', dest='state',
                default='az', help='Two char state abbreviation'),
    )

    def handle(self, *args, **options):
        run_trackers(state=options.get('state'))