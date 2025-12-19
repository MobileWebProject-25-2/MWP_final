# blog/models.py

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Post(models.Model):
    """분리수거 검출 결과 게시물"""
    
    CATEGORY_CHOICES = [
        ('plastic', '플라스틱'),
        ('glass', '유리'),
        ('paper', '종이류'),
        ('metal', '고철'),
        ('food', '음식물쓰레기'),
        ('general', '일반쓰레기'),
        ('large', '대형폐기물'),
        ('electronic', '폐가전'),
        ('clothes', '의류'),
        ('other', '기타'),
    ]
    
    author = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    title = models.CharField(max_length=200)
    text = models.TextField()
    category = models.CharField(
        max_length=20, 
        choices=CATEGORY_CHOICES, 
        default='other'
    )
    image = models.ImageField(
        upload_to='recycling_images/%Y/%m/%d/',
        null=True,
        blank=True
    )
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)
    
    class Meta:
        ordering = ['-published_date', '-created_date']
    
    def publish(self):
        self.published_date = timezone.now()
        self.save()
    
    def __str__(self):
        return self.title


class RecyclingGuide(models.Model):
    """분리수거 가이드 정보"""
    
    item_name = models.CharField(max_length=100, unique=True)
    item_name_ko = models.CharField(max_length=100, blank=True)
    category = models.CharField(max_length=50)
    guide = models.TextField()
    tips = models.TextField(blank=True)
    image = models.ImageField(
        upload_to='guide_images/',
        null=True,
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.item_name} - {self.category}"