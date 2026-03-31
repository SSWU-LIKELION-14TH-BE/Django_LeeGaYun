from django.urls import path
from .views import signup_view, login_view, home_view, logout_view, find_password_view, reset_password_view

urlpatterns = [
    path('signup/', signup_view, name='signup'),
    path('login/', login_view, name='login'),
    path('', home_view, name='home'), 
    path('logout/', logout_view, name='logout'),
    path('find-password/', find_password_view, name='find_password'),
    path('reset-password/', reset_password_view, name='reset_password'),
]