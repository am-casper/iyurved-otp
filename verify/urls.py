
from django.urls import path
from . import views



urlpatterns = [
    path('initiate-auth/', views.initiate_auth, name='initiate_auth'),
    path('verify-otp/', views.verify_otp, name='verify_otp'),
]