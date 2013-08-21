from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.utils.safestring import mark_safe
from stormpath.client import Client
from stormpath.error import Error
from django.conf import settings
from django.forms.forms import NON_FIELD_ERRORS
from django.forms import ValidationError

class HorizontalRadioRenderer(forms.RadioSelect.renderer):
  def render(self):
    return mark_safe(u'\n'.join(u'%s\n' % w for w in self))

class UserCreateForm(UserCreationForm):

    ACC_CHOICES = (('Admins', 'Administrator',),
        ('Premiums', 'Premium',),
        ('Basics', 'Basic'))

    email = forms.EmailField(required=True)
    account_type = forms.ChoiceField(
        widget=forms.RadioSelect(renderer=HorizontalRadioRenderer),
        choices=ACC_CHOICES,
        initial='Basics')

    class Meta:
        model = User
        fields = ("username", "email",
            "first_name", "last_name","password1", "password2", "account_type")

    def save(self, commit=True):
        client = Client(api_key={'id': settings.STORMPATH_ID,
            'secret': settings.STORMPATH_SECRET})
        application = client.applications.get(settings.STORMPATH_APPLICATION)

        data = self.cleaned_data
        stormpath_data = {}

        if 'password1' in data:
            stormpath_data['password'] = data['password1']

        stormpath_data['username'] = data['username']
        stormpath_data['email'] = data['email']
        stormpath_data['given_name'] = data['first_name']
        stormpath_data['surname'] = data['last_name']

        try:
            account = application.accounts.create(stormpath_data)
        except Error as e:
            self._errors[NON_FIELD_ERRORS] = self.error_class([e.message])
            raise ValidationError(e.message)

        if data['account_type'] == 'Admins':
            admin_group = client.groups.get(settings.STORMPATH_ADMINISTRATORS)
            account.add_group(admin_group)
            account.save()
        elif data['account_type'] == 'Premiums':
            premium_group = client.groups.get(settings.STORMPATH_PREMIUMS)
            account.add_group(premium_group)
            account.save()
