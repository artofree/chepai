from django.db import models
from django.conf import settings

# Create your models here.
class Picture(models.Model):
    username =models.CharField(max_length=127 ,blank=True)
    sourceip =models.CharField(max_length=127 ,blank=True)
    #投标人身份证
    identity =models.CharField(max_length=127 ,blank=True)
    url = models.CharField(max_length=127)
    code =models.CharField(max_length=127 ,blank=True)
    mounth =models.CharField(max_length=127 ,blank=True)

