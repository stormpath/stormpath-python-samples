from django import forms
from django.contrib.auth import get_user_model
from django.utils.safestring import mark_safe
from stormpath.client import Client
from stormpath.error import Error
from django.conf import settings
from django.forms.forms import NON_FIELD_ERRORS
from django.forms import ValidationError

class HorizontalRadioRenderer(forms.RadioSelect.renderer):
  def render(self):
    return mark_safe(u'\n'.join(u'%s\n' % w for w in self))

class UserCreateForm(forms.ModelForm):

    ACC_CHOICES = (('Admins', 'Administrator',),
        ('Premiums', 'Premium',),
        ('Basics', 'Basic'))

    password = forms.CharField(label='Password',
        widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation',
        widget=forms.PasswordInput)
    account_type = forms.ChoiceField(
        widget=forms.RadioSelect(renderer=HorizontalRadioRenderer),
        choices=ACC_CHOICES,
        initial='Basics')

    class Meta:
        model = get_user_model()
        fields = ("username", "email",
            "given_name", "middle_name", "surname", "password", "password2",
            "account_type")

    def clean_password2(self):
        password = self.cleaned_data.get("password")
        password2 = self.cleaned_data.get("password2")
        if password and password2 and password != password2:
            msg = "Passwords don't match"
            raise forms.ValidationError(msg)
        return password2

    def save(self, commit=True):
        client = Client(api_key={'id': settings.STORMPATH_ID,
            'secret': settings.STORMPATH_SECRET})
        application = client.applications.get(settings.STORMPATH_APPLICATION)

        data = self.cleaned_data
        account_type = data['account_type']
        del data['account_type']
        del data['password2']

        try:
            account = application.accounts.create(data)
        except Error as e:
            self._errors[NON_FIELD_ERRORS] = self.error_class([e.message])
            raise ValidationError(e.message)

        if account_type == 'Admins':
            admin_group = client.groups.get(settings.STORMPATH_ADMINISTRATORS)
            account.add_group(admin_group)
            account.save()
        elif account_type == 'Premiums':
            premium_group = client.groups.get(settings.STORMPATH_PREMIUMS)
            account.add_group(premium_group)
            account.save()
