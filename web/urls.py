from django.contrib import admin
from django.urls import path
from app import views
from django.contrib.auth import views as auth_views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.main),
    path('signup',views.signup),
    path('account',views.account),
    path('account_check',views.account_check),
    path('login',views.login),
    path('editprofile',views.editaccount),
    path('password',views.password),
    path('logout',views.logout),
    path("password_reset", views.password_reset_request, name="password_reset"),
    path('password_reset/done/',auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="password_reset_confirm.html"), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), name='password_reset_complete'),
    path('home/',views.home),
    path('home/k/<str:group_name>/',views.index),
    path('home/ok/<str:group_name>/',views.dindex),
    path('privacy',views.privacy),
    path('policy',views.policy),
    path('support',views.support),
    path('feedback',views.feedback),
    path('report',views.report),
    path('form',views.formin),
    path('wc',views.wc)
]
urlpatterns += staticfiles_urlpatterns()