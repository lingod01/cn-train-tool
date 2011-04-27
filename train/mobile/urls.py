from django.conf.urls.defaults import *

urlpatterns = patterns('train.mobile.views',
    url(r'^$', 'index', name = "train_mobile_index"),
)
