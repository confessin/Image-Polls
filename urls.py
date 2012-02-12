from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.defaults import *

handler500 = 'djangotoolbox.errorviews.server_error'

urlpatterns = patterns('',
    (r'^image_polling/', include('main.urls')),
    ('^_ah/warmup$', 'djangoappengine.views.warmup'),
    url(r'^vote_or_die/$', 'django.views.generic.simple.direct_to_template',
        {'template':'vote_or_die.html'}, name='vote_campaign'),
    url(r'^about/$', 'django.views.generic.simple.direct_to_template',
        {'template':'about.html'}, name='about'),
    # for google webmasters verification.
    url(r'^googlebfe22224fa5be37c.html$', 'django.views.generic.simple.direct_to_template',
        {'template':'googlebfe22224fa5be37c.html'}),
    # robots.txt
    url(r'^googlebfe22224fa5be37c.html$', 'django.views.generic.simple.direct_to_template',
        {'template':'googlebfe22224fa5be37c.html'}, name='about'),
    (r'^$', include('main.urls')),
)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
