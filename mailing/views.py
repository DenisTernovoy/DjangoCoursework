from django.core.mail import send_mail
from django.utils import timezone
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from mailing.forms import ClientForm, MessageForm, MailingForm
from mailing.models import Client, Mailing, Message, Attempt

import time


# Create your views here.
class ClientListView(ListView):
    model = Client
    context_object_name = "clients"


class ClientCreateView(CreateView):
    form_class = ClientForm
    template_name = "mailing/client_form.html"
    success_url = reverse_lazy("mailing:clients")


class ClientDetailView(DetailView):
    model = Client


class ClientUpdateView(UpdateView):
    model = Client
    form_class = ClientForm
    template_name = "mailing/client_form.html"
    success_url = reverse_lazy("mailing:clients")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["change_flag"] = True

        return context


class ClientDeleteView(DeleteView):
    model = Client
    template_name = "mailing/client_confirm_delete.html"
    success_url = reverse_lazy("mailing:clients")


class MessageListView(ListView):
    model = Message
    context_object_name = "messages"


class MessageCreateView(CreateView):
    form_class = MessageForm
    template_name = "mailing/message_form.html"
    success_url = reverse_lazy("mailing:messages")


class MessageDetailView(DetailView):
    model = Message


class MessageUpdateView(UpdateView):
    model = Message
    form_class = MessageForm
    template_name = "mailing/message_form.html"
    success_url = reverse_lazy("mailing:messages")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["change_flag"] = True

        return context


class MessageDeleteView(DeleteView):
    model = Message
    template_name = "mailing/message_confirm_delete.html"
    success_url = reverse_lazy("mailing:messages")


class MailingListView(ListView):
    model = Mailing
    context_object_name = "mailings"


class MailingCreateView(CreateView):
    form_class = MailingForm
    template_name = "mailing/mailing_form.html"
    success_url = reverse_lazy("mailing:mailings")


class MailingDetailView(DetailView):
    model = Mailing


class MailingUpdateView(UpdateView):
    model = Mailing
    form_class = MailingForm
    template_name = "mailing/mailing_form.html"
    success_url = reverse_lazy("mailing:mailings")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["change_flag"] = True

        return context


class MailingDeleteView(DeleteView):
    model = Mailing
    template_name = "mailing/mailing_confirm_delete.html"
    success_url = reverse_lazy("mailing:mailings")


class MailingView(TemplateView):
    model = Mailing
    template_name = "mailing/mailing_main.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        mailings = Mailing.objects.all().count()
        mailings_active = Mailing.objects.all().filter(status="active").count()
        clients = Client.objects.all().count()

        context["count"] = {
            "mailings": mailings,
            "mailings_active": mailings_active,
            "clients": clients,
        }

        return context


class AttemptListView(ListView):
    model = Attempt
    context_object_name = "attempts"


def run_mailing(request, pk):
    mailing = Mailing.objects.get(id=pk)
    mailing.status = "active"
    mailing.timestamp_start = timezone.now()
    mailing.save()

    for client in mailing.clients.all():
        send_mail(
            mailing.message.title,
            mailing.message.message,
            from_email="test@test.ru",
            recipient_list=["test1@test.ru"],
        )
        attempt = Attempt.objects.create(
            datetime_attempt=timezone.now(),
            status="OK",
            response="OK",
            mailing=mailing,
            recipient=client,
        )
        attempt.save()
        time.sleep(15)

    mailing.timestamp_end = timezone.now()
    mailing.status = "stopped"
    mailing.save()

    return redirect("mailing:mailings")


def stop_mailing(request, pk):
    mailing = Mailing.objects.get(id=pk)
    mailing.status = "stopped"
    mailing.timestamp_end = timezone.now()
    mailing.save()
