from django.urls import path
from . import views
urlpatterns = [
   path("hero/",views.HeroContentAPIView.as_view(), name="hero-content"),
    path("about/", views.AboutContentAPIView.as_view(), name="about-content"),
    path("stats/", views.StatListCreateAPIView.as_view(), name="stats-list"),
    path("stats/<int:pk>/", views.StatRetrieveUpdateDestroyAPIView.as_view(), name="stats-detail"),
    path("messages/", views.MessagesAPIView.as_view()),
    path("messages/<int:id>/", views.MessagesAPIView.as_view()),
    path("logout/", views.LogoutAPIView.as_view(), name="logout"),
]


