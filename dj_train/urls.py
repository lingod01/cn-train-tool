from django.conf.urls.defaults import *

urlpatterns = patterns('',
    # Example:
    (r'^train/', include('train.web.urls')),
    (r'^ui/', include('train.ui.urls')),
    (r'^m/', include('train.mobile.urls')),
)
