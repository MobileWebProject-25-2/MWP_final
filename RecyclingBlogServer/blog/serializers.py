# blog/serializers.py

from rest_framework import serializers
from .models import Post, RecyclingGuide
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class PostSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    image_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Post
        fields = [
            'id', 'author', 'title', 'text', 'category',
            'image', 'image_url', 'created_date', 'published_date'
        ]
    
    def get_image_url(self, obj):
        if obj.image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.image.url)
            return obj.image.url
        return None


class PostCreateSerializer(serializers.ModelSerializer):
    """게시물 생성용 Serializer"""
    
    class Meta:
        model = Post
        fields = ['title', 'text', 'category', 'image', 'created_date', 'published_date']


class RecyclingGuideSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecyclingGuide
        fields = '__all__'


class PostListSerializer(serializers.ModelSerializer):
    """목록 조회용 간략한 Serializer"""
    
    image_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Post
        fields = ['id', 'title', 'category', 'image_url', 'published_date']
    
    def get_image_url(self, obj):
        if obj.image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.image.url)
            return obj.image.url
        return None