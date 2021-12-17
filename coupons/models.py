from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Coupon(models.Model):
    """ Модель Купона """

    coupon_code = models.CharField(max_length=50, unique=True,
                                   verbose_name="Название купона")
    coupon_valid_form = models.DateTimeField(
        verbose_name="Начало действия купона")
    coupon_valid_to = models.DateTimeField(
        verbose_name="Время окончания купона")
    coupon_discount = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    coupon_active = models.BooleanField(verbose_name="Активный купон?")

    def __str__(self):
        return self.coupon_code
