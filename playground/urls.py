from django.urls import path
from . import views

# URLConf
urlpatterns = [
    path('profile/', views.profile),
    path('', views.index, name='index') # homepage
]