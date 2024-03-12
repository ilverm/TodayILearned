from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.db.models import F, Count

from .models import Post
from .forms import PostForm

from likes.models import Like

from tags.models import Tag

from users.forms import CustomUserCreationForm

User = get_user_model()

def home_page(request):
    post_qs = Post.objects.filter(private=False).order_by('-created_at')
    no_posts_per_tags = Tag.objects.annotate(num_posts=Count('posts_tag'))[:9]
    context = {'post_qs': post_qs, 'posts_per_tag': no_posts_per_tags}
    return render(request, 'home.html', context=context)

@login_required
def create_post(request):
    if request.method == 'GET':
        form = PostForm()
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data.get('title')
            content = form.cleaned_data.get('content')
            source = form.cleaned_data.get('source')
            tag = form.cleaned_data.get('tag')
            tag, _ = Tag.objects.get_or_create(name=tag)
            Post.objects.create(
                title=title, 
                content=content, 
                source=source, 
                author=request.user, 
                tag=tag
            )
            return HttpResponseRedirect(reverse('home'))
    return render(request, 'create.html', {'form': form})

def single_post_view(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)
    context = {'single_post': post, 'likes': post.likes}
    if request.method == 'POST' and request.user.is_authenticated:
        # Check if the user has already liked or disliked the post
        like, _ = Like.objects.get_or_create(user=request.user, post=post)
        if 'like' in request.POST:
            post.likes = F('likes') + 1
            like.liked = True
        if 'dislike' in request.POST:
            post.likes = F('likes') - 1
            like.liked = False

        context['liked'] = like.liked
            
        post.save()
        post.refresh_from_db()
        like.save()

    return render(request, 'single_post.html', context=context)

def create_account(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('login'))
    form = CustomUserCreationForm()
    return render(request, 'registration/create_account.html', {'form': form})