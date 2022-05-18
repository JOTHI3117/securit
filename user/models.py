from django.db import models


# Create your models here.


class User(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50, unique=True)
    password = models.CharField(max_length=20)


class Company_Details(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    company_name = models.CharField(max_length=50)
    company_email = models.EmailField(max_length=50, unique=True)
    contact = models.BigIntegerField()
    address = models.CharField(max_length=50)
    approve = models.BooleanField(default=False)
    decline = models.BooleanField(default=False)
    question = models.BooleanField(default=False)


class File_Details(models.Model):
    company_email = models.ForeignKey(Company_Details, on_delete=models.CASCADE)
    email = models.EmailField(max_length=50)
    name = models.CharField(max_length=50, null=True)
    file_name = models.CharField(max_length=50)
    file_format = models.CharField(max_length=20)
    file_weight = models.CharField(max_length=10)
    file_amount = models.IntegerField(null=True)
    fix_amount = models.BooleanField(default=False)
    accept_amount = models.BooleanField(default=False)
    file = models.FileField(upload_to='file/', null=True)
    files = models.BooleanField(default=False)
    send_data = models.BooleanField(default=False)
    encrypt = models.BooleanField(default=False)
    secure_key = models.CharField(max_length=20)
    finish = models.BooleanField(default=False)
    download = models.BooleanField(default=False)
    different = models.BooleanField(default=False)


class Request_File(models.Model):
    request = models.ForeignKey(File_Details, on_delete=models.CASCADE)
    email = models.EmailField(max_length=50)
    name = models.CharField(max_length=50, null=True)
    accept = models.BooleanField(default=False)
    generator_key = models.CharField(max_length=20, null=True)
    download = models.BooleanField(default=False)


class Question(models.Model):
    one = models.CharField(max_length=50)
    two = models.CharField(max_length=50)
    three = models.CharField(max_length=50)
    four = models.CharField(max_length=50)
    five = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)


class Client_Request(models.Model):
    name = models.CharField(max_length=20)
    email = models.EmailField(max_length=50)
    company_name = models.CharField(max_length=50)
    company_email = models.EmailField(max_length=50)
    contact = models.BigIntegerField()
    address = models.CharField(max_length=50)
    mac = models.CharField(max_length=50)
    user_email = models.EmailField(max_length=50)
    accept = models.BooleanField(default=False)
    send_link = models.BooleanField(default=False)
    partner = models.ForeignKey(Company_Details, on_delete=models.CASCADE, null=True)
    answer = models.BooleanField(default=False)
