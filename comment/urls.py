from django.urls import path
from author import views

urlpatterns = [
    path("comments/", views.CommentView.as_view()),
    path("user/<int:pk>/", views.CommentDetailView.as_view()),
]
