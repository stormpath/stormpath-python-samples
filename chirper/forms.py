from django import forms
from .models import Chirp

class ChirpForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
            super(ChirpForm, self).__init__(*args, **kwargs)
            self.fields['message'].widget.attrs['rows'] = 3
            self.fields['message'].widget.attrs['placeholder'] = \
                "Compose your chirp here..."

    class Meta:
        model = Chirp
        exclude = ("user")
