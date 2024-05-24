from django.urls import path
from . import views


urlpatterns = [
    path('/register/', views.register, name='register'),
    path('/login/', views.login, name='login'),
    path('/logout/', views.logout, name='logout'),
    path('forgotPassword/', views.forgotPassword, name='forgotPassword'),
    path('/dashboard/', views.dashboard, name='dashboard'),
    path('/dashboard/<order_number>',views.order_detail,name='order_detail'),
    path('activate/<uidb64>/<token>', views.activate, name='activate'),
    path('reset_password_validate/<uidb64>/<token>', views.reset_password_validate, name='reset_password_validate'),
    path('reset_password/', views.reset_password, name='reset_password')
]
