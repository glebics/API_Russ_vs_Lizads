from django.db import models
from django.contrib.auth.models import AbstractUser


class Character(models.Model):
    name = models.CharField(max_length=100)
    base_attack = models.IntegerField()
    max_attack = models.IntegerField()
    base_defense = models.IntegerField()
    max_defense = models.IntegerField()
    base_attack_speed = models.FloatField()
    max_attack_speed = models.FloatField()
    base_health = models.IntegerField()
    max_health = models.IntegerField()
    # Максимальный уровень прокачки, одинаковый для всех персонажей
    max_level = models.IntegerField(default=100)

    def __str__(self):
        return self.name


class CharacterInstance(models.Model):
    character = models.OneToOneField(
        Character, on_delete=models.CASCADE)  # Связь с моделью Character
    barracks = models.OneToOneField('Barracks', on_delete=models.CASCADE,
                                    related_name='character_instance')  # Один к одному с казармой
    level = models.IntegerField(default=1)
    current_health = models.IntegerField()
    # Можно заменить на связь с моделью предметов
    equipped_items = models.TextField()

    def calculate_attack(self):
        return self.character.base_attack + (self.level * (self.character.max_attack - self.character.base_attack) // self.character.max_level)

    def calculate_defense(self):
        return self.character.base_defense + (self.level * (self.character.max_defense - self.character.base_defense) // self.character.max_level)

    def calculate_attack_speed(self):
        return self.character.base_attack_speed + (self.level * (self.character.max_attack_speed - self.character.base_attack_speed) // self.character.max_level)

    def calculate_health(self):
        return self.character.base_health + (self.level * (self.character.max_health - self.character.base_health) // self.character.max_level)

    def __str__(self):
        return f"{self.character.name} (Level {self.level}) in Barracks {self.barracks.id}"


class Equipment(models.Model):
    name = models.CharField(max_length=100)
    base_power = models.IntegerField()
    max_power = models.IntegerField()
    rarity = models.CharField(max_length=50)  # Параметр редкости
    # Максимальный уровень прокачки
    max_level = models.IntegerField(default=50)

    def __str__(self):
        return self.name


class EquipmentInstance(models.Model):
    # Один к одному с моделью Equipment
    equipment = models.OneToOneField(Equipment, on_delete=models.CASCADE)
    inventory = models.OneToOneField('Inventory', on_delete=models.CASCADE,
                                     related_name='equipment_instance')  # Один к одному с инвентарем
    level = models.IntegerField(default=1)

    def calculate_power(self):
        return self.equipment.base_power + (self.level * (self.equipment.max_power - self.equipment.base_power) // self.equipment.max_level)

    def __str__(self):
        return f"{self.equipment.name} (Level {self.level}) in Inventory {self.inventory.id}"


class Inventory(models.Model):
    player = models.OneToOneField(
        'CustomUser', on_delete=models.CASCADE, related_name='inventory')
    capacity = models.IntegerField(default=100)

    def __str__(self):
        return f"Inventory for {self.player.username}"


class Barracks(models.Model):
    player = models.OneToOneField(
        'CustomUser', on_delete=models.CASCADE, related_name='barracks')

    def __str__(self):
        return f"Barracks for {self.player.username}"


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    inventory = models.OneToOneField(
        Inventory, on_delete=models.CASCADE, null=True, blank=True)
    barracks = models.OneToOneField(
        Barracks, on_delete=models.CASCADE, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.inventory:
            self.inventory = Inventory.objects.create(player=self)
        if not self.barracks:
            self.barracks = Barracks.objects.create(player=self)
        super(CustomUser, self).save(*args, **kwargs)
