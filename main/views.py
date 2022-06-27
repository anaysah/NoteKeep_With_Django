from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm



def home(response):
    return render(response,'main/home.html',{})

def login(response):
    data = {"value":"login"}
    return render(response,'main/auth.html',data)

def signup(res):
    if res.method == "POST":
        username = res.POST['email']
        form = UserCreationForm()
        # if form.is_valid():
        #     form.save()
        return redirect("/signup")
    # elif res.method == "GET":
        # form = UserCreationForm()
    
    data = {"value":"signup"}
    return render(res,'main/auth.html',data)

