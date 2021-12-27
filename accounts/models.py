from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class ExtendedUsers(models.Model):
    p_pic = models.ImageField(upload_to='static', blank=True)
    p_desc = models.CharField(max_length=1000, blank=True)
    own_comp = models.BooleanField(default=False, blank=True)
    # emp_comp = models.BooleanField(default=False, blank=True)
    comp_name = models.CharField(max_length=100, blank=True)
    # comp_position = models.CharField(max_length=100, blank=True)
    # Fr_list = models.FileField(upload_to='static', blank=True)
    # Client_list = models.FileField(upload_to='static', blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)


class Company(models.Model):
    # comp_id same as id primary key
    comp_name = models.CharField(max_length=100, blank=False)
    # comp_img = models.ImageField(upload_to='static', blank=True)
    # emp_id same as user id
    # emp_id = models.IntegerField(blank=False)
    emp_id = models.ForeignKey(User, on_delete=models.CASCADE)
    emp_position = models.CharField(max_length=100, blank=False)
    verify = models.BooleanField(default=False, blank=False)


class Chat(models.Model):
    comp = models.BooleanField(default=False)
    comp_obj = models.ForeignKey(Company, on_delete=models.CASCADE, blank=True, null=True)
    F_usr = models.BigIntegerField(blank=False, null=False)
    F_usr_name = models.CharField(default='', max_length=100)
    T_usr = models.BigIntegerField(blank=True, null=True)
    T_usr_name = models.CharField(default='', max_length=100)
    date = models.DateTimeField(default=timezone.now, blank=True)
    data = models.CharField(max_length=1000, blank=True)
    file = models.FileField(upload_to=settings.MEDIA_DIR, blank=True, null=True)  # can be image,video anything

