from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponse
from django.db import IntegrityError 
from .forms import TaskForm
from .models import Task

# Create your views here.
def home(request):
    return render(request,'home.html')


def signup(request):
    if request.method == 'GET':
        print("enviando formulario")
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                #register user
                user = User.objects.create_user(
                    username=request.POST['username'], 
                    password=request.POST["password1"]
                )
                user.save()
                # return HttpResponse("User created succesfully")
                login(request,user)
                return redirect("tasks")
            except IntegrityError:
                return render(request, "signup.html", {
                    "form": UserCreationForm,
                    "error": "Username already exists"
                })
                # return HttpResponse("user already exists")
            
        return render(request, "signup.html", {
                    "form": UserCreationForm,
                    "error": "Password do not match"
                })
        # return HttpResponse("Password do not match")

    return render(request,'signup.html', {
        'form' : UserCreationForm
    })


def tasks(request):
    tasks = Task.objects.filter(user = request.user, datecompleted__isnull=True)
    return render(request, 'tasks.html', {'tasks' : tasks})


def create_task(request):
    if request.method == "GET":
        return render(request, 'create_task.html' ,  {
            'form': TaskForm
        })
    else:
        # print(request.POST)
        try:
            form = TaskForm(request.POST)
            new_task = form.save(commit=False)
            new_task.user = request.user        
            new_task.save()
            return redirect('tasks')
        except ValueError:
            return render(request, "create_task.html", {
            'form': TaskForm,
            'error': 'Please provide valid data',
        })
 

def signout(request):
    logout(request)
    return redirect("home")

def signin(request):
    if request.method == "GET":
        return render(request, "signin.html", {
        "form": AuthenticationForm
    })
    else:
        user = authenticate(request, 
                     username = request.POST["username"], 
                     password = request.POST["password"])
        if user is None:
            return render(request, "signin.html", {
                "form": AuthenticationForm,
                "error": "Username or password is incorrrect"
            })
        else:
            login(request, user)
            return redirect("tasks")
    