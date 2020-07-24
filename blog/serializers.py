from rest_framework import serializers
from blog.models import Comment, Accounts, Post
  
class AccountSerializer(serializers.ModelSerializer):

    class Meta:
        model = Accounts
        fields = ['username']

class CommentSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()

    class Meta:      
        model = Comment
        fields = ['author', 'content'] 

class PostSerializer(serializers.ModelSerializer):
    #comments = serializers.StringRelatedField(many=True, read_only=True)
    comments = CommentSerializer(many=True)
    
    class Meta:
        model = Post
        fields = ['title', 'comments']  
