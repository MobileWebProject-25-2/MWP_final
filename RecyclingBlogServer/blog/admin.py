# blog/admin.py

from django.contrib import admin
from .models import Post, RecyclingGuide

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'author', 'published_date', 'created_date']
    list_filter = ['category', 'published_date', 'created_date']
    search_fields = ['title', 'text']
    date_hierarchy = 'published_date'

@admin.register(RecyclingGuide)
class RecyclingGuideAdmin(admin.ModelAdmin):
    list_display = ['item_name', 'item_name_ko', 'category', 'updated_at']
    list_filter = ['category']
    search_fields = ['item_name', 'item_name_ko', 'guide']