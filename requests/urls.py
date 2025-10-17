from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_request, name='create_request'),
    path('', views.request_list, name='request_list'),
    path('<int:request_id>/', views.request_detail, name='request_detail'),
    path('my-requests/', views.my_requests, name='my_requests'),
    path('<int:request_id>/respond/', views.respond_to_request, name='respond_to_request'),
]