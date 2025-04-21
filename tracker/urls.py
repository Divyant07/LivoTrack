from django.urls import path
from .views import userprofile_register, user_login, dashboard, onboarding,welcome_page, edit_profile, change_password, home, report_view, reset_daily_data

urlpatterns = [
    path('', welcome_page, name='welcome_page'),
    path('userprofile_register/', userprofile_register, name='userprofile_register'),
    path('userprofile_login/', user_login, name='userprofile_login'),
    path('dashboard/', dashboard, name='dashboard'),
    path('onboarding/', onboarding, name='onboarding'),
    path('edit-profile/', edit_profile, name='edit_profile'),
    path('change-password/', change_password, name='change_password'),
    path('home/', home, name='home'),
    path('report/', report_view, name='report'),
    path('reset-daily-data/', reset_daily_data, name='reset_daily_data'),
]