from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.db.models import Q
from django.contrib.auth.models import User
from .models import Message


class Main(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect("home")
        return render(request, 'chat/main.html')


class Login(View):
    def get(self, request):
        return render(request, 'chat/login.html')

    def post(self, request):
        data = request.POST.dict()
        username = data.get('username')
        password = data.get('password')

        user = authenticate(request=request, username=username, password=password)
        if user != None:
            login(request=request, user=user)
            return redirect("home")

        return render(request, 'chat/login.html', context={"error": "something went wrong"})


class Register(View):
    def get(self, request):
        return render(request, 'chat/register.html')

    def post(self, request):
        context = {}

        data = request.POST.dict()
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')

        try:
            new_user = User()
            new_user.first_name = first_name
            new_user.last_name = last_name
            new_user.username = username
            new_user.email = email
            new_user.set_password(password)
            new_user.save()

            user = authenticate(request=request, username=username, password=password)
            if user != None:
                login(request=request, user=user)
                return redirect("home")
        except:
            context.update({"error": "The username or password is incorrect"})

        return render(request, 'chat/register.html', context=context)


class Logout(View):
    def get(self, request):
        logout(request)
        return redirect("main")


class Home(View):
    def get(self, request):
        if request.user.is_authenticated:
            return render(request, 'chat/home.html', context={"user": request.user, "users": User.objects.all()})
        return redirect("main")


@method_decorator(login_required, name="dispatch")
class ChatPerson(View):
    def get(self, request, id):
        person = User.objects.get(id=id)
        me = request.user
        messages = Message.objects.filter(
            Q(from_who=me, to_who=person)
            |
            Q(from_who=person, to_who=me)
        ).order_by("date", "time")
        context = {
            "person": person,
            "messages": messages,
            "me":me
        }

        return render(request,'chat/chat_person.html', context=context)
