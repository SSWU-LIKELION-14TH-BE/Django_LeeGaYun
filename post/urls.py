from django.urls import path
from .views import post_create_view, post_detail_view, post_like_view, comment_like_view, post_list_view, post_edit_view, post_delete_view

urlpatterns = [
    path('', post_list_view, name='post_list'),
    path('create/', post_create_view, name='post_create'),
    path('<int:pk>/', post_detail_view, name='post_detail'),
    path('<int:pk>/edit/', post_edit_view, name='post_edit'),
    path('<int:pk>/delete/', post_delete_view, name='post_delete'),
    path('<int:pk>/like/', post_like_view, name='post_like'),
    path('comment/<int:comment_id>/like/', comment_like_view, name='comment_like'),
]