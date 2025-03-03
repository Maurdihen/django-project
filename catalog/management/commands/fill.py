from django.core.management.base import BaseCommand
from catalog.models import Category, Product


class Command(BaseCommand):

    def handle(self, *args, **options):
        Category.objects.all().delete()
        Product.objects.all().delete()

        category1 = Category.objects.create(name="Электроника", description="Гаджеты и устройства")
        category2 = Category.objects.create(name="Книги", description="Художественная и научная литература")

        Product.objects.create(
            name="Смартфон",
            description="Флагманский смартфон",
            category=category1,
            unit_price=1000
        )

        Product.objects.create(
            name="Ноутбук",
            description="Игровой ноутбук",
            category=category1,
            unit_price=1500
        )

        Product.objects.create(
            name="Книга '1984'",
            description="Антиутопия Джорджа Оруэлла",
            category=category2,
            unit_price=20
        )


