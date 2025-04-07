from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from catalog.models import Product

class Command(BaseCommand):
    help = 'Creates moderator group with necessary permissions'

    def handle(self, *args, **kwargs):
        moderator_group, created = Group.objects.get_or_create(name='Moderators')
        
        product_content_type = ContentType.objects.get_for_model(Product)
        
        permissions = Permission.objects.filter(
            content_type=product_content_type,
            codename__in=[
                'can_unpublish_product',
                'can_edit_description',
                'can_change_category',
                'change_product',
            ]
        )
        
        moderator_group.permissions.add(*permissions)
        
        self.stdout.write(
            self.style.SUCCESS('Successfully created moderator group with permissions')
        ) 