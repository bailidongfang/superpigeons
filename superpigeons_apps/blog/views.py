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
    try:
        art_id = request.POST['comment_art_id']
        text = request.POST['comment_text']
        commenter_id = request.POST['commenter_id']
        commenter = User.objects.get(id=commenter_id)
        article = Article.objects.get(id=art_id)
        Comment.objects.create(comment_article=article, commenter=commenter, text=text)
    except Exception as e:
        return HttpResponse(e)
    else:
        return HttpResponse('success')


def blog_edit(request, artid):
    if artid == 'new':
        # 新建博客
        if request.method == 'GET':
            form = WriteArticle()
            userinfo = UserInfo.objects.get(user__username=request.user)
            context = dict()
            context['userinfo'] = userinfo
            context['form'] = form
            context['template_type'] = 'new'
            return render(request, 'blog_write.html', context)
        if request.method == 'POST':
            writeform=WriteArticle(request.POST)
            if writeform.is_valid():
                # 提取form数据
                title = writeform.cleaned_data.get("title")
                text = writeform.cleaned_data.get("text")
            try:
                user = User.objects.get(username=request.user)
                article = Article.objects.create(title=title, text=text, auther=user)
            except Exception as e:
                return HttpResponse(e)
            return HttpResponse('success')
    else:
        # 修改博客
        if request.method == 'GET':
            # 获取博客数据
            article = Article.objects.get(id=artid)
            init = {
                'title': article.title,
                'text': article.text
            }
            form = WriteArticle(initial=init)
            userinfo = UserInfo.objects.get(user__username=request.user)
            context = dict()
            context['userinfo'] = userinfo
            context['form'] = form
            context['template_type'] = artid
            return render(request, 'blog_write.html', context)
        if request.method == 'POST':
            writeform=WriteArticle(request.POST)
            if writeform.is_valid():
                # 提取form数据
                title = writeform.cleaned_data.get("title")
                text = writeform.cleaned_data.get("text")
            try:
                user = User.objects.get(username=request.user)
                article = Article.objects.get(id=artid)
                article.title = title
                article.text = text
                article.save()
            except Exception as e:
                return HttpResponse(e)
            return HttpResponse('success')


def test(request):
    return render(request, 'test.html')


