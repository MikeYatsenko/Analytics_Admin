from django.urls import path
from .views import (RegisterView, VerifyEmail, LoginAPIView, LogOutAPIView)
from rest_framework_simplejwt.views import TokenRefreshView
urlpatterns = [
    path('register/', RegisterView.as_view(), name="register"),
    path('email-verify/',VerifyEmail.as_view(), name ="email-verify"),
    path('login/', LoginAPIView.as_view(), name = 'login'),
    path('logout/', LogOutAPIView.as_view(), name='logout')

]