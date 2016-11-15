from django.db import models
from django.conf import settings

# Create your models here.
class Picture(models.Model):
    # user =models.ForeignKey(settings.AUTH_USER_MODEL)
    sourceip =models.CharField(max_length=127 ,blank=True)
    #投标人身份证
    identity =models.CharField(max_length=127 ,blank=True)
    url = models.CharField(max_length=127)
    code =models.CharField(max_length=127 ,blank=True)
    mounth =models.CharField(max_length=127 ,blank=True)
    isYanxi =models.BooleanField(default=False)
#
# ###记录码工打码情况
# class DamaDetail(models.Model):
#     user =models.ForeignKey(settings.AUTH_USER_MODEL)
#     sourceip =models.CharField(max_length=32 ,blank=True)
#     pub_date = models.DateTimeField('date published')
#     during =models.FloatField()
#     isRight =models.BooleanField(default=False)
#
# class Dama(models.Model):
#     user =models.ForeignKey(settings.AUTH_USER_MODEL)
#     times =models.IntegerField(default=0)
#     rtimes =models.IntegerField(default=0)
#     wtimes =models.IntegerField(default=0)


