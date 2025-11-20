from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.utils import timezone
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.generic import ListView, DetailView, TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from mailing.forms import ClientForm, MessageForm, MailingForm
from mailing.models import Client, Mailing, Message, Attempt
from mailing.services import send_simple_email, get_messages_list
from django.core.cache import cache


# Create your views here.
class ClientListView(LoginRequiredMixin, ListView):
    model = Client
    context_object_name = "clients"

    def get_queryset(self):
        if self.request.user.has_perm("can_watch_clients"):
            return Client.objects.all()
        return Client.objects.filter(owner=self.request.user)


class ClientCreateView(LoginRequiredMixin, CreateView):
    form_class = ClientForm
    template_name = "mailing/client_form.html"
    success_url = reverse_lazy("mailing:clients")

    def get_context_data(self, **kwargs):
        if self.request.user.groups.filter(name="Manager").exists():
            raise PermissionDenied
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        client = form.save(commit=False)
        client.owner = self.request.user
        client.save()

        return super().form_valid(form)


@method_decorator(cache_page(60), name="dispatch")
class ClientDetailView(LoginRequiredMixin, DetailView):
    model = Client

    def get_context_data(self, **kwargs):
        client = Client.objects.get(id=self.object.id)
        if self.request.user != client.owner and not self.request.user.has_perm(
            "can_watch_clients"
        ):
            raise PermissionDenied

        return super().get_context_data(**kwargs)


class ClientUpdateView(LoginRequiredMixin, UpdateView):
    model = Client
    form_class = ClientForm
    template_name = "mailing/client_form.html"
    success_url = reverse_lazy("mailing:clients")

    def get_context_data(self, **kwargs):
        if self.request.user.groups.filter(name="Manager").exists():
            raise PermissionDenied
        return super().get_context_data(**kwargs)

        context = super().get_context_data(**kwargs)
        context["change_flag"] = True

        return context


class ClientDeleteView(LoginRequiredMixin, DeleteView):
    model = Client
    template_name = "mailing/client_confirm_delete.html"
    success_url = reverse_lazy("mailing:clients")

    def get_context_data(self, **kwargs):
        if self.request.user != self.object.owner:
            raise PermissionDenied
        return super().get_context_data(**kwargs)


class MessageListView(LoginRequiredMixin, ListView):
    model = Message
    context_object_name = "messages"

    def get_queryset(self):
        if self.request.user.has_perm("can_watch_messages"):
            return Message.objects.all()
        return get_messages_list(self.request.user)


class MessageCreateView(LoginRequiredMixin, CreateView):
    form_class = MessageForm
    template_name = "mailing/message_form.html"
    success_url = reverse_lazy("mailing:messages")

    def get_context_data(self, **kwargs):
        if self.request.user.groups.filter(name="Manager").exists():
            raise PermissionDenied
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        message = form.save(commit=False)
        message.owner = self.request.user
        message.save()
        cache.delete(f"messages_of_{self.request.user}")

        return super().form_valid(form)


@method_decorator(cache_page(60), name="dispatch")
class MessageDetailView(LoginRequiredMixin, DetailView):
    model = Message

    def get_context_data(self, **kwargs):
        message = Message.objects.get(id=self.object.id)
        if self.request.user != message.owner and not self.request.user.has_perm(
            "can_watch_messages"
        ):
            raise PermissionDenied

        return super().get_context_data(**kwargs)


class MessageUpdateView(LoginRequiredMixin, UpdateView):
    model = Message
    form_class = MessageForm
    template_name = "mailing/message_form.html"
    success_url = reverse_lazy("mailing:messages")

    def get_context_data(self, **kwargs):
        if self.request.user != self.object.owner:
            raise PermissionDenied
        context = super().get_context_data(**kwargs)
        context["change_flag"] = True

        return context


class MessageDeleteView(LoginRequiredMixin, DeleteView):
    model = Message
    template_name = "mailing/message_confirm_delete.html"
    success_url = reverse_lazy("mailing:messages")

    def form_valid(self, form):
        cache.delete(f"messages_of_{self.request.user}")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        if self.request.user != self.object.owner:
            raise PermissionDenied
        return super().get_context_data(**kwargs)


class MailingListView(LoginRequiredMixin, ListView):
    model = Mailing
    context_object_name = "mailings"

    def get_queryset(self):
        if self.request.user.has_perm("can_watch_mailings"):
            return Mailing.objects.all()
        return Mailing.objects.filter(owner=self.request.user)


