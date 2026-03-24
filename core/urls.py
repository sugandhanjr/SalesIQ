from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing_page, name='landing'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('home/', views.home_view, name='home'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('forecast/generate/', views.trigger_forecast_view, name='trigger_forecast'),
    path('products/', views.product_list, name='product_list'),
    path('sales/', views.sales_list, name='sales_list'),
    path('forecast/', views.forecast_view, name='forecast'),
    path('insights/', views.insights_view, name='insights'),
]
