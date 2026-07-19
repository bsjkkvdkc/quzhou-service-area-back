from django.contrib import admin
from .models import Blog, Feedback


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'created_at']
    list_filter = ['category', 'created_at']
    search_fields = ['title', 'content']


class FeedbackInline(admin.TabularInline):
    model = Feedback
    extra = 0
    readonly_fields = ['name', 'category', 'subject', 'content', 'rating', 'created_at']


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ['subject', 'category', 'priority', 'rating', 'is_read', 'is_resolved', 'created_at']
    list_filter = ['category', 'priority', 'is_read', 'is_resolved', 'created_at']
    search_fields = ['subject', 'content', 'name']
    readonly_fields = ['name', 'contact', 'category', 'priority', 'subject', 'content', 'rating', 'created_at', 'updated_at']
    actions = ['mark_as_read', 'mark_as_resolved']

    def mark_as_read(self, request, queryset):
        queryset.update(is_read=True)
    mark_as_read.short_description = "标记为已读"

    def mark_as_resolved(self, request, queryset):
        queryset.update(is_resolved=True)
    mark_as_resolved.short_description = "标记为已解决"
