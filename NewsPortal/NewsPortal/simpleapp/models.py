from django.db import models
from django.core.validators import MinValueValidator


class NewsPortal(models.Model):
    name = models.CharField(
        max_length=50,
        unique=True,
    )
    description = models.TextField()
    quantity = models.IntegerField(
        validators=[MinValueValidator(0)],
    )

    time_pub = models.DateField(null=True, blank=True)
    category = models.ForeignKey(
        to='Category',
        on_delete=models.CASCADE,
        related_name='news',
    )
    price = models.FloatField(
        validators=[MinValueValidator(0.0)],
    )

    def __str__(self):
        return f'{self.name.title()}___{self.time_pub}___{self.description}'


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name.title()
