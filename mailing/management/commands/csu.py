from django.contrib.auth.models import User
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        User.objects.all().delete()
        user = User.objects.create(username="admin")
        user.set_password("12345")
        user.is_active = True
        user.is_superuser = True
        user.save()
