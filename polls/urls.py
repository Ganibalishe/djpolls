from django.contrib import admin
from django.urls import path, re_path, include
from . import views

app_name = "polls"

urlpatterns = [
    path('<int:poll_id>/', views.detail, name='detail'),
    path('<int:poll_id>/results/', views.results, name='results'),
    path('<int:question_id>/vote/', views.vote, name='vote'),
    path('passed/', views.passed, name='passed'),
    path('', views.index, name='index'),
]
