from django.db import models
from django.contrib.auth.models import AbstractUser


class Inventory(models.Model):
    # Примерные поля, которые могут содержаться в инвентаре
    # Поле для хранения списка предметов в виде JSON или другого формата
    items = models.TextField()
    # Максимальная вместимость инвентаря
    capacity = models.IntegerField(default=100)

    def __str__(self):
        return f"Inventory (ID: {self.id})"


class Barracks(models.Model):
    # Примерные поля, которые могут содержаться в казарме
    # Поле для хранения списка героев в виде JSON или другого формата
    troops = models.TextField()
    max_level = models.IntegerField(default=1)  # Максимальный уровень прокачки

    def __str__(self):
        return f"Barracks (ID: {self.id})"


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    inventory = models.OneToOneField(
        Inventory, on_delete=models.CASCADE, null=True, blank=True)
    barracks = models.OneToOneField(
        Barracks, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        # Создание инвентаря и казармы при регистрации пользователя
        if not self.inventory:
            self.inventory = Inventory.objects.create()
        if not self.barracks:
            self.barracks = Barracks.objects.create()
        super(CustomUser, self).save(*args, **kwargs)
