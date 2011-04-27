import datetime
from piston.handler import BaseHandler
from piston.utils import rc
from train.provider._12306 import yupiao
from django.core.cache import cache
try:
    import json as json
except ImportError,e:
    import simplejson as json

class TrainHandler(BaseHandler):
    allowed_methods = ('GET',)

    def read(self, request):
        """
        Returns trains match the qeury
        """
        date = request.GET.get('date')
        start = request.GET.get('start')
        arrive = request.GET.get('arrive')
        train_code = request.GET.get('train_code', None)
        if train_code is None:
            cache_key = '%s-%s-%s' %(date, start, arrive)
        else:
            cache_key = '%s-%s-%s-%s' %(date, start, arrive, train_code)
        cache_data = cache.get(cache_key)
        if cache_data:
            return json.loads(cache_data)
        else:
            trains = yupiao(date, start, arrive, train_code)
            #TODO read expired time from 12306
            if len(trains) > 0:
                cache.set(cache_key, json.dumps(trains), 30 * 60)
            return trains
