from django.urls import path, include
from home import views

urlpatterns = [
    path('', views.index, name="index"),
    path('read/<slug:slug>', views.read, name="read"),
    path('delete/<slug:slug>', views.delete, name="delete"),
    path('edit/<slug:slug>', views.edit, name="edit"),
    path('team', views.team, name="team"),
    path('signup', views.signup, name="signup"),
    path('login', views.login, name="login"),
    path('logout', views.logout, name="logout"),
    path('otpCheck', views.otpCheck, name="otpCheck"),
]
