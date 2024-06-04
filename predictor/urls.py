# predictor/urls.py
from django.urls import path
from .views import index, predict

urlpatterns = [
    path('', index, name='index'),
    path('predict/', predict, name='predict'),
]
