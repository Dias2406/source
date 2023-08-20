from django.db import models
from django.db.models.signals import pre_save
from django.utils.text import slugify
from django.conf import settings

# Create your models here.

class Teacher(models.Model):
    account             = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


    def __str__(self):
        return self.account.email
