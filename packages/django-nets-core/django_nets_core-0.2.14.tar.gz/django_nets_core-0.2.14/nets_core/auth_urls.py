from django.urls import path
from nets_core.google_auth import login_with_google
from . import views

app_name = 'nets_core_auth_api'

urlpatterns = [
    path('loginWithGoogle/', login_with_google, name='loginWithGoogle'),
    path('login/', views.auth_login, name='login'),
    path('logout/', views.auth_logout, name='logout'),
    path('authenticate/', views.auth, name='authenticate'),
    path('update/', views.update_user, name='update'),
    path('getProfile/', views.auth_get_profile, name='getProfile'),
    path('requestDelete/', views.request_delete_user_account, name='requestDelete'),
    path('delete/', views.delete_user_account, name='delete'),
]