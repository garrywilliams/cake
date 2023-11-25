from django.core.validators import MaxValueValidator, MinValueValidator, URLValidator
from django.db import models


class Cake(models.Model):
    name = models.CharField(max_length=30)
    comment = models.CharField(max_length=200)
    imageUrl = models.URLField(validators=[URLValidator()])
    yumFactor = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
