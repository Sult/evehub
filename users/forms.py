from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from django_countries.widgets import CountrySelectWidget

from .models import ContactMail, Profile
from apis.models import Api
from characters.models import CharacterApi


class RegistrationForm(UserCreationForm):
    """
    edit the User Registration form to add an emailfield
    """

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        #add custom errormessages
        self.fields['username'].error_messages = {
            'invalid': 'Invalid username'
        }

    #make sure username is lowered and unique
    def clean_username(self):
        username = self.cleaned_data.get('username')
        try:
            User.objects.get(username__iexact=username)
            raise forms.ValidationError("This username is already in use.")
        except User.DoesNotExist:
            pass

        return username

    #def clean_email(self):
        #email = self.cleaned_data.get('email')
        #username = self.cleaned_data.get('username')
        #if email and User.objects.filter(email=email).exclude(
            #username=username
        #).count():
            #raise forms.ValidationError(
                #u'This email address is already in use.'
            #)
        #return email

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        #user.email = self.cleaned_data['email']

        if commit:
            user.save()
        return user


class LoginForm(forms.Form):
    """create login form with placeholders for fields"""

    username = forms.CharField(
        required=True, widget=forms.TextInput(
            attrs={'placeholder': 'Username:'}
        )
    )
    password = forms.CharField(
        required=True, widget=forms.PasswordInput(
            attrs={'placeholder': 'Password:'}
        )
    )

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        if not user or not user.is_active:
            raise forms.ValidationError("Login invalid")
        return self.cleaned_data

    def login(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        return user


class ContactMailForm(forms.ModelForm):
    """ send a contact mail to admin """

    body = forms.CharField(widget=forms.Textarea, label='Message')

    class Meta:
        model = ContactMail
        fields = ["title", "email", "body"]


class ProfileForm(forms.ModelForm):
    """ set optional fields for userprofile """

    #user fields
    first_name = forms.CharField(required=False, max_length=30)
    last_name = forms.CharField(required=False, max_length=30)
    email = forms.EmailField(required=False)

    CHOICES = (("", "select timezone"),) + Profile.TIMEZONES
    timezone = forms.ChoiceField(choices=CHOICES)
    # INTERESTS = (
    #     ("Exploration", "Exploration"),
    #     ("Mission Running", "Mission Running"),
    #     ("Incursion", "Incursion"),
    #     ("Alliance Warfare", "Alliance Warfare"),
    #     ("Bounty Hunting", "Bounty Hunting"),
    #     ("Factional Warfare", "Factional Warfare"),
    #     ("Piracy", "Piracy"),
    #     ("Small-Scale Gangs", "Small-Scale Gangs"),
    #     ("Trade", "Trade"),
    #     ("Mining", "Mining"),
    #     ("Research", "Research"),
    #     ("Manufacturing", "Manufacturing"),
    #     ("Roleplay", "Roleplay"),
    # )
    # interests = forms.MultipleChoiceField(
    #     widget=forms.CheckboxSelectMultiple, choices=INTERESTS
    # )

    class Meta:
        model = Profile
        fields = [
            'first_name',
            'last_name',
            'email',
            'timezone',
            'country',
        ]
        widgets = {'country': CountrySelectWidget()}
        layout = "{widget}"

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user")
        super(ProfileForm, self).__init__(*args, **kwargs)

    def save(self):
        self.user.first_name = self.cleaned_data.get('first_name')
        self.user.last_name = self.cleaned_data.get('last_name')
        self.user.email = self.cleaned_data.get('email')
        self.user.profile.country = self.cleaned_data.get('country')
        self.user.profile.timezone = self.cleaned_data.get('timezone')
        self.user.save()
        self.user.profile.save()

    def save_tags(self, postdata):
        #add tags
        for tag in self.interests() + self.locations():
            if tag in postdata:
                self.user.profile.tags.add(tag)
            else:
                self.user.profile.tags.remove(tag)
        self.user.profile.save()

    def interests(self):
        interests = [
            'Exploration', 'Mission Running', 'Incursion', 'Alliance Warfare',
            'Bounty Hunting', 'Factional Warfare', 'Piracy',
            'Small-Scale Gang', 'Trade', 'Mining', 'Research', 'Manufacturing',
            'Roleplay'
        ]
        return interests

    def tagged_interests(self):
        tags = self.user.profile.tags.all()
        checked = []
        for tag in tags:
            checked.append(tag.name)
        return checked

    def locations(self):
        locations = ["High Sec", "Low Sec", "0.0 Sec", "Wormhole Space"]
        return locations

    def tagged_locations(self):
        tags = self.user.profile.tags.all()
        checked = []
        for tag in tags:
            checked.append(tag.name)
        return checked


def validate_avatar(postdata, user):
    try:
        pk = int(postdata['character'])
    except ValueError:
        return False

    try:
        character = CharacterApi.objects.get(pk=pk, api__user=user)
        return character
    except CharacterApi.DoesNotExist:
        return False
