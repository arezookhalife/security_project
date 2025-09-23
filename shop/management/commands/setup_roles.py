from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission

from shop.models import Product


class Command(BaseCommand):
    help = "Create default groups and assign permissions"

    def handle(self, *args, **kwargs):
        admin_group, _ = Group.objects.get_or_create(name='Admin')
        viewer_group, _ = Group.objects.get_or_create(name='viewer')

        ct = ContentType.objects.get_for_model(Product)
        can_edit = Permission.objects.get(content_type=ct, codename='can_edit_product')
        can_view = Permission.objects.get(content_type=ct, codename='can_view_product')

        admin_group.permissions.add(can_edit)
        viewer_group.permissions.add(can_view)

        self.stdout.write(self.style.SUCCESS("Groups and permissions are created."))



