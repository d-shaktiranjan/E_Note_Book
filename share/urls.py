from django.urls import path
from share import views

urlpatterns = [
    path('makePublic', views.makePublic, name="makePublic"),
]
