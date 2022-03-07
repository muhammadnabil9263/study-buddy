from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from base.models import Room, Topic
from base.forms import RoomForm
from django.db.models import Q
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


#
# rooms = [{"id": 1, "name": 'python1 '},
#          {"id": 2, "name": 'python2 '},
#          {"id": 3, "name": 'python3 '},
#          {"id": 4, "name": 'python4 '}, ]


def login_user(request):
    page = 'login'
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        print(user)
        print("----------------------------------------------------------------------------------")
        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            messages.error(request, 'username or password not correct')
            return redirect('login')
    context = {"page": page}
    return render(request, "base/login_register.html", context)


def logout_user(request):
    logout(request)
    return redirect("home")


def register_user(request):
    register_form = UserCreationForm()
    context = {"register_form": register_form}

    if request.method == 'POST':
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        if password1 == password2:
            User.objects.create_user(username=username, password=password1)
            user = authenticate(username=username, password=password1)
            login(request, user)
            return redirect("home")
    return render(request, "base/login_register.html", context)


def home(request):
    q = request.GET.get('q') if request.GET.get('q') is not None else ""
    rooms = Room.objects.filter(Q(topic__name__contains=q) |
                                Q(description__contains=q) |
                                Q(name__contains=q)
                                )
    count = rooms.count()
    topics = Topic.objects.all()
    context = {'rooms': rooms, 'topics': topics, "count": count}
    return render(request=request, template_name="base/home.html", context=context)


def room(request, id):
    single_room = Room.objects.get(id=id)
    context = {"room": single_room}
    return render(request, 'base/room.html', context)


@login_required(login_url='login')
def create_room(request):
    room_form = RoomForm()
    if request.method == 'POST':
        new_room = RoomForm(request.POST)
        if new_room.is_valid():
            new_room.save()
            return redirect('home')
    context = {"room": room_form}
    return render(request, 'base/create_room.html', context)


@login_required(login_url='login')
def update_room(request, id):
    room = Room.objects.get(id=id)
    room_form = RoomForm(instance=room)
    context = {"room": room_form}
    if request.user != room.host:
        return HttpResponse("You are not allowed")
    if request.method == 'POST':
        new_room = RoomForm(request.POST, instance=room)
        if new_room.is_valid():
            new_room.save()
            return redirect('home')
    return render(request, 'base/create_room.html', context)


@login_required(login_url='login')
def delete_room(request, id):
    room = Room.objects.get(id=id)

    if request.user != room.host:
        return HttpResponse("You are not allowed")

    if request.method == 'POST':
        room.delete()
        return redirect('home')
    return render(request, 'base/delete_room.html')
