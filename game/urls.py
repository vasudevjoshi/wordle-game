from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('', views.home, name='home'),
    path('start/', views.start_game, name='start_game'),
    path('play/<int:game_id>/', views.play_game, name='play_game'),
    path('admin/daily-report/', views.admin_daily_report, name='admin_daily_report'),
    path('admin/user-report/', views.admin_user_report, name='admin_user_report'),
]
