from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import Http404

from .models import BlogPost, Entry
from .forms import BlogPostForm, EntryForm

from django.db.models import Q
# Create your views here.

def index(request):
	"""The home page for blog."""
	return render(request, 'blogs/index.html')

def _get_topics_for_user(user):
    """ returns a queryset of topics the user can access """
    q = Q(public=True)
    # if django < 1.10 you want "user.is_authenticated()" (with parens)
    if user.is_authenticated:
       # adds user's own private topics to the query
       q = q | Q(public=False, owner=user)

    return BlogPost.objects.filter(q)


def blogposts(request):
	"""Show all blogposts."""
	blogposts = _get_topics_for_user(request.user).order_by('date_added')
	context = {'blogposts': blogposts}
	return render(request, 'blogs/blogposts.html', context)


def blogpost(request, blogpost_id):
	blogposts = _get_topics_for_user(request.user)
    # here we're passing the filtered queryset, so
    # if the topic "topic_id" is private and the user is either
    # anonymous or not the topic owner, it will raise a 404 
	"""Show a single blogpost and all its entries."""
	blogpost = get_object_or_404(blogposts, id=blogpost_id)
	# Make sure the topic belogs to the current user.

	entries = blogpost.entry_set.order_by('-date_added')
	context = {'blogpost': blogpost, 'entries': entries}
	return render(request, 'blogs/blogpost.html', context)

@login_required
def new_blogpost(request):
	"""Add a new blogpost."""
	if request.method != 'POST':
		# No data submitted; create a blank form.
		form = BlogPostForm()
	else:
		# Post data submitted; process data.
		form = BlogPostForm(data=request.POST)
		if form.is_valid():
			new_blogpost = form.save(commit=False)
			new_blogpost.owner = request.user
			new_blogpost.save()
			return redirect('blogs:blogposts')

	# Display a blank or invalid form.
	context = {'form': form}
	return render(request, 'blogs/new_blogpost.html', context)

@login_required
def delete_blogpost(request, blogpost_id):
	blogpost = get_object_or_404(BlogPost, id=blogpost_id)
	check_topic_owner(blogpost.owner, request)

	if request.method == 'POST':
		blogpost.delete()
		messages.success(request, "Topic successfully deleted!")
		return redirect('blogs:blogposts')

	# Display a blank or invalid form.
	context = {'blogpost': blogpost}
	return render(request, 'blogs/delete_blogpost.html', context)



@login_required
def new_entry(request, blogpost_id):
	"""Add a new entry for a particular blogpost."""
	blogpost = get_object_or_404(BlogPost, id=blogpost_id)
	check_topic_owner(blogpost.owner, request)

	if request.method != "POST":
		# No data submitted; create a blank form.
		form = EntryForm()
	else:
		# POST data submitted; process data.
		form = EntryForm(data=request.POST)
		if form.is_valid():
			new_entry = form.save(commit=False)
			new_entry.blogpost = blogpost
			new_entry.save()
			return redirect('blogs:blogpost', blogpost_id=blogpost_id)

	# Display a blank or invalid form.
	context = {'blogpost': blogpost, 'form': form}
	return render(request, 'blogs/new_entry.html', context)

@login_required
def edit_entry(request, entry_id):
	"""Edit an existing entry."""
	entry = get_object_or_404(Entry, id=entry_id)
	blogpost = entry.blogpost
	check_topic_owner(blogpost.owner, request)

	if request.method != "POST":
		# Initial request; pre-fill form with the current entry.
		form = EntryForm(instance=entry)
	else:
		# POST data sumbmitted; process data.
		form = EntryForm(instance=entry, data=request.POST)
		if form.is_valid():
			form.save()
			return redirect('blogs:blogpost', blogpost_id=blogpost.id)

	context = {'entry': entry, 'blogpost': blogpost, 'form': form}
	return render(request, 'blogs/edit_entry.html', context)

@login_required
def delete_entry(request, entry_id):
	entry = get_object_or_404(Entry, id=entry_id)
	blogpost = entry.blogpost
	check_topic_owner(blogpost.owner, request)

	if request.method == 'POST':
		entry.delete()
		messages.success(request, "Post successfully deleted!")
		return redirect('blogs:blogpost', blogpost_id=blogpost.id)

	# Display a blank or invalid form.
	context = {'entry': entry, 'blogpost': blogpost}
	return render(request, 'blogs/delete_entry.html', context)

def check_topic_owner(owner, request):
	if owner != request.user:
		raise Http404

