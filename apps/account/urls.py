from django.urls import path
from .views import LoginView, RegisterView, user_logout, UserProfileView, UserProfileUpdateView


urlpatterns = [
    path("user-login", LoginView.as_view(), name="user_login"),
    path("user-register", RegisterView.as_view(), name="user_register"),
    path("user-logout", user_logout, name="user_logout"),
    path("user-profile/<int:pk>/", UserProfileView.as_view(), name="user_profile"),
    path("update-profile/<int:pk>/", UserProfileUpdateView.as_view(), name="update_profile")
]
