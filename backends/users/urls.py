from django.urls import path
from .views import RegisterView, RetrieveUserView,UserLoginView,UpdateProfileView


urlpatterns = [
  path('register', RegisterView.as_view()),
  path('login', UserLoginView.as_view()),
  path('me', RetrieveUserView.as_view()),
  path('update_profile/<int:pk>/', UpdateProfileView.as_view())
]