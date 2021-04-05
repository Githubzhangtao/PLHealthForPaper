from django.urls import path, include
from . import views

urlpatterns = [
    path('getUser/', views.TestView.as_view())
]
