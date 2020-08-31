from django.db import models
from django.utils.translation import gettext_lazy as _


# Create your models here.
class Stonk(models.Model):
    """
    Stonk class.
    """

    class HalalStatus(models.TextChoices):
        """Provides three options, halal, non-halal and questionable"""

        HALAL = "Y", _("Halal")
        NOT_HALAL = "N", _("Not halal")
        QUES = "Q", _("Questionable")

    ticker = models.CharField(primary_key=True, max_length=10)
    name = models.CharField(max_length=200)
    price = models.FloatField()
    halal_status = models.CharField(
        max_length=2,
        choices=HalalStatus.choices,
        default=HalalStatus.NOT_HALAL,
    )
    annual_dividend = models.FloatField()
    dividend_per_dollar = models.FloatField()
    market_cap = models.PositiveBigIntegerField()
    volume = models.PositiveBigIntegerField()

    @property
    def get_dividend_per_dollar(self):
        """Gets dividend per dollar invested"""
        return self.annual_dividend / self.price

    def save(self, *args, **kwargs):
        self.dividend_per_dollar = self.get_dividend_per_dollar()
        super().save(*args, **kwargs)
