from django import views
from django.contrib import admin
from django.urls import path,include
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('login/',views.loginPage,name = 'login'),
    path('register/',views.registerPage,name = 'register'),
    path('logout/',views.logoutUser,name = 'logout'),
    path('user/',views.userPage,name = 'user'),
    path('account/',views.account_setting,name = 'account'),


    path('',views.home,name='home'),
    path('products/',views.products,name='products'),
    path('customer/<str:pk_test>/',views.customer,name='customer'),

    path('create_order/',views.CreateOrder,name='create_order'),
    path('update_order/<str:pk>/',views.UpdateOrder,name='update_order'),
    path('delete_order/<str:pk>/',views.DeleteOrder,name='delete_order'),

    path('password_reset/',auth_views.PasswordResetView.as_view(template_name = 'accounts/reset_password_form.html'),
    name='password_reset'),

    path('password_reset_done/',auth_views.PasswordResetDoneView.as_view(template_name = 'accounts/reset_password_done.html'),
    name='password_reset_done'),

    path('password_reset_confirm/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name = 'accounts/reset_password_confirm.html'),
    name='password_reset_confirm'),

    path('password_reset_complete/',auth_views.PasswordResetCompleteView.as_view(template_name = 'accounts/reset_password_confirm_done.html'),
    name='password_reset_complete')


]