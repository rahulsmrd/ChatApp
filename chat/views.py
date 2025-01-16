from django.shortcuts import render
from django.contrib.auth import get_user_model
from chat.models import Message

# Create your views here.
def chat_page(request, *args, **kwargs):
    user_object = get_user_model().objects.get(username=kwargs['username'])
    users = get_user_model().objects.exclude(username=request.user.username)
    chat_id = f"{max(request.user.id, user_object.id)}-{min(user_object.id, request.user.id)}"
    messages = Message.objects.filter(chat_id=chat_id).order_by('timestamp')
    context = {
        'users': users,
        'user_object': user_object,
        'messages': messages,
    }
    return render(request, 'chat/chat.html', context)