from django.db import models


# Create your models here.
class Company(models.Model):
    name = models.CharField(max_length=20, null=True)
    email = models.EmailField(max_length=20, unique=True, null=True)
    password = models.CharField(max_length=20, null=True)
