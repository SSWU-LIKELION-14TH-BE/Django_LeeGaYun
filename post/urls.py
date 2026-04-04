from django.urls import path
from .views import post_create_view, post_detail_view

urlpatterns = [
    path('create/', post_create_view, name='post_create'),
    path('<int:pk>/', post_detail_view, name='post_detail'),
]