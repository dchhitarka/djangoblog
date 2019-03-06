from django.urls import path
from . import views
from django.contrib.sitemaps.views import sitemap
from .sitemaps import PostSitemap
from .feeds import LatestPostsFeed

sitemaps = {
    'posts': PostSitemap,
}

urlpatterns = [
    path('', views.list_view, name='home'),
    path('<int:post_id>/detail/', views.detail_delete_view, name='detail'),
    path('<int:post_id>/delete/', views.detail_delete_view, name='delete'),
    path('create/', views.create_update_view, name='create'),
    path('<int:post_id>/edit/', views.create_update_view, name='update'),
    path('<int:post_id>/edit/', views.create_update_view, name='update'),
    path('<int:post_id>/share/', views.post_share, name='share'),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps},name='django.contrib.sitemaps.views.sitemap'),
    path('feed/', LatestPostsFeed(), name='post_feed'),
]

