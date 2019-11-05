from django.contrib import admin
from django.urls import path, re_path, include
from . import views

app_name = "polls"

urlpatterns = [
    path('<int:poll_id>/', views.detail, name='detail'),
    path('<int:poll_id>/results/', views.results, name='results'),
    path('<int:poll_id>/vote/', views.vote, name='vote'),
    path('', views.index, name='index'),
]
