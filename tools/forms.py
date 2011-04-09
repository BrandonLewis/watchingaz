from django import forms
from watchingaz.base.models import SessionDetail

TRACKER_CHOICES = (('d', 'Daily'), ('w', 'Weekly', ), ('m', 'Monthly'),
                      ('o', 'on_action'))
SEARCH_OPTIONS = (('b', 'Bills'), ('l', 'People'))

def get_session_details():
    sessions = SessionDetail.objects.values_list('name', 'full_name')
    if sessions:
        return tuple(sessions)
    else:
        return (('102', 'Fiftieth Legislature - First Regular Session'),
                ('104', 'Fiftieth Legislature - First Special Session'))

SESSIONS = get_session_details()

class AddTrackerShortForm(forms.Form):
    object_id = forms.CharField(widget=forms.HiddenInput)
    content_type = forms.CharField(widget=forms.HiddenInput)
    where_to = forms.CharField(widget=forms.HiddenInput)

class AddTrackerForm(forms.Form):
    object_id = forms.CharField(widget=forms.HiddenInput)
    content_type = forms.CharField(widget=forms.HiddenInput)
    email = forms.EmailField(required=False)
    update_on = forms.ChoiceField(choices=TRACKER_CHOICES,
                                  widget=forms.RadioSelect)
    where_to = forms.CharField(widget=forms.HiddenInput)

class SearchBarForm(forms.Form):
    search_field = forms.CharField()
    search_options = forms.ChoiceField(choices=SEARCH_OPTIONS,
                                       widget=forms.RadioSelect,
                                       required=False)
    session = forms.ChoiceField(choices=SESSIONS,
                                required=False)
class SearchForm(forms.Form):
    search_field = forms.CharField()
    search_options = forms.ChoiceField(choices=SEARCH_OPTIONS,
                                       widget=forms.RadioSelect,
                                       required=False)
    session_selection = forms.ChoiceField(choices=SESSIONS)

class QuestionForm(forms.Form):
    name = forms.CharField()
    email = forms.EmailField()
    subject = forms.CharField()
    question = forms.CharField(widget=forms.Textarea)
    bill_id = forms.CharField(widget=forms.HiddenInput)
    version_id = forms.CharField(widget=forms.HiddenInput)