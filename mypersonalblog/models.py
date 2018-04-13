# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models


class ArtInfo(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    art_id = models.CharField(max_length=10)
    art_aut = models.CharField(max_length=15)
    article = models.TextField()
    art_tit = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = 'art_info'


class Article(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    userid = models.CharField(max_length=5)
    art_id = models.CharField(max_length=10)
    art_tit = models.CharField(max_length=30)
    art_itr = models.CharField(max_length=150)
    type_no = models.IntegerField()
    art_type = models.CharField(max_length=10)

    class Meta:
        managed = False
        db_table = 'article'
        unique_together = (('id', 'art_id'),)


class Comment(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    art_id = models.CharField(max_length=10)
    user_name = models.CharField(max_length=10)
    comment = models.TextField()
    user_id = models.CharField(max_length=5)

    class Meta:
        managed = False
        db_table = 'comment'
        unique_together = (('id', 'art_id'),)


class SysUser(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    userid = models.CharField(max_length=5)
    username = models.CharField(max_length=15)
    password = models.CharField(max_length=200)
    isadmin = models.IntegerField(default=0)

    class Meta:
        managed = False
        db_table = 'sys_user'
        unique_together = (('id', 'userid'),)


class UserInfo(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    username = models.CharField(max_length=10)
    userid = models.CharField(max_length=5)
    user_tel = models.CharField(max_length=15, blank=True, null=True)
    user_eml = models.CharField(max_length=25, blank=True, null=True)
    user_img = models.CharField(max_length=100, blank=True, null=True)
    user_gender = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user_info'
        unique_together = (('id', 'username'),)