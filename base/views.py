from django.shortcuts import render, redirect
from base.models import Room
from base.forms import RoomForm

rooms = [{"id": 1, "name": 'python1 '},
         {"id": 2, "name": 'python2 '},
         {"id": 3, "name": 'python3 '},
         {"id": 4, "name": 'python4 '}, ]


# Create your views here.
def home(request):
    rooms = Room.objects.all()
    context = {'rooms': rooms}
    return render(request=request, template_name="base/home.html", context=context)


def room(request, id):
    single_room = Room.objects.get(id=id)
    context = {"room": single_room}
    return render(request, 'base/room.html', context)


def create_room(request):
    room_form = RoomForm()
    if request.method == 'POST':
        new_room = RoomForm(request.POST)
        if new_room.is_valid():
            new_room.save()
            return redirect('home')
    context = {"room": room_form}
    return render(request, 'base/create_room.html', context)


def update_room(request, id):
    room = Room.objects.get(id=id)
    room_form = RoomForm(instance=room)
    context = {"room": room_form}

    if request.method == 'POST':
        new_room = RoomForm(request.POST, instance=room)
        if new_room.is_valid():
            new_room.save()
            return redirect('home')
    return render(request, 'base/create_room.html', context)


def delete_room(request, id):
    room = Room.objects.get(id=id)
    if request.method == 'POST':
        room.delete()
        return redirect('home')
    return render(request, 'base/delete_room.html')
