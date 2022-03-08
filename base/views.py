from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from base.models import Room, Topic, Message
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
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            login(request, new_user)
            return redirect('home')
        else:
            messages.error(request, "password didn't match ")
            return redirect("register")
    # if request.method == 'POST':
    # username = request.POST.get('username')
    # password1 = request.POST.get('password1')
    # password2 = request.POST.get('password2')
    # if password1 == password2:
    #     User.objects.create_user(username=username, password=password1)
    #     user = authenticate(username=username, password=password1)
    #     login(request, user)
    #     return redirect("home")
    # else:
    #     messages.error(request,"password didn't match ")
    #     return redirect("register")
    return render(request, "base/login_register.html", context)


def home(request):
    q = request.GET.get('q') if request.GET.get('q') is not None else ""
    rooms = Room.objects.filter(Q(topic__name__contains=q) |
                                Q(description__contains=q) |
                                Q(name__contains=q)
                                )
    count = rooms.count()
    topics = Topic.objects.all()
    room_messages = Message.objects.all()
    context = {'rooms': rooms, 'topics': topics, "count": count, "room_messages": room_messages}
    return render(request=request,
                  template_name="base/home.html",
                  context=context)


def room(request, id):
    single_room = Room.objects.get(id=id)
    room_messages = single_room.message_set.all()
    participants = single_room.participants.all()
    if request.method == 'POST':
        Message.objects.create(
            user=request.user,
            room=single_room,
            body=request.POST.get("body")
        )
        single_room.participants.add(request.user)
        return redirect('room', id)
    context = {"room": single_room, "room_messages": room_messages, "participants": participants}
    return render(request, 'base/room.html', context)


def user_profile(request, id):
    user = User.objects.get(id=id)
    topics = Topic.objects.all()
    rooms = user.room_set.all()
    room_messages = Message.objects.all()
    context = {"user": user, "topics": topics, "rooms": rooms, 'room_messages': room_messages}
    return render(request, "base/user-profile.html", context)


@login_required(login_url='login')
def create_room(request):
    room_form = RoomForm()
    if request.method == 'POST':
        new_room = RoomForm(request.POST)
        if new_room.is_valid():
            new_room = new_room.save(commit=False)
            new_room.host = request.user
            if new_room.host != None:
                new_room.save()
            else:
                messages(request, "user is none")

            return redirect('home')
    context = {"room": room_form}
    return render(request,
                  'base/create_room.html',
                  context)


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
        return redirect(request.META.get('HTTP_REFERER'))
    return render(request, 'base/delete.html', {"obj": room})


@login_required(login_url='login')
def delete_message(request, id):
    message = Message.objects.get(id=id)
    if request.method == 'POST':
        message.delete()
        return redirect(request.META.get('HTTP_REFERER'))
    return render(request, 'base/delete.html', {"obj": message})
