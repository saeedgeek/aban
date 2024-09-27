from django.urls import path
from . import views

urlpatterns = [
    path('tracks/', views.tracks_list, name='tracks_list'),
    # Add more paths as needed for your app
]
