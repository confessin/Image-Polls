from django.conf.urls.defaults import patterns, include, url


urlpatterns = patterns('main.views',
    # Examples:
    url(r'^$', 'index', name='home'),
    url(r'^upload_image$', 'show_image', name='upload_image'),
    url(r'^user_images/(?P<image_id>\d+)$', 'serve_user_image'),
    url(r'^submit_poll/(?P<image_id>\d+)/$', 'submit_poll', name='submit_poll'),
    url(r'^show/(?P<poll_id>\d+)/$', 'show_poll', name='show_poll'),
    url(r'^show/random/$', 'show_poll', name='show_random_poll'),
    url(r'^vote/(?P<poll_id>\d+)/$', 'vote', name='vote'),
    )
