from django.db import models

NULLABLE = {"null": True, "blank": True}


class Category(models.Model):
    name = models.CharField(max_length=50, verbose_name="имя")
    description = models.TextField(**NULLABLE, verbose_name="описание")


    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = "категория"
        verbose_name_plural = "категории"


class Product(models.Model):
    name = models.CharField(max_length=50, verbose_name="название")
    description = models.TextField(**NULLABLE, verbose_name="описание")
    image = models.ImageField(upload_to="product/", **NULLABLE, verbose_name="изображение")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="категория")
    unit_price = models.IntegerField(verbose_name="цена за штуку")
    data_created = models.DateField(**NULLABLE, verbose_name="дата создания")
    data_changed = models.DateField(**NULLABLE, verbose_name="дата последнего изменения")


    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = "продукт"
        verbose_name_plural = "продукты"
