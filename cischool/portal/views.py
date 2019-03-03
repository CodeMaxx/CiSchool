from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from portal.models import Instructor, Policy
from django.contrib.auth import logout

# Create your views here.

def land(request):
	user = request.user
	if user.is_authenticated:
		instructor = Instructor.objects.get(user=user)
		if instructor is not None:
			# current lecture, upcoming lecture, name of policies,
			return render(request, 'dashboard.html', context={})
	return render(request, 'landing.html')


def register(request):
	if request.method == 'GET':
		return render(request, 'register.html')
	elif request.method == 'POST':
		first_name = request.POST['first_name']
		last_name = request.POST['last_name']
		username = request.POST['username']
		password = request.POST['password']
		user = User.objects.create_user(username=username, password=password, first_name=first_name, last_name=last_name)
		user.save()
		Instructor(user=user).save()
		authenticate(request, username=username, password=password)
		return redirect('landing')


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


@login_required
def courses(request):
	user = request.user
	instructor = Instructor.objects.get(user=user)
	courses = Policy.objects.filter(instructor=instructor)
	return render(request, 'courses.html', context={'courses': courses})


@login_required
def edit_course(request, pk):
	pass


@login_required
def policies(request):
	user = request.user
	instructor = Instructor.objects.get(user=user)
	policies = Policy.objects.filter(instructor=instructor)
	return render(request, 'policies.html', context={'policies': policies})

@login_required
def edit_policies(request, pk):
	if request.method == 'GET':
		policy = Policy.objects.get(pk=pk)
		context = {'policy': policy}
		return render(request, 'edit_policy.html', context=context)
	elif request.method == 'POST':
		raise NotImplementedError
