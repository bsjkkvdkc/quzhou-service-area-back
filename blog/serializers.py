from rest_framework import serializers
from .models import Blog, Feedback


class BlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = ['id', 'title', 'summary', 'content', 'category', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class FeedbackSerializer(serializers.ModelSerializer):
    category_display = serializers.CharField(source='get_category_display', read_only=True)
    rating_stars = serializers.CharField(source='rating_stars', read_only=True)

    class Meta:
        model = Feedback
        fields = ['id', 'name', 'contact', 'category', 'category_display', 'priority',
                  'priority_display', 'subject', 'content', 'rating', 'rating_stars',
                  'is_read', 'is_resolved', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
