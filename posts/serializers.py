from rest_framework import serializers
from .models import Post

class PostSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField(source='user.username')
    user_id = serializers.ReadOnlyField(source='user.id')
    
    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'username', 'user_id', 'created_at', 'updated_at']
        read_only_fields = ['id', 'username', 'user_id', 'created_at', 'updated_at']