from django.urls import path
from . import views

urlpatterns = [
    path('', views.donor_list, name='donor_list'),
    path('create/', views.donor_create, name='donor_create'),
    path('update/<int:pk>/', views.donor_update, name='donor_update'),
    path('delete/<int:pk>/', views.donor_delete, name='donor_delete'),
]