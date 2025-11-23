from django.core.management.base import BaseCommand
from mailing.models import Mailing
from mailing.views import run_mailing


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument("id", type=int)

    def handle(self, *args, **options):
        try:
            mailing = Mailing.objects.get(id=options["id"])
            if mailing.status in ("active", "stopped"):
                return "Рассылка уже была запущена"
            return run_mailing(None, mailing.pk)
        except Mailing.DoesNotExist:
            return "Рассылки с таким id не существует"
