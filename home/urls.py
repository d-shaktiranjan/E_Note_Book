from django.urls import path, include
from home import views

urlpatterns = [
    path('',views.index, name = "index"),
    path('read/<slug:slug>',views.read, name = "read"),
    path('delete/<slug:slug>',views.delete, name = "delete"),
    path('edit/<slug:slug>',views.edit, name = "edit"),
]