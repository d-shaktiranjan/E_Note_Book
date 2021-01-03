from django.urls import path, include
from home import views

urlpatterns = [
    path('',views.index, name = "index"),
    path('read/<slug:slug>',views.read, name = "read"),
]