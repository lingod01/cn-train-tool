from django.conf.urls.defaults import *
from piston.resource import Resource
from piston.emitters import Emitter
from handlers import TrainHandler
from emitters import TextTableEmitter,HtmlEmitter

yupiao_handler = Resource(TrainHandler)

Emitter.register('txt', TextTableEmitter, 'text/plain; charset=utf-8')
Emitter.register('html', HtmlEmitter, 'text/html; charset=utf-8')

urlpatterns = patterns('',
    url(r'^yupiao\.(?P<emitter_format>.+)$', yupiao_handler),
    url(r'^yupiao$', yupiao_handler, {'emitter_format' : 'html'}),
)
