from django.urls import path
from . import views

# URLConf
urlpatterns = [
    path('product/', views.ShowProduct)
]
