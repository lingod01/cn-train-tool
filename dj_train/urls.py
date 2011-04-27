from django.conf.urls.defaults import *
from django.conf import settings


urlpatterns = patterns('',
    # Example:
    (r'^train/', include('train.web.urls')),
    (r'^ui/', include('train.ui.urls')),
    (r'^m/', include('train.mobile.urls')),
    (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
)
