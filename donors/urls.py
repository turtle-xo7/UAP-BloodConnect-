from django.urls import path
from . import views


urlpatterns = [
   path('dashboard/', views.donor_dashboard, name='donor_dashboard'),
   path('register/', views.donor_register, name='donor_register'),
   path('directory/', views.donor_directory, name='donor_directory'),
   path('add-donation/', views.add_donation_history, name='add_donation'),
   path('history/', views.donation_history, name='donation_history'),
]
