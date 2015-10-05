from django.shortcuts import render, redirect, render_to_response
from .models import *
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import Http404
from django.views.decorators.cache import cache_page
from .forms import MessageForm


# 全局传递的数据
def base(request):
    cat = Category.objects.all()
    tag_list = Tag.objects.all()
    recommendation = Article.objects.filter(is_recommend=True)[:7]
    return locals()


# 获取文章列表
@cache_page(60 * 15)  # 页面缓存
def article_view(request):
    article_list = Article.objects.all()
    article_list = get_page(request, article_list)
    return render(request, 'index.html', locals())


# 文章详细
def content_detail(request, title):
    try:
        content = Article.objects.get(title=title)
        content.click_count += 1
        content.save()
    except Article.DoesNotExist:
        raise Http404
    return render(request, 'content.html', locals())


# 文章分类
def get_category(request, category):
    is_cat = True
    try:
        category = Category.objects.get(name=category)
        article_list = Article.objects.filter(category_id=category.id)
        article_list = get_page(request, article_list)
    except Category.DoesNotExist:
        raise Http404
    return render(request, 'index.html', locals())


def me(request):
    return render(request, 'me.html')


# 分页函数
def get_page(request, article_list, num=4):
    paginator = Paginator(article_list, num)
    try:
        page = request.GET.get('page')
        article_list = paginator.page(page)
    except EmptyPage:
        article_list = paginator.page(paginator.num_pages)
    except PageNotAnInteger:
        article_list = paginator.page(1)
    return article_list


# 文章归档
@cache_page(60 * 15)
def get_archive(request):
    archive_list = []
    cat_list = Category.objects.all()
    for c, x in enumerate(cat_list):
        archive_list.insert(c, [x.name, x.article_set.all()])
    return render(request, 'archive.html', locals())


# 标签云
def get_tag(request, tag):
    is_tag = True
    try:
        try:
            int(tag)
            tag = Tag.objects.get(id=tag)
        except ValueError:
            tag = Tag.objects.get(name=tag)
        article_list = get_page(request, tag.article_set.all())
    except Tag.DoesNotExist:
        raise Http404('Tag does not exist!')
    return render(request, 'index.html', locals())


# 搜索
def search(request):
    is_search = True
    title = request.GET.get('search')
    article_list = get_page(request, Article.objects.filter(title__icontains=title))
    return render(request, 'index.html', locals())


# 留言
def message(request):
    message_list = get_page(request, Message.objects.all(), num=9)
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            Message.objects.create(username=form.cleaned_data['username'],
                                   content=form.cleaned_data['content'])
            return redirect(message)
    else:
        form = MessageForm()
    return render(request, 'message.html', {'article_list': message_list, 'form': form})

