import datetime
from piston.handler import BaseHandler
from piston.utils import rc
from train.provider._12306 import yupiao

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
        trains = yupiao(date, start, arrive, train_code)
        return trains
