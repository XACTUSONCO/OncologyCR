from django.contrib.auth.models import User
from django.db import models


class Organization(models.Model):
    name = models.CharField(max_length=100)
    logo = models.ImageField(upload_to='organization/logo/', null=True, blank=True)
    is_deleted = models.BooleanField(default=False)


class Company(models.Model):
    type = models.CharField(max_length=50, null=True, blank=True)
    foreign_type = models.CharField(max_length=50, null=True, blank=True)
    name_kor = models.CharField(max_length=100, null=True, blank=True)
    name_eng = models.CharField(max_length=100, null=True, blank=True)
    is_deleted = models.BooleanField(default=False)


class Notice(models.Model):
    title = models.CharField(max_length=100)
    contents = models.TextField()
    target = models.CharField(max_length=200)
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    create_date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    is_deleted = models.BooleanField(default=False)


class Commute(models.Model):
    date = models.DateField(null=False)
    start_work = models.DateTimeField(null=True, blank=True)
    end_work = models.DateTimeField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    is_deleted = models.BooleanField(default=False)
