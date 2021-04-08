from django.shortcuts import render
from django.contrib.auth.models import User

def index(request):
    return render(request, 'chat/index.html', {})

def room(request, room_name):
    user = User(username=request.user.username)
    return render(request, 'chat/room.html', {
        'room_name': room_name,
        'curr_user': user
    })