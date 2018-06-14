from django.http import HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import render
from superpigeons_apps.user.models import UserInfo
from superpigeons_apps.blog.forms import WriteArticle
from superpigeons_apps.blog.models import Article, Comment, ArticleSeen, Tags
from common.Decorator import article_inter_permission
from common.rePaginator import NewPaginator
from common.level import Level
from django.db.models import Q
import traceback
import json


# 博客主页
def blog_index(request):
    article = Article.objects.all().order_by('-mod_date')
    top_seen_article = Article.objects.all().values('id', 'title', 'seen_count').order_by('-seen_count')[:10]
    current_page = request.GET.get("page", 1)
    pages = NewPaginator(article, 10)
    article = pages.page(current_page)
    tags = Tags.objects.all()
    context = dict()
    context['tags'] = tags
    context['top_seen_article'] = top_seen_article
    context['article'] = article
    context['pages'] = pages
    return render(request, 'blog_index.html', context)


# 博客内容页
def blog_article(request, artid):
    try:
        seener_csrf = request.COOKIES.get('csrftoken')
        article = Article.objects.get(id=artid)
        comment = Comment.objects.filter(comment_article__id=artid)
        userinfo = UserInfo.objects.get(user_id=article.auther_id)
        seener = str(request.user)
        other_articles = Article.objects.filter(auther=article.auther_id).exclude(id=artid).values('title', 'id').order_by("-seen_count")[:10]
        # 判断是否浏览过
        if ArticleSeen.objects.filter(seen_csrf=seener_csrf, seen_article=article).exists():
            pass
        else:
            ArticleSeen.objects.create(seen_csrf=seener_csrf, seen_article=article, seener=seener)
            article.seen_count = ArticleSeen.objects.filter(seen_article=article).count()
            article.save()
        context = dict()
        context['other_articles'] = other_articles
        context['article'] = article
        context['userinfo'] = userinfo
        context['comment'] = comment
    except Exception as e:
        traceback.print_exc()
    else:
        return render(request, 'blog_article.html', context)


# 博客评论
def blog_comment(request):
    try:
        comment_art_id = request.POST['comment_art_id']
        comment_text = request.POST['comment_text']
        commenter_id = request.POST['commenter_id']
        comment_type = request.POST['comment_type']
        comment_target = request.POST['comment_target']
        comment_tree = request.POST['comment_tree']
        commenter = User.objects.get(id=commenter_id)
        if comment_type == 'art_comment':
            article = Article.objects.get(id=comment_art_id)
            Comment.objects.create(commenter=commenter, comment_article=article, text=comment_text)
            article.comment_count = Comment.objects.filter(comment_article=article).count()
            article.save()
        if comment_type == 'com_comment':
            target_comment = Comment.objects.get(id=comment_target)
            tree_comment = Comment.objects.get(id=comment_tree)
            Comment.objects.create(commenter=commenter, recomment_target=target_comment, recomment_tree=tree_comment, text=comment_text)
    except Exception as e:
        traceback.print_exc()
        return HttpResponse(e)
    else:
        # 加积分 每日登陆=a 写文章=b 评论=c 点赞=d
        lev = Level(request.user)
        lev.comput_level("c")
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
            articles = Article.objects.filter(auther=request.user)
            used_tags = []
            # 从已写的博客中找到已用的tag
            for i in articles:
                for t in i.tags.all():
                    used_tags.append(t.id)
            # 去重
            used_tags = list(set(used_tags))
            context = dict()
            context['used_tags'] = used_tags
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
                    # 加积分 每日登陆=a 写文章=b 评论=c 点赞=d
                    lev = Level(request.user)
                    lev.comput_level("b")
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
            articles = Article.objects.filter(auther=request.user)
            used_tags = []
            # 从已写的博客中找到已用的tag
            for i in articles:
                for t in i.tags.all():
                    used_tags.append(t.id)
            # 去重
            used_tags = list(set(used_tags))
            context = dict()
            context['used_tags'] = used_tags
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
            traceback.print_exc()
            return HttpResponse(e)
        else:
            return HttpResponse('success')


# 新增删除标签
def tags_edit(request):
    commenter = User.objects.get(username=request.user)
    if request.POST['type'] == 'add':
        if Tags.objects.filter(tag_name=request.POST['tag_name']).exists():
            return HttpResponse('该标签已存在')
        else:
            try:
                newtag = Tags.objects.create(tag_name=request.POST['tag_name'], is_common=0, commenter=commenter)
                dic = dict()
                dic[newtag.id] = newtag.tag_name
            except Exception as e:
                traceback.print_exc()
                return HttpResponse(e)
            else:
                return HttpResponse(json.dumps(dic), content_type="application/json")
    if request.POST['type'] == 'delete':
        Tags.objects.filter(id=request.POST['tag_id']).delete()
        return HttpResponse('success')
