from django.urls import path
from . import views

urlpatterns = [
    path('projects/',views.ProjectAPIView.as_view()),
    path('projects/<int:id>/',views.ProjectAPIView.as_view()),
    path('project-section/',views.ProjectSectionAPIView.as_view()),
]