from django.http import HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import render
from superpigeons_apps.user.models import UserInfo
from superpigeons_apps.blog.forms import WriteArticle
from superpigeons_apps.blog.models import Article, Comment, ArticleSeen, Tags
from common.Decorator import article_inter_permission
from common.rePaginator import NewPaginator
from django.db.models import Q
import traceback
import json


# 博客主页
def blog_index(request):
    article = Article.objects.all().order_by('-mod_date')
    current_page = request.GET.get("page", 1)
    pages = NewPaginator(article, 10)
    # article = pages.page(current_page)
    context = dict()
    context['article'] = article
    context['pages'] = pages
    return render(request, 'blog_index.html', context)


# 博客内容页
def blog_article(request, artid):
    seener_csrf = request.COOKIES.get('csrftoken')
    article = Article.objects.get(id=artid)
    comment = Comment.objects.filter(comment_article__id=artid)
    userinfo = UserInfo.objects.get(user_id=article.auther_id)
    # 判断是否浏览过
    if ArticleSeen.objects.filter(seen_csrf=seener_csrf,seen_article=article).exists():
        pass
    else:
        ArticleSeen.objects.create(seen_csrf=seener_csrf, seen_article=article)
        article.seen_count = ArticleSeen.objects.filter(seen_article=article).count()
        article.save()
    context = dict()
    context['article'] = article
    context['userinfo'] = userinfo
    context['comment'] = comment
    return render(request, 'blog_article.html', context)


# 博客评论
def blog_comment(request):
    try:
        art_id = request.POST['comment_art_id']
        text = request.POST['comment_text']
        commenter_id = request.POST['commenter_id']
        commenter = User.objects.get(id=commenter_id)
        article = Article.objects.get(id=art_id)
        Comment.objects.create(comment_article=article, commenter=commenter, text=text)
        article.comment_count = Comment.objects.filter(comment_article=article).count()
        article.save()
    except Exception as e:
        traceback.print_exc()
        return HttpResponse(e)
    else:
        return HttpResponse('success')


# 博客编辑
@article_inter_permission
def blog_edit(request, ftype, artid):
    if ftype == 'add':
        # 新建博客
        if request.method == 'GET':
            form = WriteArticle()
            userinfo = UserInfo.objects.get(user__username=request.user)
            tags = Tags.objects.filter(Q(is_common=1) | Q(commenter__userinfo__username=request.user))
            context = dict()
            context['userinfo'] = userinfo
            context['form'] = form
            context['template_type'] = 'add'
            context['artid'] = 'new'
            context['tags'] = tags
            return render(request, 'blog_write.html', context)
        if request.method == 'POST':
            writeform = WriteArticle(request.POST)
            tags_id = request.POST.getlist('tags')
            if writeform.is_valid():
                # 提取form数据
                title = writeform.cleaned_data.get("title")
                text = writeform.cleaned_data.get("text")
                try:
                    user = User.objects.get(username=request.user)
                    article = Article.objects.create(title=title, text=text, auther=user)
                    article.tags.clear()
                    for i in Tags.objects.filter(id__in=tags_id):
                        article.tags.add(i)
                except Exception as e:
                    traceback.print_exc()
                    return HttpResponse(e)
                else:
                    return HttpResponse('success')
            else:
                return HttpResponse('valid error')
    if ftype == 'modify':
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
            tags = Tags.objects.filter(Q(is_common=1) | Q(commenter__userinfo__username=request.user))
            context = dict()
            context['userinfo'] = userinfo
            context['form'] = form
            context['template_type'] = 'modify'
            context['artid'] = artid
            context['article'] = article
            context['tags'] = tags
            return render(request, 'blog_write.html', context)
        if request.method == 'POST':
            tags_id = request.POST.getlist('tags')
            writeform = WriteArticle(request.POST)
            if writeform.is_valid():
                # 提取form数据
                title = writeform.cleaned_data.get("title")
                text = writeform.cleaned_data.get("text")
            try:
                user = User.objects.get(username=request.user)
                article = Article.objects.get(id=artid)
                article.title = title
                article.text = text
                article.tags.clear()
                for i in Tags.objects.filter(id__in=tags_id):
                    article.tags.add(i)
                article.save()
            except Exception as e:
                print(e)
                return HttpResponse(e)
            return HttpResponse('success')
    if ftype == 'delete':
        try:
            Article.objects.get(id=artid).delete()
        except Exception as e:
            print(e)
            return HttpResponse(e)
        return HttpResponse('success')


# 新增删除标签
def tags_edit(request):
    print(request.POST)
    commenter = User.objects.get(username=request.user)
    if Tags.objects.filter(tag_name=request.POST['tag_name']).exists():
        return HttpResponse(status=502, content='该标签已存在')
    else:
        newtag = Tags.objects.create(tag_name='t测试', is_common=0, commenter=commenter)
    # tags = Tags.objects.filter(Q(is_common=1) | Q(commenter__userinfo__username=request.user))
    dic = dict()
    dic[newtag.id] = newtag.tag_name
    return HttpResponse(json.dumps(dic), content_type="application/json")
