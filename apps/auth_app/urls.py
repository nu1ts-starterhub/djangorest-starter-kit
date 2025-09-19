from django.urls import path
from .views import RegisterView, LoginView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='auth_app-register'),
    path('login/', LoginView.as_view(), name='auth-login'),
]
