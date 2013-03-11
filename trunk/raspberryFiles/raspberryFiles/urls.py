from django.conf.urls import patterns, include, url
from views import *
from django.conf.urls.static import static

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'raspberryFiles.views.home', name='home'),
    # url(r'^raspberryFiles/', include('raspberryFiles.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
    url(r'^$', home),
    url(r'^files/$', files), 
    url(r'^files/(?P<directory>[\w\W]+)+', files_subdirectory), 
    url(r'^settings', settings),
    url(r'^list/$', 'list', name='list'),
    url(r'^test/$', test_root),
    url(r'^test/(?P<directory>[\w\W]+)+', test)   
   # url(r'^upload', upload_file),
    )
