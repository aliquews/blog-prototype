from django.urls import path, re_path

from . import views

urlpatterns = [
    path('',views.index, name='index'),
    re_path(r'^author/(?P<slug>[-\w]+)/$', views.UserDetailView.as_view(), name='user-detail'),
    re_path(r'authors/$', views.UserListView.as_view(), name='users'),
    re_path(r'^author/(?P<slug>[-\w]+)/post/new$',views.PostCreateView.as_view(), name='create-post'),
    re_path(r'^post/(?P<pk>\d+)/$', views.PostDetailView.as_view(), name='post-detail'),
    re_path(r'^post/(?P<pk>\d+)/delete$', views.PostDeleteView.as_view(), name='delete-post'),
    re_path(r'^post/comment/new/(?P<pk>\d+)$', views.CommentCreateView.as_view(), name='new-comment'),
    re_path(r'^comment/(?P<pk>\d+)/delete$', views.CommentDeleteView.as_view(), name='delete-comment'),
    path("register", views.register, name="register"),
]