from django.db import models

# Create your models here.

class Items(models.Model):
    name = models.CharField(max_length=200)
    price = models.DecimalField(decimal_places=2, max_digits=4)
    in_stock = models.BooleanField(default=True)

class City(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = 'cities'