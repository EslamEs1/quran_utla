from django.contrib import admin
from .models import Post
from django_summernote.admin import SummernoteModelAdmin


class SomeModelAdmin(SummernoteModelAdmin):
    summernote_fields = "__all__"


@admin.register(Post)
class PostAdmin(SomeModelAdmin, admin.ModelAdmin):
    list_display = ("title", "slug", "created_at", "updated_at")
    search_fields = ("title", "content")
    prepopulated_fields = {"slug": ("title",)}
    readonly_fields = ("created_at", "updated_at")
