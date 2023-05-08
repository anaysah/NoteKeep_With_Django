from django.shortcuts import render,redirect
from django.http import JsonResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as loginAs, logout as logoutAs
from django import forms
from .models import Notes


# class NotesForm(forms.Form):
#     titleFeild = forms.CharField(max_length = 50,label='',widget=forms.TextInput(attrs={"class":"noteFields","placeholder":"Title"}))
#     noteFeild = forms.CharField(max_length = 200,widget=forms.Textarea(attrs={"rows":5, "cols":33,"class":"noteFields"}),label='')
# class NotesForm(forms.ModelForm):
#     class Meta:
#         model = Notes
#         fields = ['title', 'data']
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields['title'].widget.attrs.update({'placeholder': 'Title','class':'noteFields'})
#         self.fields['data'].widget.attrs.update({'placeholder': 'Your Note', "rows":5,"class":"noteFields"})
    
# def home(response):
#     NoteFormObj = NotesForm()
#     if not response.user.is_authenticated:
#         return redirect("login")
#     if not response.method == "POST" and (response.path=="/home" or response.path=="/"):
#         allNotes = response.user.notes_set.all()
#         return render(response,'main/home.html',{"user":response.user,"NoteFormObj":NoteFormObj,"allNotes":allNotes,"value":"Home"})
    
#     data = response.POST['noteFeild']
#     title = response.POST['titleFeild']
#     note = Notes(title=title,data=data,user=response.user)
#     note.save()
#     return redirect("home")
    # elif response.method == "GET" :

class NotesForm(forms.ModelForm):
    class Meta:
        model = Notes
        fields = ['title', 'data']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Title', 'class': 'noteFields'}),
            'data': forms.Textarea(attrs={'placeholder': 'Your Note', 'rows': 5, 'class': 'noteFields'})
        }

def home(request):
    if not request.user.is_authenticated:
        return redirect('login')
    NoteFormObj = NotesForm(request.POST or None)
    if request.method == 'POST' and NoteFormObj.is_valid():
        note = NoteFormObj.save(commit=False)
        note.user = request.user
        note.save()
        return redirect('home')
    allNotes = request.user.notes_set.all()
    return render(request, 'main/home.html', {'user': request.user, 'NoteFormObj': NoteFormObj, 'allNotes': allNotes, 'value': 'Home'})

        
    
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