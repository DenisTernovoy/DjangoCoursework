from django.core.management.base import BaseCommand
from mailing.models import *


class Command(BaseCommand):
    def handle(self, *args, **options):
        Client.objects.all().delete()
        Message.objects.all().delete()
        Mailing.objects.all().delete()
        Attempt.objects.all().delete()
