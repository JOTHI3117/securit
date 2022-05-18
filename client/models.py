from django.db import models

# Create your models here.


class Client(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50, unique=True)
    password = models.CharField(max_length=20)


class Client_Details(models.Model):
    name = models.CharField(max_length=20)
    email = models.EmailField(max_length=50)
    company_name = models.CharField(max_length=50)
    company_email = models.EmailField(max_length=50, unique=True)
    contact = models.BigIntegerField()
    address = models.CharField(max_length=50)
    mac = models.CharField(max_length=50)

