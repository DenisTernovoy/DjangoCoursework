from django.contrib import admin
from .models import *

# Register your models here.


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = (
        "email",
        "name",
        "comment",
    )


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "message",
    )


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = (
        "timestamp_start",
        "timestamp_end",
        "status",
        "message",
    )


@admin.register(Attempt)
class AttemptAdmin(admin.ModelAdmin):
    list_display = (
        "datetime_attempt",
        "status",
        "response",
        "mailing",
    )
