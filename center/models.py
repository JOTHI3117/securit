from django.db import models
from user.models import *
from client.models import *


# Create your models here.


class Center(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50, unique=True)
    password = models.CharField(max_length=20)


class Requests_Client(models.Model):
    client_details = models.ForeignKey(Client_Details, on_delete=models.CASCADE, default=0)
    email = models.EmailField(max_length=50, null=True)
    client_email = models.EmailField(max_length=50, null=True)
    file_name = models.CharField(max_length=50, null=True)
    user_file = models.FileField(upload_to='request/', null=True)
    same = models.BooleanField(default=False)
    temporary_mac = models.BooleanField(default=False)
    different = models.BooleanField(default=False)
    mac = models.CharField(max_length=50, null=True)
    sent_organization = models.BooleanField(default=False)


class Change_Mac(models.Model):
    client = models.ForeignKey(Client_Details, on_delete=models.CASCADE)
    email = models.EmailField(max_length=50)
    client_email = models.EmailField(max_length=50, null=True)
    different_mac = models.BooleanField(default=False)
    question_link = models.BooleanField(default=False)
    file_name = models.CharField(max_length=50, null=True)
    files = models.FileField(upload_to='request/', null=True)
    correct = models.BooleanField(default=False)
    current_mac = models.CharField(max_length=50, null=True)
    sent_user = models.BooleanField(default=False)
    again_link = models.BooleanField(default=False)
    approve = models.BooleanField(default=False)
    director_sent = models.BooleanField(default=False)
    security = models.CharField(max_length=20, null=True)
