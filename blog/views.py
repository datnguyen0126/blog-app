from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib import auth
from blog.models import Accounts, CustomUserManager, Post
from django.core.files.storage import FileSystemStorage

# Create your views here.
@login_required(login_url='/login/')
def home(request): 
    posts = None
    if request.method == "POST":
        posts = Post.objects.filter(title__contains=request.POST.get("search"))
    else:
        posts = Post.objects.all()
    context = {
        'posts': posts
    }
    return render(request, 'blog/home.html', context)

@login_required(login_url='/login/')
def about(request):
    
    return render(request, 'blog/about.html')

@login_required(login_url='/login/')
def blog_create(request, id=None):
    if request.method == "POST":
        post = Post()
        post.title = request.POST.get('title') 
        post.description = request.POST.get('description')
        post.image = request.FILES.get('image')
        post.save()       
        return redirect('blog-home')        
    else:
        if id:
            context = {
                'post': Post.objects.get(id = id)
            }
            return render(request, 'blog/blog_create.html', context)            
        else:
            return render(request, 'blog/blog_create.html')
    

def register(request):    
    if request.method == "POST":
        if request.POST.get('username') and request.POST.get('password1') and request.POST.get('password2'):            
            Accounts.objects.create_user(request.POST.get('username'), request.POST.get('password1'))
            messages.success(request, "New User added!")
        return redirect('blog-home')
    else:
        return render(request, 'blog/register.html')

def login(request):
    if request.user.is_authenticated:
        return redirect('blog-home')
 
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = auth.authenticate(username=username, password=password)
 
        if user is not None:
            auth.login(request, user)
            next_url = request.GET.get('next')
            if next_url:
                return HttpResponseRedirect(next_url)
            else:
                return redirect('blog-home')
 
        else:
            messages.error(request, 'Error wrong username/password')
 
    return render(request, 'blog/login.html')
 
 
def logout(request):
    auth.logout(request)
    return render(request,'blog/logout.html')

def blog_delete(request, id):
    post = Post.objects.filter(id=id)
    post.delete()
    return redirect('blog-home')