class MailingCreateView(LoginRequiredMixin, CreateView):
    form_class = MailingForm
    template_name = "mailing/mailing_form.html"
    success_url = reverse_lazy("mailing:mailings")

    def get_context_data(self, **kwargs):
        if self.request.user.groups.filter(name="Manager").exists():
            raise PermissionDenied
        return super().get_context_data(**kwargs)

    def get_form(self, form_class=MailingForm):
        form = super().get_form(form_class)
        form.fields["clients"].queryset = Client.objects.filter(owner=self.request.user)
        form.fields["message"].queryset = Message.objects.filter(
            owner=self.request.user
        )
        return form

    def form_valid(self, form):
        mailing = form.save(commit=False)
        mailing.owner = self.request.user
        mailing.save()

        return super().form_valid(form)


class MailingDetailView(LoginRequiredMixin, DetailView):
    model = Mailing

    def get_context_data(self, **kwargs):
        mailing = Mailing.objects.get(id=self.object.id)
        if self.request.user != mailing.owner and not self.request.user.has_perm(
            "can_watch_mailings"
        ):
            raise PermissionDenied

        return super().get_context_data(**kwargs)


class MailingUpdateView(LoginRequiredMixin, UpdateView):
    model = Mailing
    form_class = MailingForm
    template_name = "mailing/mailing_form.html"
    success_url = reverse_lazy("mailing:mailings")

    def get_context_data(self, **kwargs):
        if self.request.user != self.object.owner:
            raise PermissionDenied
        context = super().get_context_data(**kwargs)
        context["change_flag"] = True

        return context


class MailingDeleteView(LoginRequiredMixin, DeleteView):
    model = Mailing
    template_name = "mailing/mailing_confirm_delete.html"
    success_url = reverse_lazy("mailing:mailings")

    def get_context_data(self, **kwargs):
        if self.request.user != self.object.owner:
            raise PermissionDenied
        return super().get_context_data(**kwargs)


class MailingView(LoginRequiredMixin, TemplateView):
    model = Mailing
    template_name = "mailing/mailing_main.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        mailings = Mailing.objects.filter(owner=self.request.user).count()
        mailings_active = (
            Mailing.objects.filter(owner=self.request.user)
            .filter(status="active")
            .count()
        )
        clients = Client.objects.filter(owner=self.request.user).count()

        context["count"] = {
            "mailings": mailings,
            "mailings_active": mailings_active,
            "clients": clients,
        }

        return context


class AttemptListView(LoginRequiredMixin, ListView):
    model = Attempt
    context_object_name = "attempts"

    def get_queryset(self):
        if self.request.user.groups.filter(name="Managers").exists():
            return Attempt.objects.all()
        return Attempt.objects.filter(owner=self.request.user)


def run_mailing(request, pk):
    mailing = Mailing.objects.get(id=pk)
    mailing.status = "active"
    mailing.timestamp_start = timezone.now()
    mailing.save()

    for client in mailing.clients.all():
        response, status = send_simple_email(
            mailing.message.title,
            mailing.message.message,
            recipient=client.email,
        )
        attempt = Attempt.objects.create(
            datetime_attempt=timezone.now(),
            status=status,
            response=response,
            mailing=mailing,
            recipient=client,
            owner=request.user,
        )
        attempt.save()

    mailing.timestamp_end = timezone.now()
    mailing.status = "stopped"
    mailing.save()

    return redirect("mailing:mailings")


def stop_mailing(request, pk):
    mailing = Mailing.objects.get(id=pk)
    mailing.status = "stopped"
    mailing.timestamp_end = timezone.now()
    mailing.save()

    return redirect("mailing:mailings")


def pause_mailing(request, pk):
    mailing = Mailing.objects.get(id=pk)
    mailing.status = "paused"
    mailing.save()

    return redirect("mailing:mailings")


def active_mailing(request, pk):
    mailing = Mailing.objects.get(id=pk)
    mailing.status = "active"
    mailing.save()

    return redirect("mailing:mailings")


def report(request):
    attempts = Attempt.objects.filter(owner=request.user)
    attempts_all = attempts.count()
    attempts_success = attempts.filter(status="OK").count()

    context = {
        "attempts_all": attempts_all,
        "attempts_success": attempts_success,
    }

    return render(request, "mailing/mailing_report.html", context=context)
