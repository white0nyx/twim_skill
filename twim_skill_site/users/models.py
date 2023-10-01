from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models

class User(AbstractUser):
    """Изменённая модель пользователя"""
    experience = models.IntegerField(verbose_name='Опыт')
    balance = models.IntegerField(null=True, verbose_name='Баланс')

    def save(self, *args, **kwargs):
        if self.balance < 0:
            raise ValidationError("Баланс не может быть отрицательным.")
        super().save(*args, **kwargs)

class TypeOfOperations(models.Model):
    "Модель типа операций"
    title = models.CharField(max_length=50, verbose_name='Заголовок')

class Operations(models.Model):
    "Модель операций пользователя"
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="operations", verbose_name='Пользователь')
    amount = models.IntegerField(verbose_name='Сумма')
    type_operations = models.ForeignKey(TypeOfOperations, on_delete=models.CASCADE, verbose_name='Тип операции')
    date = models.DateTimeField(verbose_name='Дата операции')
    source = models.CharField(max_length=50, verbose_name='Источник операции')
