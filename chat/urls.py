from django.urls import path
from chat.views import chat_page
from django.contrib.auth.views import LoginView, LogoutView

app_name = 'chat'

urlpatterns = [
    path('chat/<str:username>/', chat_page, name='chat_page'),
    path('login/', LoginView.as_view(template_name='chat/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout')
]