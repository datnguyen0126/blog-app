from rest_framework import serializers
from blog.models import Comment,Accounts, Post

class CommentSerializer(serializers.ModelSerializer):
    content = serializers.CharField()
    post = serializers.ReadOnlyField(source='post.id')
    author = serializers.ReadOnlyField(source='accounts.id')
    
    class Meta:
        model = Comment
        fields = ['content', 'post', 'author']
    
    def create(self, validated_data):
        return Comment.objects.create(**validated_data)
