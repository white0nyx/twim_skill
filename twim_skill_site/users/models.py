from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models

class User(AbstractUser):
    """Изменённая модель пользователя"""
    experience = models.IntegerField(verbose_name='Опыт')
    balance = models.DecimalField(max_digits=8, decimal_places=2, null=True, verbose_name='Баланс')
 
class TypeOfOperations(models.Model):
    "Модель типа операций"
    name = models.CharField(max_length=50, verbose_name='Название')

class Operations(models.Model):
    "Модель операций пользователя"
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="operations", verbose_name='Пользователь')
    amount = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='Сумма')
    type_operations = models.ForeignKey(TypeOfOperations, on_delete=models.CASCADE, verbose_name='Тип операции')
    date = models.DateTimeField(auto_now=True, verbose_name='Дата операции')

class OperationsGame(models.Model):
    operation = models.ForeignKey(Operations, on_delete=models.CASCADE, related_name="operations_games", verbose_name="Операция")
    game = models.IntegerField(verbose_name="Матч")

