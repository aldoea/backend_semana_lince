from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.

class User(AbstractUser):
    control_number = models.CharField(primary_key=True, max_length=20)
    name = models.CharField(max_length=200)
    semester = models.PositiveSmallIntegerField()
    department = models.ForeignKey('semana_lince.Department', on_delete=models.CASCADE)


class Department(models.Model):
    name = models.CharField(max_length=100)


class ActivityType(models.Model):
    name = models.CharField(max_length=100)


class Location(models.Model):
    name = models.CharField(max_length=200)


class Speaker(models.Model):
    name = models.CharField(max_length=200, unique=True)


class ActivityCategory(models.Model):
    name = models.CharField(max_length=120)


class Responsable(models.Model):
    name = models.CharField(max_length=200, blank=True, null=True)
    department = models.ForeignKey('semana_lince.Department', on_delete=models.CASCADE, null=True)

    class Meta:
        ordering = ('id',)


class Activity(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    category = models.ForeignKey('semana_lince.ActivityCategory', on_delete=models.CASCADE, null=True)
    department = models.ForeignKey('semana_lince.Department', on_delete=models.CASCADE)
    responsable = models.ForeignKey('semana_lince.Responsable', on_delete=models.CASCADE, default=0)
    activity_type = models.ForeignKey('semana_lince.ActivityType', on_delete=models.CASCADE, null=True)
    external = models.BooleanField(default=False)
    participant_material = models.CharField(max_length=512)
    speaker_material = models.CharField(max_length=512)

    class Meta:
        ordering = ('id',)


class Event(models.Model):
    activity = models.ForeignKey('semana_lince.Activity', on_delete=models.CASCADE)
    capacity = models.PositiveIntegerField(default=30)
    date = models.DateField()
    starts_at = models.TimeField(null=True)
    ends_at = models.TimeField(null=True)
    location = models.ForeignKey('semana_lince.Location', on_delete=models.CASCADE)
    speakers = models.ManyToManyField('semana_lince.Speaker')

    class Meta:
        ordering = ('id',)


class Assistance(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    event = models.ForeignKey('semana_lince.Event', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('id',)
        unique_together = ('user', 'event', 'created')
