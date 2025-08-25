from django.urls import path
from .views import (Main, Login, Home, Register, Logout, ChatPerson)


urlpatterns = [
    path('', Main.as_view(), name='main'),
    path('login', Login.as_view(), name='login'),
    path('register', Register.as_view(), name='register'),
    path('logout', Logout.as_view(), name='logout'),
    path('home', Home.as_view(), name='home'),
    path('chat_person/<int:id>', ChatPerson.as_view(), name='chat_person'),
]