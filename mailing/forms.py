from django import forms

from config.mixins import StyleFormMixin
from mailing.models import Client, Message, Mailing


class ClientForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Client
        exclude = ("owner",)


class MessageForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Message
        exclude = ("owner",)


class MailingForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Mailing
        exclude = ("timestamp_start", "timestamp_end", "status", "owner")
        widgets = {
            "clients": forms.CheckboxSelectMultiple(),
        }
