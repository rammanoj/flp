from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^team/create/$', views.TeamCreateView.as_view()),
    url(r'^team/$', views.TeamListView.as_view()),
    url(r'^team/(?P<pk>\d+)/$', views.TeamRetrieveUpdateDestroyView.as_view()),
    url(r'^team/invite/$', views.TeamAddUser.as_view()),
    url(r'^team/user/edit/$', views.TeamAddorRemoveUser.as_view()),
    url(r'^team/users/(?P<pk>\d+)/$', views.TeamUserListView.as_view()),
    url(r'^user/team/$', views.UserTeamListView.as_view()),
    url(r'^user/team/delete/(?P<pk>\d+)/(?P<user>\d+)/$', views.TeamUserDeleteView.as_view()),
]