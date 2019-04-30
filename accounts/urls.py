from django.conf.urls import url
from . import views

urlpatterns = [

    # Login and Logout User
    url(r'^login/$', views.UserLoginView.as_view()),
    url(r'^logout/$', views.UserLogoutView.as_view()),

    # Register User
    url(r'^signup/$', views.UserCreateView.as_view()),

    # user mail verification
    url(r'^mail_verify/(?P<id>\w+)/$', views.MailVerificationView, name='mail-verify'),

    # update user password
    url(r'^password_update/$', views.UserPasswordUpdateView.as_view(), name='password-update'),

    # user forgot password operation.
    url(r'^forgot_password_update/(?P<id>\w+)/$', views.ForgotUserPasswordUpdateView.as_view(), name='forgot-password'),
    url(r'^forgot_password/', views.password_forgot, name='forgot_update'),

    # Update User
    url(r'^update/(?P<pk>\d+)/$', views.UserUpdateView.as_view(), name='user-update'),
    url(r'^email_verify/(?P<id>\w+)/$', views.EmailChangeVerifyView.as_view(), name='email-verify'),

]