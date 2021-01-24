# accounts/views.py
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import HttpResponse

def signup_view(request):
    status = 200
    form = UserCreationForm
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, 'Account was created for ' + user)
            return redirect('login')
        else:
            messages.info(request,"Please try again")
            status = 409
    else:
        form = UserCreationForm()
    context = {}
    return render(request,'../templates/registration/signup.html', status = status)


def login_view(request):
    status = 200
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, "Username or password is incorrect!  Please try again!")
            status = 401
    return render(request, '../templates/registration/login.html', status = status)

def logout_view(request):
    logout(request)
    return redirect('login')
