from django.shortcuts import render

# Create your views here.

def land(request):
	context = {'hello': 'world'}
	return render(request, 'portal/landing.html', context)


def login(request):
	context = {'hello': 'world'}
	return render(request, 'portal/login.html', context)

def logout(request):
	pass


def register(request):
	context = {'hello': 'world'}
	return render(request, 'portal/register.html', context)


def courses(request):
	pass


def edit_course(request):
	pass


def policies(request):
	pass


def edit_policies(request):
	pass
