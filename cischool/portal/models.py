from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class Venue(models.Model):
	name = models.CharField(max_length=50)
	router_ip = models.GenericIPAddressField()


class Slot(models.Model):
	start = models.IntegerField() # 0 - 23 0 means from 00:00 to 00:59
	day = models.IntegerField() # 0-6 0 is Monday


class Instructor(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)


class Student(models.Model):
	username = models.CharField(max_length=50, primary_key=True)
	name = models.CharField(max_length=50)


class Lecture(models.Model):
	venue = models.ForeignKey(Venue, on_delete=models.CASCADE)
	slot = models.ForeignKey(Slot, on_delete=models.CASCADE)


class Url(models.Model):
	url = models.URLField()
	small_id = models.AutoField(primary_key=True)
	identity = models.CharField(max_length=100)
	name = models.CharField(max_length=50)
	desc = models.CharField(max_length=150)


class UrlCategories(models.Model):
	name = models.CharField(max_length=30)
	small_id = models.AutoField(primary_key=True)
	identity = models.CharField(max_length=100)
	reputation = models.CharField(max_length=200)
	link = models.URLField()


class Rule(models.Model):
	name = models.CharField(max_length=50)
	enabled = models.BooleanField(default=True)
	urls = models.ManyToManyField(Url)
	url_categories = models.ManyToManyField(UrlCategories)
	action = models.CharField(max_length=15)


class Policy(models.Model):
	name = models.CharField(max_length=50)
	desc = models.CharField(max_length=150)
	small_id = models.AutoField(primary_key=True)
	identity = models.CharField(max_length=100)
	rules = models.ManyToManyField(Rule)
	action = models.CharField(max_length=15)


class Course(models.Model):
	name = models.CharField(max_length=50)
	code = models.CharField(max_length=10)
	lecture = models.ForeignKey(Lecture, on_delete=models.CASCADE)
	instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE)
	students = models.ManyToManyField(Student)
	policy = models.ForeignKey(Policy, on_delete=models.DO_NOTHING)
