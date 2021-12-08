from django.conf.urls import url
from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views
from Products.views import ProductList

app_name = 'register_login'

urlpatterns = [
    # path('', ProductList.as_view(), name='ProductList'),
    path('register/', register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/Login.html', redirect_field_name='index'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='Products/product_list.html'), name='logout'),

    path('reset_password/',
         auth_views.PasswordResetView.as_view(template_name="registration/reset_password.html"),
         name="reset_password"),

    path('reset_password_sent/',
         auth_views.PasswordResetDoneView.as_view(template_name="registration/password_reset_done.html"),
         name="password_reset_done"),

    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(),name="password_reset_confirm"),

    path('reset_password_completed/', auth_views.PasswordResetCompleteView.as_view(), name="password_reset_completed"),
]