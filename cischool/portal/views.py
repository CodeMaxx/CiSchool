from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from portal.models import Instructor, Policy
from django.contrib.auth import logout, login
from django.views.decorators.csrf import csrf_exempt
import json
import sys
import requests

# Create your views here.

def land(request):
	user = request.user
	if user.is_authenticated:
		instructor = Instructor.objects.get(user=user)
		if instructor is not None:
			# current lecture, upcoming lecture, name of policies,
			return redirect(reverse('portal:dashboard'))
	return render(request, 'portal/landing.html')

@csrf_exempt
def register(request):
	if request.method == 'GET':
		return render(request, 'portal/register.html')
	elif request.method == 'POST':
		# first_name = request.POST['first_name']
		# last_name = request.POST['last_name']
		username = request.POST['username']
		password = request.POST['password']
		user = User.objects.create_user(username=username, password=password)#, first_name=first_name, last_name=last_name)
		user.save()
		Instructor(user=user).save()
		authenticate(request, username=username, password=password)
		return redirect(reverse('portal:dashboard'))

@csrf_exempt
def login_view(request):
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(request, username=username, password=password)
		if user is not None:
			login(request, user)
			return redirect(reverse('portal:dashboard'))
		else:
			return HttpResponse(status=401)
	elif request.method == 'GET':
		return render(request, 'portal/login.html')


@login_required
def logout_view(request):
	logout(request)
	return redirect('portal:landing')

@login_required
def dashboard(request):
	context = {'hello': 'world'}
	return render(request, 'portal/dashboard.html', context)

@login_required
def courses(request):
	user = request.user
	instructor = Instructor.objects.get(user=user)
	courses = Policy.objects.filter(instructor=instructor)
	return render(request, 'portal/courses.html', context={'courses': courses})


@login_required
def edit_course(request, pk):
	pass

@login_required
def policy_toolbox(request):
	context = {'hello': 'world'}
	return render(request, 'portal/ptoolbox.html', context)

@login_required
def policy_edit(request):
	context = {'hello': 'world'}
	return render(request, 'portal/policyedit.html', context)

@login_required
def filter_edit(request):
	context = {'hello': 'world'}
	return render(request, 'portal/filteredit.html', context)

@login_required
def policies(request):
	user = request.user
	instructor = Instructor.objects.get(user=user)
	policies = Policy.objects.filter(instructor=instructor)
	return render(request, 'portal/policies.html', context={'policies': policies})

@login_required
def edit_policies(request, pk):
	if request.method == 'GET':
		policy = Policy.objects.get(pk=pk)
		context = {'policy': policy}
		return render(request, 'portal/edit_policy.html', context=context)
	elif request.method == 'POST':
		raise NotImplementedError

def fetch_policy(request):
	server = "https://fmcrestapisandbox.cisco.com"
	username = "nihal.111"
	password = "Tx6RWzAQ"

	r = None
	headers = {'Content-Type': 'application/json'}
	api_auth_path = "/api/fmc_platform/v1/auth/generatetoken"
	auth_url = server + api_auth_path
	try:
	    # 2 ways of making a REST call are provided:
	    # One with "SSL verification turned off" and the other with "SSL verification turned on".
	    # The one with "SSL verification turned off" is commented out. If you like to use that then
	    # uncomment the line where verify=False and comment the line with =verify='/path/to/ssl_certificate'
	    # REST call with SSL verification turned off:
	    r = requests.post(auth_url, headers=headers, auth=requests.auth.HTTPBasicAuth(
	        username, password), verify=False)
	    # REST call with SSL verification turned on: Download SSL certificates from your FMC first and provide its path for verification.
	    # r = requests.post(auth_url, headers=headers, auth=requests.auth.HTTPBasicAuth(
	    # username, password), verify='/path/to/ssl_certificate')
	    print(r)
	    auth_headers = r.headers
	    auth_token = auth_headers.get('X-auth-access-token', default=None)
	    if auth_token == None:
	        print("auth_token not found. Exiting...")
	        sys.exit()
	except Exception as err:
	    print ("Error in generating auth token --> " + str(err))
	    sys.exit()

	headers['X-auth-access-token'] = auth_token

	idx = "005056BB-0B24-0ed3-0000-858993527846"
	api_path = "/api/fmc_config/v1/domain/e276abec-e0f2-11e3-8169-6d9ed49b625f/policy/accesspolicies/{}".format(idx)    # param
	url = server + api_path
	if (url[-1] == '/'):
	    url = url[:-1]

	try:
	    # REST call with SSL verification turned off:
	    # r = requests.get(url, headers=headers, verify=False)
	    # REST call with SSL verification turned on:
	    # r = requests.get(url, headers=headers, verify='/path/to/ssl_certificate')
	    r = requests.get(url, headers=headers, verify=False)
	    status_code = r.status_code
	    resp = r.text
	    if (status_code == 200):
	        # print("GET successful. Response data --> ")
	        json_resp = json.loads(resp)
	        return HttpResponse(json.dumps(json_resp, sort_keys=True,
	                         indent=4, separators=(',', ': ')))
	    else:
	        r.raise_for_status()
	        print("Error occurred in GET --> " + resp)
	except requests.exceptions.HTTPError as err:
	    print ("Error in connection --> " + str(err))
	finally:
	    if r:
	        r.close()
