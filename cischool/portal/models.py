from django.db import models

# Create your models here.

class Venue(models.Model):
	name = models.CharField(max_length=50)
	router_ip = models.GenericIPAddressField()


class Slot(models.Model):
	start = models.IntegerField() # 0 - 23 0 means from 00:00 to 00:59
	day = models.IntegerField() # 0-6 0 is Sunday


class Instructor(models.Model):
	username = models.CharField(max_length=50, primary_key=True)
	name = models.CharField(max_length=50)


class Student(models.Model):
	username = models.CharField(max_length=50, primary_key=True)
	name = models.CharField(max_length=50)


class Lecture(models.Model):
	venue = models.ForeignKey(Venue, on_delete=models.CASCADE)
	slot = models.ForeignKey(Slot, on_delete=models.CASCADE)


class Url(models.Model):
	url = models.URLField()
	id = models.IntegerField(primary_key=True)
	name = models.CharField(max_length=50)
	desc = models.CharField(max_length=150)


class Rule(models.Model):
	ip = models.CharField(max_length=15)
	url = models.ForeignKey(Url, on_delete=models.CASCADE)
	ports = models.CharField(max_length=50)
	action = models.CharField(max_length=15)


class Policy(models.Model):
	rules = models.ManyToManyField(Rule)
	instructor = models.ForeignKey(Instructor)
	white = models.BooleanField()


class Course(models.Model):
	lecture = models.ForeignKey(Lecture, on_delete=models.CASCADE)
	instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE)
	students = models.ManyToManyField(Student)
	policy = models.ForeignKey(Policy, on_delete=models.DO_NOTHING)
