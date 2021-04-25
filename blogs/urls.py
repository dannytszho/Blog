"""Defines URL patterns for blogs."""

from django.urls import path
from . import views

app_name = 'blogs'
urlpatterns = [
	# Home page.
	path('', views.index, name='index'),
	# Page shows all BlogPosts.
	path('blogposts/', views.blogposts, name='blogposts'),
	# Page shows a BlogPost.
	path('blogposts/<int:blogpost_id>/', views.blogpost, name='blogpost'),
	# Page for adding a new BlogPost.
	path('new_blogpost/', views.new_blogpost, name='new_blogpost'),
	# Page for adding a new entry.
	path('new_entry/<int:blogpost_id>/', views.new_entry, name='new_entry'),
	# Page for editing an entry.
	path('edit_entry/<int:entry_id>/', views.edit_entry, name='edit_entry'),
	# Page for delete a BlogPost.
	path('blogposts/<int:blogpost_id>/delete_blogpost/', views.delete_blogpost, name='delete_blogpost'),
	# Page for delete an entry.
	path('delete_entry/<int:entry_id>/', views.delete_entry, name='delete_entry'),



]