from django.conf.urls import patterns, url
# from django.conf.urls import include
# from django.contrib import admin
from tree.views import render_tree, ajax_get_tree, ajax_remove_subtree, ajax_update_name

from django.conf.urls.static import static
from django.conf import settings

urlpatterns = patterns('',
                       # Examples:
                       url(r'^$', render_tree),
                       url(r'^ajax_get_tree/$', ajax_get_tree),
                       url(r'^ajax_remove_subtree/$', ajax_remove_subtree),
                       url(r'^ajax_update_name/$', ajax_update_name),
                       # url(r'^admin/', include(admin.site.urls)),
                       )
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
