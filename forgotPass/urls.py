from django.urls import path
from forgotPass import views

urlpatterns = [
    path('', views.index, name="index"),
]