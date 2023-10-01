from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models

class User(AbstractUser):
    """Изменённая модель пользователя"""
    experience = models.IntegerField()
    balance = models.IntegerField(null=True)

    def save(self, *args, **kwargs):
        if self.balance < 0:
            raise ValidationError("Баланс не может быть отрицательным.")
        super().save(*args, **kwargs)

class TypeOfOperations(models.Model):
    "Модель типа операций"
    title = models.CharField(max_length=50)

class Operations(models.Model):
    "Модель операций пользователя"
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="operations")
    amount = models.IntegerField()
    type_operations = models.ForeignKey(TypeOfOperations, on_delete=models.CASCADE)
    date = models.DateTimeField()
    source = models.CharField(max_length=50)
