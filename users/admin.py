from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from users.models import CustomUser


# Register your models here.
@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = (
        "email",
        "username",
        "phone",
        "country",
    )
    search_fields = (
        "email",
        "username",
        "phone",
        "country",
    )
    ordering = ("email",)
