from django.urls import path, include
from django.contrib import admin 
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("", views.home, name="home"),
    path('admin/', admin.site.urls), # Admin URL

    # Auth
    path("login/", views.custom_login_view, name="login"),
    path("logout/", auth_views.LogoutView.as_view(next_page='home'), name="logout"),
    path("signup/", views.signup, name="signup"),

    # App pages
    path("chart/", views.chart, name="chart"),
    path("portfolio/", views.portfolio, name="portfolio"),
    path("prediction/", views.prediction, name="prediction"),
    path("announcement/", views.announcement, name="announcement"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("payment/", views.payment, name="payment"),
]
