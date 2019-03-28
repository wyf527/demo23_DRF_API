"""demo23_DRF_API URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from rest_framework.documentation import include_docs_urls
from rest_framework.routers import DefaultRouter, SimpleRouter

from API import views
from demo23_DRF_API import settings

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    # url(r'^', include('API.urls')),
    url(r'^docs/',include_docs_urls(title='MY API FILE')),
]

#1.创建路由器对象
router=DefaultRouter()
# router=SimpleRouter()

# 2.调用register方法，配置路由的信息prefix, viewset, basename=None
# 相当于 url(r'^actors/$', views1.ActorListView.as_view()),
#     url(r'^actors/(?P<pk>\d+)/$', views1.ActorDetailView.as_view()),
router.register('actors',views.ActorListView,basename='actors')
router.register('movies',views.MovieListView,basename='movies')


#3.加入url列表
urlpatterns+=router.urls

#DRF前端页面图片链接无之url配置
from django.conf.urls.static import static
if settings.DEBUG:
  urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
