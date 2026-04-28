from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Trip


# LOGIN + REGISTER (SAME PAGE)
def user_login(request):
    if request.method == "POST":

        # REGISTER
        if request.POST.get('email'):
            username = request.POST.get('username')
            email = request.POST.get('email')
            password = request.POST.get('password')
            confirm = request.POST.get('confirm')

            if password == confirm:
                if User.objects.filter(username=username).exists():
                    return render(request, 'mainapp/login.html', {'error': 'Username already exists'})

                User.objects.create_user(username=username, email=email, password=password)
                return render(request, 'mainapp/login.html', {'success': 'Account created! Please login'})
            else:
                return render(request, 'mainapp/login.html', {'error': 'Passwords do not match'})

        # LOGIN
        else:
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('/home/')
            else:
                return render(request, 'mainapp/login.html', {'error': 'Invalid username or password'})

    return render(request, 'mainapp/login.html')


# LOGOUT
def user_logout(request):
    logout(request)
    return redirect('/login/')


# HOME
@login_required(login_url='/login/')
def home(request):
    if request.method == "POST":
        title = request.POST.get('title')
        desc = request.POST.get('desc')
        image = request.FILES.get('image')
        date = request.POST.get('date')

        Trip.objects.create(
            user=request.user,   # 🔥 FIXED
            title=title,
            desc=desc,
            image=image,
            date=date
        )

    trips = Trip.objects.filter(user=request.user)   # 🔥 USER-WISE DATA
    return render(request, 'mainapp/home.html', {'trips': trips})


# DELETE
@login_required(login_url='/login/')
def delete_trip(request, id):
    trip = get_object_or_404(Trip, id=id, user=request.user)
    trip.delete()
    return redirect('/home/')


# EDIT
@login_required(login_url='/login/')
def edit_trip(request, id):
    trip = get_object_or_404(Trip, id=id, user=request.user)

    if request.method == "POST":
        trip.title = request.POST.get('title')
        trip.desc = request.POST.get('desc')

        if request.FILES.get('image'):
            trip.image = request.FILES.get('image')

        trip.save()
        return redirect('/home/')

    return render(request, 'mainapp/edit.html', {'trip': trip})