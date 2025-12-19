# blog/views.py

from rest_framework import viewsets, permissions, status, generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import render, get_object_or_404
from django.utils import timezone

from .models import Post, RecyclingGuide
from .serializers import (
    PostSerializer, 
    PostCreateSerializer,
    PostListSerializer,
    RecyclingGuideSerializer
)


class PostViewSet(viewsets.ModelViewSet):
    """게시물 CRUD API"""
    
    queryset = Post.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def get_serializer_class(self):
        if self.action == 'create':
            return PostCreateSerializer
        elif self.action == 'list':
            return PostListSerializer
        return PostSerializer
    
    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user if self.request.user.is_authenticated else None,
            published_date=timezone.now()
        )


class RecyclingGuideViewSet(viewsets.ReadOnlyModelViewSet):
    """분리수거 가이드 조회 API"""
    
    queryset = RecyclingGuide.objects.all()
    serializer_class = RecyclingGuideSerializer
    permission_classes = [permissions.AllowAny]


class PostListAPIView(generics.ListAPIView):
    """이미지 목록 조회 API (2-4 요구사항)"""
    
    queryset = Post.objects.filter(published_date__isnull=False)
    serializer_class = PostListSerializer
    permission_classes = [permissions.AllowAny]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # 카테고리 필터링
        category = self.request.query_params.get('category')
        if category:
            queryset = queryset.filter(category=category)
        
        # 날짜 필터링
        date_from = self.request.query_params.get('date_from')
        date_to = self.request.query_params.get('date_to')
        if date_from:
            queryset = queryset.filter(published_date__gte=date_from)
        if date_to:
            queryset = queryset.filter(published_date__lte=date_to)
        
        return queryset


class ImageDetailAPIView(generics.RetrieveAPIView):
    """이미지 상세 조회 API"""
    
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.AllowAny]


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def recycling_guide_by_item(request, item_name):
    """아이템 이름으로 분리수거 가이드 조회"""
    
    guide = get_object_or_404(RecyclingGuide, item_name__iexact=item_name)
    serializer = RecyclingGuideSerializer(guide)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def category_list(request):
    """카테고리 목록 조회"""
    
    categories = [
        {'code': code, 'name': name} 
        for code, name in Post.CATEGORY_CHOICES
    ]
    return Response(categories)


# 웹 페이지 뷰
def post_list(request):
    """게시물 목록 웹 페이지"""
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    return render(request, 'blog/post_list.html', {'posts': posts})


def post_detail(request, pk):
    """게시물 상세 웹 페이지"""
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})