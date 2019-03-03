from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class Venue(models.Model):
	name = models.CharField(max_length=50)
	router_ip = models.GenericIPAddressField()


class Slot(models.Model):
	start = models.IntegerField() # 0 - 23 0 means from 00:00 to 00:59
	day = models.IntegerField() # 0-6 0 is Sunday


class Instructor(models.Model):
	user = models.ForeignKey(User)
	name = models.CharField(max_length=50)


class Student(models.Model):
	username = models.CharField(max_length=50, primary_key=True)
	name = models.CharField(max_length=50)


class Lecture(models.Model):
	venue = models.ForeignKey(Venue, on_delete=models.CASCADE)
	slot = models.ForeignKey(Slot, on_delete=models.CASCADE)


class Url(models.Model):
	url = models.URLField()
	identity = models.CharField(max_length=100, primary_key=True)
	name = models.CharField(max_length=50)
	desc = models.CharField(max_length=150)


class UrlCategories(models.Model):
	name = models.CharField(max_length=30)
	identity = models.CharField(max_length=100, primary_key=True)
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
	identity = models.CharField(max_length=100, primary_key=True)
	rules = models.ManyToManyField(Rule)
	action = models.CharField(max_length=15)
	instructor = models.ForeignKey(Instructor)

class Course(models.Model):
	lecture = models.ForeignKey(Lecture, on_delete=models.CASCADE)
	instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE)
	students = models.ManyToManyField(Student)
	policy = models.ForeignKey(Policy, on_delete=models.DO_NOTHING)
