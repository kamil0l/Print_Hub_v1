from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from .constants import USER_TYPE_CHOICES



class Printer(models.Model):
    name = models.CharField(max_length=123)
    head = models.IntegerField()
    max_temperature = models.IntegerField()
    max_speed = models.IntegerField()
    image = models.ImageField(upload_to='printer_images/', null=True, blank=True)

    def __str__(self):
        return self.name


class Filament(models.Model):
    name = models.CharField(max_length=123)
    producer = models.CharField(max_length=123)
    material = models.CharField(max_length=12)
    colour = models.CharField(max_length=24)
    temperature_min = models.IntegerField()
    temperature_max = models.IntegerField()
    weight = models.IntegerField()

    def __str__(self):
        return f"{self.name} ({self.colour}) - {self.weight}g"

class Project(models.Model):
    name = models.CharField(max_length=256)
    printer = models.ForeignKey(Printer, on_delete=models.SET_NULL, null=True)
    material = models.ForeignKey(Filament, on_delete=models.SET_NULL, null=True)
    filament_needed = models.IntegerField(default=0)
    print_time = models.IntegerField(default=0)
    image = models.ImageField(upload_to='project_images/', null=True, blank=True)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, default=None)

    def __str__(self):
        return self.name

class Parts(models.Model):
    name = models.CharField(max_length=123)
    description = models.CharField(max_length=256)
    printers = models.ManyToManyField(Printer)

    def __str__(self):
        return self.name


class PrintingQue(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True)
    order = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.project.name

    class Meta:
        ordering = ["order"]

class UserProfile(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, null=True, blank=True, default=None)
