from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.template import RequestContext, loader
from django.http import Http404
from django.contrib import auth
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
import json

def login(request):
    if request.user.username:
	return HttpResponseRedirect('/')
    else:
	if request.method == 'POST':
	    username=request.POST.get('username','')
	    password=request.POST.get('password','')
            url_to_go = request.POST.get('place_to_go','')
            user=auth.authenticate(username=username,password=password)
	    if user is not None:
		auth.login(request,user)
                if url_to_go == '':
                    return HttpResponse('/buzz/hackin/getstarted')
                else:
                    return HttpResponseRedirect(url_to_go)
	    else:
		return HttpResponseRedirect('/buzz/hackin/invalid/')
        else:
	    c={}
	    
            url_to_go = request.GET.get('next')
            if url_to_go != None:
                c['place_to_go'] = url_to_go
            else:
                c['place_to_go'] = ''
	    return render_to_response('authentication/login.html',c)

def invalid(request):
    if request.user.username:
	return HttpResponseRedirect('/')
    else:
	c={}
	c.update(csrf(request))
	return render_to_response('authentication/invalid.html',c)

def register(request):
    if request.user.username:
	return HttpResponseRedirect('/')
    else:
	if request.method =='POST':
	    form = UserCreationForm(request.POST)
	    if form.is_valid():
		user = form.save()
		return HttpResponseRedirect('/buzz/hackin/getstarted')
	else:
	    form = UserCreationForm()
	return render_to_response('authentication/register.html', {
		    'form': form,
		},context_instance=RequestContext(request))

@login_required
def logout(request):
    auth.logout(request)
    return redirect('authentication.views.login')
