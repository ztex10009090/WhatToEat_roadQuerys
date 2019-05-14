# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from users.models import *
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

class Classify(models.Model):
    ClassifyID = models.AutoField(primary_key=True)
    ClassifyName = models.CharField(max_length=50)
    TagColor = models.CharField(max_length=20)

    def __str__(self):
        return self.ClassifyName


class RoadQuery(models.Model):
    RoadQueryID = models.AutoField(primary_key=True)
    RoadQueryName = models.CharField(max_length=50)
    RoadQueryAddress = models.CharField(max_length=50)
    RoadQueryPicture = models.CharField(max_length=100, blank=True)
    Classify = models.ManyToManyField(Classify)
    Introduction = models.TextField()
    Star = models.IntegerField(default=0)
    OpenTime = models.CharField(max_length=50)
    Latitude = models.CharField(max_length=30)
    Longitude = models.CharField(max_length=30)
    CreateUser = models.ForeignKey(UserAccount, on_delete=models.PROTECT, related_name='RoadQuery_CreateUser')
    CreateDate = models.DateTimeField()
    ModifyDate = models.DateTimeField()

    def __str__(self):
        return self.RoadQueryName


class Comment(models.Model):
    CommentID = models.AutoField(primary_key=True)
    RoadQuery = models.ForeignKey(RoadQuery, on_delete=models.PROTECT, related_name='Comment_RoadQuery')
    User = models.ForeignKey(UserAccount, on_delete=models.PROTECT, related_name='Comment_User')
    StarAmount = models.IntegerField(default=1, validators=[MaxValueValidator(5), MinValueValidator(-5)])
    CommentContent = models.CharField(max_length=200)
    CreateDate = models.DateField()

    def __str__(self):
        return self.RoadQuery.RoadQueryName + ':' + str(self.StarAmount)
