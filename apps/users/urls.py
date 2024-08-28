from django.urls import path
from .views.user_views import UserListGenericView, RegisterUserGenericView, UserDetailGenericView

urlpatterns = [
    path('', UserListGenericView.as_view(), name='user-list'),
    path('register/', RegisterUserGenericView.as_view(), name='user-register'),
    path('users/<int:pk>/', UserDetailGenericView.as_view(), name='user-detail'),
]