from rest_framework import generics
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from django.db.models import Avg
from .models import Blog, Feedback
from .serializers import BlogSerializer, FeedbackSerializer


class BlogListView(generics.ListCreateAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer


class BlogDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer


class FeedbackListView(generics.ListCreateAPIView):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer


class FeedbackDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer


class FeedbackStatsView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        total = Feedback.objects.count()
        unread = Feedback.objects.filter(is_read=False).count()
        resolved = Feedback.objects.filter(is_resolved=True).count()
        by_category = {}
        for cat_id, cat_label in Feedback.CATEGORY_CHOICES:
            by_category[cat_label] = Feedback.objects.filter(category=cat_id).count()
        by_priority = {}
        for pri_id, pri_label in Feedback.PRIORITY_CHOICES:
            by_priority[pri_label] = Feedback.objects.filter(priority=pri_id).count()
        avg_rating = Feedback.objects.aggregate(models_avg=Avg('rating'))
        return Response({
            'total': total,
            'unread': unread,
            'resolved': resolved,
            'pending': total - resolved,
            'by_category': by_category,
            'by_priority': by_priority,
            'avg_rating': round(avg_rating['models_avg'] or 0, 1),
        })
