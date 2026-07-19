from django.urls import path
from . import views

urlpatterns = [
    path('blogs/', views.BlogListView.as_view(), name='blog-list'),
    path('blogs/<int:pk>/', views.BlogDetailView.as_view(), name='blog-detail'),
    path('feedbacks/', views.FeedbackListView.as_view(), name='feedback-list'),
    path('feedbacks/<int:pk>/', views.FeedbackDetailView.as_view(), name='feedback-detail'),
    path('feedback-stats/', views.FeedbackStatsView.as_view(), name='feedback-stats'),
]
