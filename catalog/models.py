from django.db import models
from django.urls import reverse

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


class BlogPost(models.Model):
    title = models.CharField(max_length=255, verbose_name='Заголовок')
    slug = models.CharField(max_length=255, unique=True, verbose_name='URL')
    content = models.TextField(verbose_name='Содержимое')
    preview = models.ImageField(upload_to='blog/', verbose_name='Превью', blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    is_published = models.BooleanField(default=False, verbose_name='Опубликовано')
    views_count = models.IntegerField(default=0, verbose_name='Количество просмотров')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog_detail', kwargs={'slug': self.slug})

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'
        ordering = ['-created_at']
