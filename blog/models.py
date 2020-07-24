from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth import get_user_model

# Create your models here.
    
class CustomUserManager(BaseUserManager):
    """custom user manager class"""
    
    use_in_migration = True

    def _create_user(self, username, password, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not username:
            raise ValueError('The given username must be set')
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def get_user(self, pk):
        user = get_user_model().objects.get(pk=pk)
        return user
    
    def create_user(self, username, password=None, **extra_fields):
        return self._create_user(username, password, **extra_fields)

    def create_superuser(self, username, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self._create_user(username, password, **extra_fields)

class Accounts(AbstractBaseUser):
    username = models.CharField(unique=True, max_length=100)
    USERNAME_FIELD = 'username'
    objects = CustomUserManager()
    
class Post(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(Accounts, on_delete=models.CASCADE, default=1)
    image = models.ImageField(upload_to='images/',null=True)

class Comment(models.Model):
    content = models.TextField()
    author = models.ForeignKey(Accounts, on_delete=models.CASCADE, null=True, related_name='accounts')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True, related_name='comments')
    date_created = models.DateTimeField(auto_now_add=True)
    
    def __repr__(self):
        return { self.author: self.content }
    
    def __str__(self):
        return '%s:%s' % (self.author,self.content)
        
