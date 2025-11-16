from django import forms

from config.forms import StyleFormMixin
from mailing.models import Client


class ClientForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Client
        fields = "__all__"
