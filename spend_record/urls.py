"""track_spending URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from . import views
appname = 'spend_record'
urlpatterns = [
    path('records/', views.record_list, name='record_list'),
    path('add/', views.add_record, name='add_record'),
    path('analysis/', views.analysis, name='analysis'),
]
urlpatterns += [
    path('categories/', views.category_list, name='category_list'),
    # path('categories/add/', views.category_add, name='category_add'),
    path('categories/delete/<int:pk>/', views.delete_category, name='delete_category'),
]

urlpatterns += [
    path('records/edit/<int:pk>/', views.edit_record, name='edit_record'),
    path('records/delete/<int:pk>/', views.delete_record, name='delete_record'),
]