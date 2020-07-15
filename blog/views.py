from django.shortcuts import render, redirect
from django.http import HttpRequest
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib import auth

# Create your views here.
@login_required
def home(request):
    return render(request, 'blog/home.html')

def register(request):
    if request.method == "POST":
        print(request.POST);
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/register')
    else:
        form = UserCreationForm()
    return render(request, 'blog/register.html', {'form': form})

def login(request):
    if request.user.is_authenticated:
        return redirect('blog-home')
 
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = auth.authenticate(username=username, password=password)
 
        if user is not None:
            auth.login(request, user)
            return redirect('blog-home')
 
        else:
            messages.error(request, 'Error wrong username/password')
 
    return render(request, 'blog/login.html')
 
 
def logout(request):
    auth.logout(request)
    return render(request,'blog/logout.html')

