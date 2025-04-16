
from django.shortcuts import render
from django.shortcuts import render, redirect

def login_view(request):
    return render(request, 'login.html')

def pdg_dashboard(request):
    return render(request, 'pdg/dashboard.html') 