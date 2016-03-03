""" Forms for public website."""

import json

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.template.loader import render_to_string

class ErrorStringForm(forms.Form):                      # pylint: disable=no-init
    """ A form with a default error message """
    def error_code(self):                         # pylint: disable=missing-docstring,R0201
        return 'Enter the required fields'

class AddTournamentForm(ErrorStringForm):               # pylint: disable=no-init
    """ Add a tournament """
    inputTournamentName = forms.CharField(label='Tournament Name', )
    inputTournamentDate = forms.DateField(
        label='Tournament Date',
    )

class ApplyForTournamentForm(ErrorStringForm):          # pylint: disable=no-init
    """ Apply for a tournament """
    def __init__(self, *args, **kwargs):                # pylint: disable=E1002
        t_list = kwargs.pop('tournament_list')
        super(ApplyForTournamentForm, self).__init__(*args, **kwargs)
        # pylint: disable=no-member
        self.fields['inputTournamentName'] = forms.ChoiceField(
            label='Select a tournament to register for',
            choices=t_list
        )
    inputUserName = forms.CharField(label='Your Username')

class CreateAccountForm(UserCreationForm):              # pylint: disable=no-init
    """ Add an account """
    email = forms.EmailField(required=True)

    class Meta: # pylint: disable=no-init,missing-docstring,C1001
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):                # pylint: disable=no-init,E1002
        user = super(CreateAccountForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]         # pylint: disable=no-member
        if commit:
            user.save()
        return user

    def error_code(self):                               # pylint: disable=missing-docstring
        # pylint: disable=no-member
        if 'email' in self._errors and len(self._errors) == 1:
            return 'This email does not appear valid'
        elif 'username' in self._errors and len(self._errors) == 1:
            return 'Please choose another name'
        elif 'password2' in self._errors and len(self._errors) == 1:
            return 'Please enter two matching passwords'
        else:
            return 'Enter the required fields'

class EnterScoreForm(ErrorStringForm):                  # pylint: disable=no-init
    """Enter a score for a tournament"""
    def __init__(self, *args, **kwargs):                # pylint: disable=E1002
        username = kwargs.pop('username')
        tournament = kwargs.pop('tournament')
        super(EnterScoreForm, self).__init__(*args, **kwargs)
        # pylint: disable=no-member
        self.fields['username'] = forms.CharField(
            initial=username,
            widget=forms.widgets.HiddenInput())
        self.fields['tournament'] = forms.CharField(
            initial=tournament,
            widget=forms.widgets.HiddenInput())
    key = forms.CharField(label='Category (e.g. round_1_battle)', )
    value = forms.CharField(label='Score', )

class FeedbackForm(ErrorStringForm):                    # pylint: disable=no-init
    """ Feedback and suggestions"""
    inputFeedback = forms.CharField(
        widget=forms.Textarea(attrs={'id': 'inputFeedback'}),
        label='Feedback',
        max_length=500)

class LoginForm(ErrorStringForm):                       # pylint: disable=no-init
    """ Login """
    inputUsername = forms.CharField(label='Username')
    inputPassword = forms.CharField(label='Password')

class MissionWidget(forms.MultiWidget):
    """Widget to handle the input for the custom mission field"""
    def __init__(self, *args, **kwargs):# pylint: disable=E1002
        rounds = int(kwargs.pop('rounds', 0))
        widgets = tuple(forms.TextInput() for x in range(1, rounds + 1))

        super(MissionWidget, self).__init__(widgets, *args, **kwargs)

    def decompress(self, value):
        return value.split(',') if value else []

    def format_output(self, rendered_widgets):
        """Customize widget rendering. We need the inputs to look separate"""
        widget_context = {
            'elements': [{'label': 'Round {}'.format(x + 1), 'input': y} \
            for x, y in enumerate(rendered_widgets)]
        }
        return render_to_string('mission-input.html', widget_context)

class MissionFields(forms.MultiValueField):
    """Custom field to display all the mission inputs and combine them"""
    def __init__(self, *args, **kwargs):                # pylint: disable=E1002
        rounds = int(kwargs.pop('rounds', 0))
        fields = tuple(forms.CharField() for x in range(0, rounds))
        widget = MissionWidget(rounds=rounds)

        super(MissionFields, self).__init__(
            fields, widget=widget, *args, **kwargs)

    def compress(self, data_list):
        return json.dumps(data_list)

class SetMissionsForm(ErrorStringForm):
    """Set missions for a tournament"""
    def __init__(self, *args, **kwargs):                # pylint: disable=E1002
        t_id = kwargs.pop('tournament_id')
        initial_missions = kwargs.pop('initial_missions', None)
        rounds = int(kwargs.pop('rounds'))

        super(SetMissionsForm, self).__init__(*args, **kwargs)

        # pylint: disable=no-member
        self.fields['missions'] = MissionFields(rounds=rounds, required=False)
        if initial_missions is not None:
            self.initial['missions'] = initial_missions # pylint: disable=no-member
        # pylint: disable=no-member
        self.fields['tournamentId'] = forms.CharField(
            initial=t_id,
            widget=forms.widgets.HiddenInput())

class SetRoundsForm(ErrorStringForm):
    """ Set number of rounds for a tournament"""
    def __init__(self, *args, **kwargs):                # pylint: disable=E1002
        t_id = kwargs.pop('tournament_id')
        super(SetRoundsForm, self).__init__(*args, **kwargs)
        # pylint: disable=no-member
        self.fields['tournamentId'] = forms.CharField(
            initial=t_id,
            widget=forms.widgets.HiddenInput())
    numRounds = forms.CharField(label='Number of rounds')

class TournamentSetupForm(ErrorStringForm):             # pylint: disable=no-init
    """Setup a tournament. Mostly set the scores you can get"""
    def __init__(self, *args, **kwargs):                # pylint: disable=E1002
        t_id = kwargs.pop('tournament_id')
        score_categories = kwargs.pop('score_categories')
        super(TournamentSetupForm, self).__init__(*args, **kwargs)
        # pylint: disable=no-member
        self.fields['tournamentId'] = forms.CharField(
            initial=t_id,
            widget=forms.widgets.HiddenInput())
        self.fields['scoreCategory'] = forms.ChoiceField(
            label='What type of score is this?',
            choices=score_categories
        )

    key = forms.CharField(label='Score key', )
    maxVal = forms.CharField(label='Min Score', required=False)
    minVal = forms.CharField(label='Max Score', required=False)
