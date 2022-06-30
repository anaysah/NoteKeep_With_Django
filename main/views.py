from django.shortcuts import render,redirect
from django.http import JsonResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as loginAs, logout as logoutAs
from django import forms
from .models import Notes


class NoteForm(forms.Form):
    noteFeild = forms.CharField(max_length = 200,label="Note:",widget=forms.Textarea(attrs={"rows":5, "cols":33,"class":"addNote"}))
    
def home(response):
    NoteFormObj = NoteForm()
    if response.user.is_authenticated:
        if response.method == "POST":
            data = response.POST['noteFeild']
            note = Notes(data=data,user=response.user)
            note.save()
            return redirect("/home")
        elif response.method == "GET" and response.path=="/home":
            allNotes = response.user.notes_set.all()
            return render(response,'main/home.html',{"user":response.user,"NoteFormObj":NoteFormObj,"allNotes":allNotes})
    else:
        return redirect("/auth/login")



def login(res):
    if res.user.is_authenticated:
        return redirect("/home")
    if res.method == "POST":
        username = res.POST['email']
        password = res.POST['password']
        user = authenticate(res,username=username, password=password)
        if user is not None:
            loginAs(res,user)
            return redirect("/home")
    data = {"value":"login"}
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
        return redirect("/auth/signup")
    # elif res.method == "GET":
        # form = UserCreationForm()
    data = {"value":"signup"}
    return render(res,'main/auth.html',data)

def logout(res):
    if res.user.is_authenticated:
        logoutAs(res)
    return redirect("/auth/login")