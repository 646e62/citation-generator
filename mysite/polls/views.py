from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def index(request):
    return HttpResponse("<h1>Hello, world.</h1> You're at the polls index.\nIt's everything you'd hope for in a poll index.")
