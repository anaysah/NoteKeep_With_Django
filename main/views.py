from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as loginAs, logout as logoutAs



def home(response):
    if response.user.is_authenticated:
        return render(response,'main/home.html',{})
    else:
        return redirect("http://127.0.0.1:8000/auth/login")

def login(res):
    user="nothing"
    if res.method == "POST":
        username = res.POST['email']
        password = res.POST['password']
        user = authenticate(res,username=username, password=password)
        if user is not None:
            loginAs(res,user)
            return render(res,'main/home.html',{})
    data = {"value":"login","authen":user}
    return render(res,'main/auth.html',data)

def signup(res):
    if res.method == "POST":
        username = res.POST['name']
        email = res.POST['email']
        password = res.POST['password']
        form = User.objects.create_user(username,email,password)
        # print(form.is_valid())    
        # if form.is_valid():
        #     form.save()
        return redirect("http://127.0.0.1:8000/auth/signup")
    # elif res.method == "GET":
        # form = UserCreationForm()
    data = {"value":"signup"}
    return render(res,'main/auth.html',data)

def logout(res):
    if res.user.is_authenticated:
        logoutAs(res)
    return redirect("http://127.0.0.1:8000/auth/login")