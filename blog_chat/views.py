from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils.safestring import mark_safe
from django.http import HttpRequest, HttpResponse
from django.views.generic import DetailView, ListView
import json

from . import models
from blog.models import CustomUser
# Create your views here.

class ChatListView(ListView):
    model = models.Chat
    context_object_name = 'chat_list'
    template_name = 'chat/index.html'


@login_required
def room(request:HttpRequest, room_name):
    if str(room_name).isdigit():
        return render(
                request,
                'chat/room.html',
                {
                    'room_name': room_name,
                    'username': mark_safe(json.dumps(request.user.username)),
                },
            )
    
    try:
        user = CustomUser.objects.get(username=room_name)
        selfuser = CustomUser.objects.get(username=request.user.username)
        chat_instance = models.Chat.objects.get(user1=selfuser, user2=user)
        return redirect(
            'room',
            room_name=chat_instance.id,
            permanent=True
        )
    except:
        try:
            user = CustomUser.objects.get(username=room_name)
            selfuser = CustomUser.objects.get(username=request.user.username)
            chat_instance = models.Chat.objects.get(user1=user, user2=selfuser)
            return redirect(
                'room',
                room_name=chat_instance.id,
                permanent=True
            )
        except:
            user = CustomUser.objects.get(username=room_name)
            selfuser = CustomUser.objects.get(username=request.user.username)
            chat_instance = models.Chat.objects.create(
                user1=selfuser,
                user2=user
            )
            return redirect(
                'room',
                room_name=chat_instance.id,
                permanent=True,
            )