from django.views.static import * 
from django.conf import settings

from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('Library.library.views',
    # Examples:
    url(r'^books/$', 'book_list', name='browse'),
    url(r'^books/(?P<book_id>\d+)/$', 'detail', name='detail'),
    url(r'^books/create/$', 'create', name='create'),
    url(r'^books/createa/$', 'createa', name='createa'),
    url(r'^books/(?P<book_id>\d+)/delete/$', 'delete', name='delete'),
    url(r'^books/(?P<book_id>\d+)/borrow/$', 'loanx', name = 'loan'),
    url(r'^books/(?P<book_id>\d+)/borrowa/$', 'loanx', name = 'loana'),

    url(r'^books/(?P<book_id>\d+)/return/$', 'return_book', name = 'return_book'),
    url(r'^books/(?P<book_id>\d+)/returna/$', 'return_book', name = 'return_booka'),
    url(r'^books/scan/$', 'scanx',name='scan'),
    url(r'^books/scana/$', 'scanx',name='scana'),

    url(r'^accounts/register/$', 'register', name='register'),
    url(r'^books/user_books/$', 'user_books', name='user_books'),
    url(r'^books/search/$', 'search_googlex', name='search'),
    url(r'^books/searcha/$', 'search_googlex', name='searcha'),)

urlpatterns += patterns('',
    url(r'^accounts/login/$', 'django.contrib.auth.views.login', name = 'login'),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout', {'next_page': '/books/'}, name = 'logout'),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
)
