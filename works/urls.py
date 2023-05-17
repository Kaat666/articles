from django.urls import path
from author import views

urlpatterns = [
    path("works/", views.WorksView.as_view()),
    path("Works/<int:pk>/", views.WorksDetailView.as_view()),
]
