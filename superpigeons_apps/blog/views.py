from django.shortcuts import render
from superpigeons_apps.user.models import UserInfo
from superpigeons_apps.blog.forms import WriteArticle
from superpigeons_apps.blog.models import Article
# Create your views here.


def blog_index(request):
    article = Article.objects.values('id', 'auther_id', 'title').order_by('-mod_date')
    context = dict()
    context['article'] = article
    return render(request, 'blog.html', context)


def blog_article(request,artid):
    article = Article.objects.get(id=artid)
    context = dict()
    context['article'] = article
    return render(request, 'blog_article.html', context)


def blog_write(request):
    form = WriteArticle()
    userinfo = UserInfo.objects.get(user__username='bailidf')
    context = dict()
    context['t'] = 'aaaa'
    context['userinfo'] = userinfo
    context['form'] = form
    return render(request, 'blog_write.html', context)


def test(request):
    return render(request, 'test.html')


