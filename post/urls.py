from django.urls import path
from .views import post_create_view, post_detail_view, post_like_view, comment_like_view

urlpatterns = [
    path('create/', post_create_view, name='post_create'),
    path('<int:pk>/', post_detail_view, name='post_detail'),
    path('<int:pk>/like/', post_like_view, name='post_like'),
    path('comment/<int:comment_id>/like/', comment_like_view, name='comment_like'),
]