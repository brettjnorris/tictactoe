from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from rest_framework import routers
from main import views

from django.contrib import admin
admin.autodiscover()

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'games', views.GameViewSet)
router.register(r'moves', views.MoveViewSet)


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'tictactoe.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', TemplateView.as_view(template_name='index.html')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/', include(router.urls)),
)
