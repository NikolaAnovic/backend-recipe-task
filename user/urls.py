from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from user.views import UserRegisterView, UserInfo

urlpatterns = [
    path('register/', UserRegisterView.as_view(), name="register"),
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('info/<pk>/', UserInfo.as_view(), name="info"),
]