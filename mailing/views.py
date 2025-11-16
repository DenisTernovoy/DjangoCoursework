from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from mailing.forms import ClientForm
from mailing.models import Client, Mailing


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


class MailingView(TemplateView):
    model = Mailing
    template_name = "mailing/mailing_list.html"
