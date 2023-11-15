# accounts/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('',views.CustomLoginView.as_view(), name='login')
    # You can add more URL patterns as needed for other user types
]
