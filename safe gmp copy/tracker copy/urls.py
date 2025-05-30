from django.urls import path
from . import views
from .views import check_in
from .views import SignUpView
urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('start-session/', views.start_session, name='start_session'),
    path('end-session/', views.end_session, name='end_session'),
    path('check-in/', views.check_in, name='check_in'),
    path('', views.home, name='home'),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('mark-detox-day/', views.mark_detox_day, name='mark_detox_day'),
]