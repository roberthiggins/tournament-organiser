""" Forms for public website."""

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class ErrorStringForm(forms.Form):                      # pylint: disable=W0232
    """ A form with a default error message """
    def error_code(self):                         # pylint: disable=C0111,R0201
        return 'Enter the required fields'

class AddTournamentForm(ErrorStringForm):               # pylint: disable=W0232
    """ Add a tournament """
    inputTournamentName = forms.CharField(label='Tournament Name', )
    inputTournamentDate = forms.DateField(
        label='Tournament Date',
        error_messages={'required': 'Enter the required fields'}
    )
    def error_code(self):                               # pylint: disable=C0111
        # pylint: disable=E1101
        if 'inputTournamentDate' in self._errors \
        and len(self._errors) == 1:                     # pylint: disable=E1101
            return self._errors['inputTournamentDate']  # pylint: disable=E1101
        else:
            return ErrorStringForm.error_code(self)

class ApplyForTournamentForm(ErrorStringForm):          # pylint: disable=W0232
    """ Apply for a tournament """
    def __init__(self, *args, **kwargs):                # pylint: disable=E1002
        t_list = kwargs.pop('tournament_list')
        super(ApplyForTournamentForm, self).__init__(*args, **kwargs)
        # pylint: disable=E1101
        self.fields['inputTournamentName'] = forms.ChoiceField(
            label='Select a tournament to register for',
            choices=t_list
        )
    inputUserName = forms.CharField(label='Your Username')

class CreateAccountForm(UserCreationForm):              # pylint: disable=W0232
    """ Add an account """
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(CreateAccountForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user

    def error_code(self):
        # pylint: disable=E1101
        if 'email' in self._errors and len(self._errors) == 1:
            return 'This email does not appear valid'
        elif 'username' in self._errors and len(self._errors) == 1:
            return 'Please choose another name'
        elif 'password2' in self._errors and len(self._errors) == 1:
            return 'Please enter two matching passwords'
        else:
            return 'Enter the required fields'

class FeedbackForm(ErrorStringForm):                    # pylint: disable=W0232
    """ Feedback and suggestions"""
    inputFeedback = forms.CharField(
        widget=forms.Textarea(attrs={'id': 'inputFeedback'}),
        label='Feedback',
        max_length=500)

class LoginForm(ErrorStringForm):                       # pylint: disable=W0232
    """ Login """
    inputUsername = forms.CharField(label='Username')
    inputPassword = forms.CharField(label='Password')

