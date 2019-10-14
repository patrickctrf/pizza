from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.utils import timezone

from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout

def telahome(request):
    return render(request, 'pizza/telaHome.html')

