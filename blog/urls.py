from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.sitemaps.views import sitemap
from article.sitemaps import ArticleSitemap, CategorySitemap, TagSitemap
from article.feeds import AllArticleRssFeed

from rest_framework.routers import DefaultRouter
from api import views as api_views
if settings.API_FLAG:
    router = DefaultRouter()
    router.register(r'users', api_views.UserListSet)
    router.register(r'articles', api_views.ArticleListSet)
    router.register(r'tags', api_views.TagListSet)
    router.register(r'categorys', api_views.CategoryListSet)

# 网站地图
sitemaps = {
    'articles': ArticleSitemap,
    'tags': TagSitemap,
    'categories': CategorySitemap
}

urlpatterns = [
    # 用户
    path('admin/', admin.site.urls),
    # url(r'^tinymce/', include('tinymce.urls')),  # 使用富文本编辑框配置
    url(r'^search', include('haystack.urls')),  # 全文检索框架

    url(r'^accounts/', include(('user.urls', 'user'), namespace='accounts')),  # 用户模块
    url('', include(('article.urls', 'article'), namespace='blog')),  # blog
    url(r'^comment/', include(('comment.urls', 'comment'), namespace='comment')),  # 评论
    url(r'^sitemap\.xml$', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),  # 网站地图
    url(r'^feed/$', AllArticleRssFeed(), name='rss'),  # rss订阅

    # url(r'^/', include(('goods.urls', 'goods'), namespace='goods')),  # 商品模块
    # url(r'^comment/', include('comment.urls', namespace='comment')),  # comment

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # 加入这个才能显示media文件

if settings.API_FLAG:
    urlpatterns.append(url(r'^api/v1/', include((router.urls, 'api'), namespace='api')))    # restframework