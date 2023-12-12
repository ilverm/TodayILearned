from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.db.models import F

from tags.models import Tag

from .models import Post
from .forms import PostForm

from likes.models import Like

User = get_user_model()

def home_page(request):
    post_qs = Post.objects.all()
    context = {'post_qs': post_qs}
    return render(request, 'home.html', context=context)

@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data.get('title')
            source = form.cleaned_data.get('source')
            tag = form.cleaned_data.get('tag')
            new_post = Post.objects.create(title=title, source=source, author=request.user)
            tag, _ = Tag.objects.get_or_create(name=tag)
            new_post.tag.add(tag)
            return HttpResponseRedirect(reverse('home'))
    else:
        form = PostForm()
    return render(request, 'create.html', {'form': form})

@login_required
def single_post_view(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)
    user = request.user
    like, _ = Like.objects.get_or_create(user=user, post=post)
    if request.method == 'POST':
        # Check if the user has already liked or disliked the post
        if 'like' in request.POST:
            post.likes = F('likes') + 1
            like.liked = True
        if 'dislike' in request.POST:
            post.likes = F('likes') - 1
            like.liked = False
            
    post.save()
    post.refresh_from_db()
    like.save()

    context = {
        'single_post': post, 
        'likes': post.likes,
        'liked': like.liked,
        }
    return render(request, 'single_post.html', context=context)