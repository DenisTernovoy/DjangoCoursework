from django.urls import path
from .apps import MailingConfig
from . import views


app_name = MailingConfig.name

urlpatterns = [
    path("", views.MailingView.as_view(), name="mailings"),
    path("clients/", views.ClientListView.as_view(), name="clients"),
    path("clients/create/", views.ClientCreateView.as_view(), name="client_form"),
    path("clients/<int:pk>/", views.ClientDetailView.as_view(), name="client_detail"),
    path(
        "clients/<int:pk>/update",
        views.ClientUpdateView.as_view(),
        name="client_update",
    ),
    path(
        "clients/<int:pk>/delete",
        views.ClientDeleteView.as_view(),
        name="client_delete",
    ),
]
