from django.urls import path, include
from . import views
from .views import home

urlpatterns = [
    path("", views.home, name="home"),
    path("accounts/",include("django.contrib.auth.urls")),  # For login/logout
    path("login/", views.user_login, name="login"),
    path("signup/", views.signup, name="signup"),
    path("chart/", views.chart, name="chart"),
    path("portfolio/", views.portfolio, name="portfolio"),
    path("prediction/", views.prediction, name="prediction"),
    path("announcement/", views.announcement, name="announcement"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("payment/", views.payment, name="payment"),

]
