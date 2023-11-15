from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required

from .models import Post
from .forms import PostForm

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
            Post.objects.create(title=title, source=source, author=request.user)
            return HttpResponseRedirect(reverse('home'))
    else:
        form = PostForm()
    return render(request, 'create.html', {'form': form})