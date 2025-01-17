from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.contrib.auth import login
from .forms import SignupForm
from chat.models import Message
from django.db.models import Q
from django.contrib.auth.decorators import login_required

from django.urls import reverse

# Create your views here.
@login_required
def chat_page(request, *args, **kwargs):
    user_object = get_user_model().objects.get(username=request.user.username)
    users = get_user_model().objects.exclude(username=request.user.username)
    messages = Message.objects.filter(
        Q(sender=user_object) | Q(receiver=user_object)
    ).order_by('timestamp')
    group = {}
    for message in messages:
        if message.chat_id not in group:
            group[message.chat_id] = []
        group[message.chat_id].append(message)
    context = {
        'users_list': users,
        'user_object': user_object,
        'groups': group,
    }
    return render(request, 'chat/chat.html', context)

def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect(reverse('chat:chat_page'))
        return render(request, 'chat/signup.html', {'errors': form.errors, 'form': form})
    else:
        form = SignupForm()
    
    return render(request, 'chat/signup.html', {'form': form})

def home(request):
    return render(request, 'chat/home.html')