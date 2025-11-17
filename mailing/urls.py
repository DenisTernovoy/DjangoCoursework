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
    path("messages/", views.MessageListView.as_view(), name="messages"),
    path("messages/create/", views.MessageCreateView.as_view(), name="message_form"),
    path(
        "messages/<int:pk>/", views.MessageDetailView.as_view(), name="message_detail"
    ),
    path(
        "messages/<int:pk>/update",
        views.MessageUpdateView.as_view(),
        name="message_update",
    ),
    path(
        "messages/<int:pk>/delete",
        views.MessageDeleteView.as_view(),
        name="message_delete",
    ),
    path("mailings/", views.MailingListView.as_view(), name="mailings"),
    path("mailings/create/", views.MailingCreateView.as_view(), name="mailing_form"),
    path(
        "mailings/<int:pk>/", views.MailingDetailView.as_view(), name="mailing_detail"
    ),
    path(
        "mailings/<int:pk>/update",
        views.MailingUpdateView.as_view(),
        name="mailing_update",
    ),
    path(
        "mailings/<int:pk>/delete",
        views.MailingDeleteView.as_view(),
        name="mailing_delete",
    ),
]
