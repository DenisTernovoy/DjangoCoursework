from django import forms

from config.forms import StyleFormMixin
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
        exclude = ("status",)
        widgets = {
            "timestamp_start": forms.DateTimeInput(
                attrs={
                    "type": "datetime-local",  # Задает тип входного поля
                }
            ),
            "timestamp_end": forms.DateTimeInput(
                attrs={
                    "type": "datetime-local",  # Задает тип входного поля
                }
            ),
            "clients": forms.CheckboxSelectMultiple(),
        }
