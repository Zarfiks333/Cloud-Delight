from django.db import models
from django.urls import reverse
from django.utils.text import slugify

class Service(models.Model):
    name = models.CharField(max_length=255)
    card_description = models.TextField()
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=0)
    image = models.ImageField(upload_to='services/', null=True, blank=True)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)  # Генерация slug на основе name
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('services:service_detail', kwargs={'slug': self.slug})

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Услуги"
        verbose_name_plural = "Услуги"

