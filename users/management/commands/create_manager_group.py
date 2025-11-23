from django.contrib.auth.models import Group, Permission
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        Group.objects.all().delete()

        group = Group.objects.create(name="Manager")

        permission = Permission.objects.get(codename="can_watch_clients")
        permission1 = Permission.objects.get(codename="can_watch_messages")
        permission2 = Permission.objects.get(codename="can_watch_mailings")
        permission3 = Permission.objects.get(codename="can_pause_mailings")
        permission4 = Permission.objects.get(codename="can_watch_users")
        permission5 = Permission.objects.get(codename="can_block_users")

        group.permissions.add(
            permission, permission1, permission2, permission3, permission4, permission5
        )

        group.save()
