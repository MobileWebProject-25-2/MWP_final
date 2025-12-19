from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from blog.views import PostViewSet, RecyclingGuideViewSet

# REST API 라우터
router = DefaultRouter()
router.register(r'Post', PostViewSet, basename='post')
router.register(r'Guide', RecyclingGuideViewSet, basename='guide')

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # 블로그 앱
    path('', include('blog.urls')),
    
    # REST API
    path('api_root/', include(router.urls)),
    
    # JWT 인증 (Simple JWT)
    path('api-token-auth/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api-token-refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # DRF 로그인/로그아웃 (브라우저용)
    path('api-auth/', include('rest_framework.urls')),
]

# 개발 환경에서 미디어 파일 서빙
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)