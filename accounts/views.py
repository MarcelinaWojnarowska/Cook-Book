from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate


def index(request):
    return render(request, 'accounts/index.html')


def signup_user(request):
    form = UserCreationForm()

    if request.method == 'GET':
        return render(request, 'registration/signup.html', {'form': form})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                new_user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                new_user.save()
                login(request, new_user)
                return redirect('cookbook:get_recipes')
            except IntegrityError:
                error = "That username has already been taken. Pleas choose another username."
                return render(request, 'registration/signup.html', {'form': form, 'error': error})
        else:
            error = "Passwords did not match! Try again."
            return render(request, 'registration/signup.html', {'form': form, 'error': error})


def login_user(request):
    form = AuthenticationForm()

    if request.method == 'GET':
        return render(request, 'registration/login.html', {'form': form})
    else:
        user = authenticate(request,username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'registration/login.html',
                          {'form': form, 'error': 'Username or password is incorrect.'})
        else:
            login(request, user)
            return redirect('cookbook:get_recipes')


def logout_user(request):
    if request.method == 'POST':
        logout(request)
        return redirect('accounts:index')
