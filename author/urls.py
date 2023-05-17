from django.urls import path
from author import views

urlpatterns = [
    path("users/", views.AuthorView.as_view()),
    path("user/<int:pk>/", views.AuthorDetailView.as_view()),
]
