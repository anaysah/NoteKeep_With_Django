from django.shortcuts import render,redirect
from django.http import JsonResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as loginAs, logout as logoutAs
from django import forms
from .models import Notes


class NoteForm(forms.Form):
    titleFeild = forms.CharField(max_length = 30,label='',widget=forms.TextInput(attrs={"class":"noteFields","placeholder":"Title"}))
    noteFeild = forms.CharField(max_length = 200,widget=forms.Textarea(attrs={"rows":5, "cols":33,"class":"noteFields"}),label='')
    
def home(response):
    NoteFormObj = NoteForm()
    if not response.user.is_authenticated:
        return redirect("login")
    if not response.method == "POST" and (response.path=="/home" or response.path=="/"):
        allNotes = response.user.notes_set.all()
        return render(response,'main/home.html',{"user":response.user,"NoteFormObj":NoteFormObj,"allNotes":allNotes,"value":"Home"})
    
    data = response.POST['noteFeild']
    title = response.POST['titleFeild']
    note = Notes(title=title,data=data,user=response.user)
    note.save()
    return redirect("home")
    # elif response.method == "GET" :
        
    
def deleteNote(res):
    noteToDelete = Notes.objects.filter(id=res.POST['noteid'])
    noteToDelete[0].delete()
    return JsonResponse({})

def login(res):
    message = None
    data = {"value":"Login"}
    if res.user.is_authenticated:
        return redirect("/home")
    if res.method == "POST":
        email = res.POST['email']
        password = res.POST['password']
        if User.objects.filter(username=email).exists():
            user = authenticate(res,username=email, password=password)
            if user is not None:
                loginAs(res,user)
                return redirect("/home")
            else:
                data['message'] = "wrong password"
        else:
            data['message'] = "user not exits";
    return render(res,'main/auth.html',data)

def signup(res):
    data = {"value":"Signup"}
    data['message'] = None
    if res.method == "POST":
        name = res.POST['name'].split()
        first_name = name[0]
        last_name = ' '.join(name[1:])
        email = res.POST['email']
        password = res.POST['password']
        if not User.objects.filter(username=email).exists():
            user = User.objects.create_user(username=email,first_name=first_name, last_name=last_name, email=email, password=password)
            if isinstance(user, User):
                data['message'] = "User Created"
            else:
                data['message'] = "Not Created"
        else:
            data['message'] = "user already exists"
    
    return render(res,'main/auth.html',data)

def logout(res):
    if res.user.is_authenticated:
        logoutAs(res)
    return redirect("/auth/login")