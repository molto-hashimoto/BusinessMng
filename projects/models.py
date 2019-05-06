from django.db import models
from django.utils import timezone
from users.models import User

CHOICES_STATUS = (
    ('New', 'New'),
    ('Waiting', 'Waiting'),
    ('Working', 'Working'),
    ('completed', 'completed'),
    ('discontinued', 'discontinued'),
    ('pending', 'pending'),
)

class mdl_Project(models.Model):

    name = models.CharField(max_length=200, null=True)
    status = models.CharField(max_length=10, null=True, choices=CHOICES_STATUS)
    member = models.ManyToManyField(User, blank=True)
    partner = models.CharField(max_length=200, null=True)
    note = models.CharField(max_length=500, null=True, blank=True)

    def __str__(self):
        return self.name

class mdl_Task(models.Model):
    project = models.ForeignKey(mdl_Project, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    status = models.CharField(max_length=10, null=True, choices=CHOICES_STATUS)
    member = models.ManyToManyField(User, blank=True)
    start = models.DateField(verbose_name = 'date start', default=timezone.now)
    end = models.DateField(verbose_name = 'date end', default=timezone.now)
    note = models.CharField(max_length=500, null=True, blank=True)

    def __str__(self):
        return self.name
