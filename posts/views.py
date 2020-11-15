from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from .models import Group, Post, PostForm


def index(request):
    latest = Post.objects.all() [:11]
    return render(request, 'index.html', {'posts': latest})


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    posts = group.posts.all() [:11]
    return render(request, 'group.html', {'group': group, 'posts': posts})


@login_required
def new_post(request):
    if request.method == 'POST':    
        form = PostForm(request.POST or None)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.author = request.user
            new_post.save()
            return redirect('index')
    form = PostForm()    
    return render(request, 'new.html', {'form': form})