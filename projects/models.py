from django.db import models
from django.utils import timezone

class mdl_Project(models.Model):
    prj_id = models.IntegerField(default=0)
    prj_name = models.CharField(max_length=200)

class mdl_Task(models.Model):
    project = models.ForeignKey(mdl_Project, on_delete=models.CASCADE)
    tsk_name = models.CharField(max_length=200)
    tsk_date_start = models.DateTimeField(verbose_name = 'date start', default=timezone.now)
    tsk_date_end = models.DateTimeField(verbose_name = 'date end', default=timezone.now)
