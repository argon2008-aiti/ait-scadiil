from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    # Examples:
    # url(r'^$', 'ait_ilcdmp.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include('info_system.urls.admin', namespace='admin')),
    url(r'^student/', include('info_system.urls.student', namespace='student')),
    url(r'^admin/', include(admin.site.urls)),
]
