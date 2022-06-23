from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.ItemView.as_view()),
    path('order/', views.ItemOrderView.as_view()),
]