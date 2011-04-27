from django.template import RequestContext
from django.shortcuts import render_to_response
#from django.core.urlresolvers import reverse
#from django.http import HttpResponseRedirect, HttpResponseForbidden,HttpResponse,HttpResponseBadRequest
#from django.conf import settings
from train.provider._12306 import yupiao,FIELDS

def index(request):
    date = request.GET.get('date', None)
    start = request.GET.get('start', None)
    arrive = request.GET.get('arrive', None)
    train_code = request.GET.get('train_code', None)
    if date and start and arrive:
        data = yupiao(date, start, arrive, train_code)
        fields = [item[1] for item in FIELDS]
        trains = []
        for train in data:
            trains.append([train[key].strip() for key,value in FIELDS])
        context = {'fields' : fields, 'trains' : trains}
        return render_to_response('mobile/yupiao.html', 
            context,
            context_instance = RequestContext(request)
        )
    else:
        return render_to_response('mobile/index.html',
            {
            },
            context_instance = RequestContext(request)
        )
 


