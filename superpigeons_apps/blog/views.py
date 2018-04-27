from django.http import HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import render
from superpigeons_apps.user.models import UserInfo
from superpigeons_apps.blog.forms import WriteArticle
from superpigeons_apps.blog.models import Article, Comment


def blog_index(request):
    article = Article.objects.values('id', 'auther__userinfo__nickname', 'auther_id', 'title').order_by('-mod_date')
    context = dict()
    context['article'] = article
    return render(request, 'blog_index.html', context)


def blog_article(request, artid):
    article = Article.objects.get(id=artid)
    comment = Comment.objects.filter(comment_article__id=artid)
    userinfo = UserInfo.objects.get(user_id=article.auther_id)
    context = dict()
    context['article'] = article
    context['userinfo'] = userinfo
    context['comment'] = comment
    return render(request, 'blog_article.html', context)


def blog_comment(request):
    print(request.POST)
    art_id = request.POST['comment_art_id']
    text = request.POST['comment_text']
    commenter_id = request.POST['commenter_id']
    commenter = User.objects.get(id=commenter_id)
    article = Article.objects.get(id=art_id)
    Comment.objects.create(comment_article=article, commenter=commenter, text=text)
    return HttpResponse('success')


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


