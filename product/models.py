from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.utils.timezone import now

class Category(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название категории")
    slug = models.SlugField(max_length=255, unique=True, blank=True, verbose_name="slug")
    description = models.TextField(blank=True, null=True)
    is_disabled = models.BooleanField(default=False, verbose_name="Отключена")

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class Product(models.Model):
    name = models.CharField(max_length=200) 
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    card_description = models.TextField()
    description = models.TextField()  
    price = models.DecimalField(max_digits=10, decimal_places=0)
    discount = models.DecimalField(max_digits=5, decimal_places=0, default=0) 
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)  
    slug = models.SlugField(unique=True) 
    file = models.FileField(upload_to='product_files/', blank=True, null=True, verbose_name="Файл для скачивания")
    is_best_seller = models.BooleanField(default=False, verbose_name="Хит продаж")  # новое поле

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_discounted_price(self):
        """Метод для получения цены со скидкой"""
        return self.price * (1 - self.discount / 100)
    
    def get_absolute_url(self):
        return reverse('product:product_detail', kwargs={'category_slug': self.category.slug, 'product_slug': self.slug})


    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Продукты"
        verbose_name_plural = "Продукты"


class PromoCode(models.Model):
    code = models.CharField(max_length=50, unique=True, verbose_name="Код промокода")
    discount = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Скидка (%)")
    start_date = models.DateTimeField(default=now, verbose_name="Дата начала действия")
    end_date = models.DateTimeField(verbose_name="Дата окончания действия")
    is_active = models.BooleanField(default=True, verbose_name="Активен")
    usage_limit = models.PositiveIntegerField(default=1, verbose_name="Лимит использования")
    times_used = models.PositiveIntegerField(default=0, verbose_name="Количество использований")

    def is_valid(self):
        """Проверяем, действует ли промокод."""
        return (
            self.is_active and
            self.start_date <= now() <= self.end_date and
            self.times_used < self.usage_limit
        )

    def __str__(self):
        return self.code

    class Meta:
        verbose_name = "Промокод"
        verbose_name_plural = "Промокоды"
