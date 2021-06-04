from django.urls import path
from forgotPass import views

urlpatterns = [
    path('', views.index, name="index"),
    path('otpcheck/', views.otpcheck, name="otpcheckForgot"),
    path('resetPass/', views.resetPass, name="resetPass"),
]
