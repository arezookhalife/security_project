from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission

class Command(BaseCommand):
    help = "ایجاد گروه‌ها و مجوزهای پایه"

    def handle(self, *args, **kwargs):
        admin_group, _ = Group.objects.get_or_create(name='Admin')
        viewer_group, _ = Group.objects.get_or_create(name='viewer')

        can_edit = Permission.objects.get(codename='can_edit_product')
        can_view = Permission.objects.get(codename='can_view_product')

        admin_group.permissions.add(can_edit)
        viewer_group.permissions.add(can_view)

        self.stdout.write(self.style.SUCCESS("Groups and permissions are created."))



