from django.urls import path
from . import views

urlpatterns = [
    path('', views.book_list, name='book_list'),
    path('add/', views.book_add, name='book_add'),
    path('edit/<int:id>/', views.book_edit, name='book_edit'),
    path('delete/<int:id>/', views.book_delete, name='book_delete'),
    path('search/', views.book_search, name='book_search'),
    path('statistics/', views.book_statistics, name='book_statistics'),
]
