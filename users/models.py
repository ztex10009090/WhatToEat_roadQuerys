# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models


# Create your models here.
class UserAccount(models.Model):
    UserID = models.CharField(primary_key=True, max_length=50)
    UserName = models.CharField(max_length=50)
    UserPicture = models.CharField(max_length=100, blank=True)
    EMail = models.CharField(max_length=100, blank=True)
    Password = models.CharField(max_length=100)
    VerificationCode = models.CharField(max_length=10, blank=True)
    Weight = models.IntegerField(default=0)
    SignInOrigin = models.CharField(max_length=20, default='testPost')
    CreateDate = models.DateTimeField()
    ModifyDate = models.DateTimeField()

    def __str__(self):
        return self.UserName
