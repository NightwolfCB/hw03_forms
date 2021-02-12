from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import PostForm
from .models import Group, Post, User


def index(request):
    post_list = Post.objects.all()
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number) 
    return render(
         request,
         'index.html',
         {'page': page,}
     )


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    posts = group.posts.all()[:11]
    return render(request, 'group.html', {'group': group, 'posts': posts})


@login_required
def new_post(request):
    form = PostForm(request.POST or None)
    if form.is_valid():
        new_post = form.save(commit=False)
        new_post.author = request.user
        new_post.save()
        return redirect('index')
    return render(request, 'new.html', {'form': form})


def profile(request, username):
    author = get_object_or_404(User, username=username)
    posts_latest = author.posts.all().order_by('-pub_date')
    paginator = Paginator(posts_latest, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    context = {
        'page': page,
        'posts_latest': posts_latest,
        'author': author
    }
    return render(request, 'profile.html', context)
 
 
def post_view(request, username, post_id):
    author = get_object_or_404(User, username=username)
    post = get_object_or_404(Post, id=post_id, author=author)
    context = {
        'author': author,
        'post': post        
    }
    return render(request, 'post.html', context)


@login_required
def post_edit(request, username, post_id):
    author = get_object_or_404(User, username=username)
    item = get_object_or_404(Post, id=post_id)
    if request.user != author:
        raise Http404('Вы не можете редактировать эту публикацию')
    else:
        if request.method == 'POST':
            form = PostForm(request.POST, instance=item)
            if form.is_valid():
                edit_item = form.save(commit=False)
                item.text = edit_item.text
                item.group = edit_item.group
                item.save()
                return redirect('posts:post', item.author, item.id)
    form = PostForm(instance=item)
    return render(request, 'post_edit.html', {'form': form, })
