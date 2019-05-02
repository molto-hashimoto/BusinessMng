from django.db import models
from django.utils import timezone
from users.models import User

class mdl_Project(models.Model):

    CHOICES_PRJ_STATUS = (
        ('New', 'New'),
        ('Waiting', 'Waiting'),
        ('Working', 'Working'),
        ('completed', 'completed'),
        ('discontinued', 'discontinued'),
        ('pending', 'pending'),
    )

    name = models.CharField(max_length=200, null=True)
    status = models.CharField(max_length=10, null=True, choices=CHOICES_PRJ_STATUS)
    member = models.ManyToManyField(User, blank=True)
    note = models.CharField(max_length=500, null=True)

class mdl_Task(models.Model):
    project = models.ForeignKey(mdl_Project, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    start = models.DateField(verbose_name = 'date start', default=timezone.now)
    end = models.DateField(verbose_name = 'date end', default=timezone.now)
