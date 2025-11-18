from django import forms

from config.mixins import StyleFormMixin
from mailing.models import Client, Message, Mailing


class ClientForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Client
        fields = "__all__"


class MessageForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Message
        fields = "__all__"


class MailingForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Mailing
        exclude = (
            "timestamp_start",
            "timestamp_end",
            "status",
        )
        widgets = {
            "clients": forms.CheckboxSelectMultiple(),
        }
