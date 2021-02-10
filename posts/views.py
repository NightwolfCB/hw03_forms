from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import PostForm
from .models import Group, Post


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
    author_posts = User.objects.get(username=username)
    posts_count = Post.objects.count(username=username) # нам надо как-то передать количество постов автора
    context = {
        "page": page,
        "author_posts": author_posts
    }
    return render(request, 'profile.html', context)
 
 
def post_view(request, username, post_id):
        # тут тело функции
    return render(request, 'post.html', {})

@login_required
def post_edit(request, username, post_id):
        # тут тело функции. Не забудьте проверить, 
        # что текущий пользователь — это автор записи.
        # В качестве шаблона страницы редактирования укажите шаблон создания новой записи
        # который вы создали раньше (вы могли назвать шаблон иначе)
    return render(request, 'post_new.html', {})
