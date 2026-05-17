from django.urls import path
from . import views

urlpatterns = [
    path("", views.login_view),
    path("login/", views.login_view),
    path("logout/", views.logout_view),
    path("dashboard/", views.dashboard),
    path("create/", views.create_goal),
    path("toggle/<int:id>/", views.toggle_step),
]