from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib import auth
from blog.models import Accounts, CustomUserManager, Post, Comment

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework import status
from blog.serializers import PostSerializer, CommentSerializer

# Create your views here.
@login_required(login_url='/login/')
def home(request): 
    posts = None
    if request.method == "POST":
        posts = Post.objects.filter(title__contains=request.POST.get("search"))
    else:
        posts = Post.objects.all()
    for post in posts:
        author = Accounts.objects.get_user(pk=post.author_id)
        if post.author_id == request.user.id:
            post.allow_to_delete = True
        post.author_name = author.username
    context = {
        'posts': posts
    }
    return render(request, 'blog/home.html', context)

@login_required(login_url='/login/')
def blog_detail(request, id):
    context = {
        'post': Post.objects.get(id=id)
    }
    return render(request, 'blog/detail.html', context)

@login_required(login_url='/login/')
def about(request):
    
    return render(request, 'blog/about.html')

@login_required(login_url='/login/')
def blog_create(request, id=None):
    if request.method == "POST":
        if id:
            post = Post.objects.get(id=id)
        else:
            post = Post()
        post.title = request.POST.get('title') 
        post.description = request.POST.get('description')
        post.image = request.FILES.get('image')
        post.author_id = request.user.id
        if post.image:
            post.save()
        else:
            post.save(update_fields=['title', 'description', 'author_id'])       
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



# Create your views here.
class JSONResponse(HttpResponse):
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)
        
@csrf_exempt
def comment_collection(request, id):
    if request.method == 'GET':
        comments = Comment.objects.filter(post__id=id)
        comment_serializer = CommentSerializer(comments, many=True)
        post = Post.objects.get(id=id)
        post_serializer = PostSerializer(post)
        return JSONResponse(post_serializer.data)
    elif request.method == 'POST':
        comment_data = JSONParser().parse(request)
        author = Accounts.objects.get(id=comment_data.get('author_id'))
        post = Post.objects.get(pk=id)
        try:
            comment_data = Comment.objects.create(content=comment_data.get('content'), author=author, post=post)
        except Exception:            
            return JSONResponse({"can not save comment!" }, status=status.HTTP_400_BAD_REQUEST)
        else:
            return JSONResponse({ "message": "Done"}, status=status.HTTP_201_CREATED)
    
# @csrf_exempt
# def game_detail(request, id):
#     try:
#         game = Game.objects.get(id=id)
#     except Game.DoesNotExist:
#         return HttpResponse(status=status.HTTP_404_NOT_FOUND)
#     if request.method == 'GET':
#         game_serializer = GameSerializer(game)
#         return JSONResponse(game_serializer.data)
#     elif request.method == 'PUT':
#         game_data = JSONParser().parse(request)
#         game_serializer = GameSerializer(game, data=game_data)
#         if game_serializer.is_valid():
#             game_serializer.save()
#             return JSONResponse({ "msg": "Update success"}, status=status.HTTP_204_NO_CONTENT)
#         return JSONResponse(game_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#     elif request.method == 'DELETE':
#         game.delete()
#         return HttpResponse(status=status.HTTP_204_NO_CONTENT)