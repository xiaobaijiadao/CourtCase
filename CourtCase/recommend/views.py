from django.shortcuts import render
from django.http import HttpResponseRedirect

def index(request):
	return render(request, 'recommend/index.html')

def list(request):
	blogs = {}
	return render(request, 'recommend/list.html')

def display(request):
	return render(request, 'recommend/display.html')