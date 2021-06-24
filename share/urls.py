from django.urls import path
from share import views

urlpatterns = [
    path('makePublic', views.makePublic, name="makePublic"),
    path('makePrivate', views.makePrivate, name="makePrivate"),
    path('<slug:slug>/', views.share, name="share"),
]
