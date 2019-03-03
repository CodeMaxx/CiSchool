from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from portal.models import Instructor, Policy
from django.contrib.auth import logout

# Create your views here.

def land(request):
	pass


def register(request):
	first_name = request.POST['first_name']
	last_name = request.POST['last_name']
	username = request.POST['username']
	password = request.POST['password']
	user = User.objects.create_user(username=username, password=password, first_name=first_name, last_name=last_name)
	user.save()
	Instructor(user=user).save()


def login(request):
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(username=username, password=password)
		if user is not None:
			return redirect('landing')
		else:
			return HttpResponse(status=401)
	elif request.method == 'GET':
		return render(request, 'login.html')


@login_required
def logout(request):
	logout(request)
	pass


@login_required
def courses(request):
	user = request.user
	instructor = Instructor.objects.get(user=user)
	courses = Policy.objects.filter(instructor=instructor)
	return render(request, 'courses.html', context={'courses': courses})


@login_required
def edit_course(request):
	pass


@login_required
def policies(request):
	user = request.user
	instructor = Instructor.objects.get(user=user)
	policies = Policy.objects.filter(instructor=instructor)
	return render(request, 'policies.html', context={'policies': policies})

@login_required
def edit_policies(request):
	pass
