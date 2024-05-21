import re

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.db.models import Q, F, Count
from django.core.exceptions import ObjectDoesNotExist

from .models import Post
from .forms import PostForm, UpdatePostForm

from likes.models import Like

from tags.models import Tag

from users.forms import CustomUserCreationForm

User = get_user_model()

def home_page(request):
    post_qs = Post.objects.filter(private=False).order_by('-created_at')
    no_posts_per_tag = Tag.objects.annotate(num_posts=Count('posts_tag'))[:10]
    context = {'post_qs': post_qs, 'posts_per_tag': no_posts_per_tag}
    return render(request, 'home.html', context=context)

def search(request):
    searched = request.GET.get('q')
    not_private = Post.objects.filter(private=False)
    try:
        qs = not_private.filter(
            Q(title__icontains=searched) | 
            Q(content__icontains=searched) | 
            Q(tag__name__icontains=searched))
        context = {
            'searched': qs
        }
        return render(request, 'searched.html', context=context)
    except ValueError:
        return render(request, 'searched.html')

@login_required
def create_post(request):
    if request.method == 'GET':
        form = PostForm()
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data.get('title')
            slug = form.cleaned_data.get('slug')
            content = form.cleaned_data.get('content')
            source = form.cleaned_data.get('source')
            tag = form.cleaned_data.get('tag')
            tag, _ = Tag.objects.get_or_create(name=tag)
            Post.objects.create(
                title=title,
                slug=slug,
                content=content, 
                source=source, 
                author=request.user, 
                tag=tag
            )

            return HttpResponseRedirect(reverse('home'))
    return render(request, 'create.html', {'form': form})

def single_post_view(request, year, slug):
    post = get_object_or_404(Post, created_at__year=year, slug=slug, private=False)
    try:
        liked = Like.objects.get(post=post).liked
    except ObjectDoesNotExist:
        liked = False
    context = {'single_post': post, 'likes': post.likes, 'liked': liked}
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

def tag_view(request, tag):
    if request.method == 'GET':
        posts_filtered_by_tag = Post.objects.filter(tag__name=tag)
        context = {'posts': posts_filtered_by_tag, 'tag': tag}
        return render(request, 'filtered_by_tag.html', context=context)
    
def personal_page(request, username):
    if request.method == 'GET':
        posts_filtered_by_author = Post.objects.filter(author__username=username)
        context = {'posts': posts_filtered_by_author, 'username': username}
        return render(request, 'personal_page.html', context=context)
    if request.method == 'POST':
        pattern = re.compile(r'make_private\s-\s\d+')
        is_private = {
            k[-1]: request.POST[k] for k in request.POST.keys() if pattern.search(k)
        }
        post_id = list(is_private.keys())[0]
        post = Post.objects.get(id=int(post_id))
        post.private = False if 'on' in is_private.values() else True
        post.save()
        return HttpResponseRedirect(reverse('personal_page', kwargs={'username': username}))

    
@login_required
def delete_article(request, slug):
    try:
        Post.objects.get(author=request.user, slug=slug).delete()
        return HttpResponseRedirect(reverse('personal_page', kwargs={'username': request.user.username}))
    except ObjectDoesNotExist:
        return HttpResponseRedirect(reverse('home'))
    
@login_required
def update_article(request, slug):
    try:
        post = Post.objects.get(author=request.user, slug=slug)
    except ObjectDoesNotExist:
        return HttpResponseRedirect(reverse('home'))
    initial_values = {
        'title': post.title,
        'slug': post.slug,
        'content': post.content,
        'source': post.source,
        'tag': post.tag,
        'private': post.private
    }
    form = UpdatePostForm(initial=initial_values)
    if request.method == 'POST':
        form = UpdatePostForm(request.POST, initial=initial_values)
        updated_fields = {
            k: request.POST.get(k) for k in form.changed_data if form.has_changed()
        }
        tag, _ = Tag.objects.get_or_create(name=updated_fields['tag'])
        updated_fields['tag'] = tag
        # if checkbox is checked 'on' is in getlist_private else getlist_private is empty
        getlist_private = request.POST.getlist('private')
        updated_fields['private'] = True if 'on' in getlist_private else False
        Post.objects.filter(author=request.user, slug=slug).update(**updated_fields)
        return HttpResponseRedirect(reverse(
            'single_post', kwargs={'year': post.created_at.year, 'slug': post.slug}
        ))
    context = {
        'form': form,
        'title': post.title
    }
    return render(request, 'update.html', context=context)