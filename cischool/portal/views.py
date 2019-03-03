from django.shortcuts import render

# Create your views here.

def land(request):
	context = {'hello': 'world'}
	return render(request, 'portal/landing.html', context)


def login(request):
	pass


def logout(request):
	pass


def register(reqeust):
	pass


def courses(request):
	pass


def edit_course(request):
	pass


def policies(request):
	pass


def edit_policies(request):
	pass
