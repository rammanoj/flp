from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^team/create/$', views.TeamCreateView.as_view()),
    url(r'^team/$', views.TeamListView.as_view()),
    url(r'^team/(?P<pk>\d+)/$', views.TeamRetrieveUpdateDestroyView.as_view()),
    url(r'^team/invite/$', views.TeamAddUser.as_view()),
    url(r'^team/user/edit/$', views.TeamAddorRemoveUser.as_view()),
    url(r'^team/users/(?P<pk>\d+)/$', views.TeamUserListView.as_view()),
    url(r'^user/team/$', views.TeamListView.as_view()),
    url(r'^user/team/delete/(?P<pk>\d+)/(?P<user>\d+)/$', views.TeamUserDeleteView.as_view()),

    # Subgroup
    url(r'^subgroup/create/(?P<pk>\d+)/$', views.SubGroupCreateView.as_view()),
    url(r'^subgroup/(?P<pk>\d+)/$', views.SubGroupRetrieveUpdateDestroyView.as_view()),

    url(r'^post/create/$', views.PostCreateView.as_view()),
    url(r'^posts/(?P<pk>\d+)/$', views.PostListView.as_view()),
    url(r'^post/(?P<pk>\d+)/$', views.PostRetrieveUpdateDeleteView.as_view()),
    url(r'^post/action/(?P<pk>\d+)/$', views.UpdatePostAction.as_view()),

    url(r'^post/comment/add/(?P<pk>\d+)/$', views.CommentCreateView.as_view()),
    url(r'^post/comments/(?P<pk>\d+)/$', views.CommentListView.as_view()),
    url(r'^post/comment/(?P<pk>\d+)/$', views.CommentRetrieveUpdateDestroyView.as_view()),

    url(r'^recomment/(?P<pk>\d+)/$', views.ReCommentCreateView.as_view()),
    url(r'^recomment/update/(?P<pk>\d+)/$', views.ReCommentRetrieveUpdateDestroyView.as_view()),

    # Notifications List
    url(r'^(?P<pk>\d+)/notifications/$', views.RecentNotifications.as_view()),

    url(r'^(?P<team>\d+)/post/action/(?P<action>\w+)/$', views.Actionusers.as_view())

]