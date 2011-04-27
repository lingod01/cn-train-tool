from django.template import RequestContext
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponseForbidden,HttpResponse,HttpResponseBadRequest
from django.conf import settings

def index(request):
    return render_to_response('ui/index.html',
        {
        },
        context_instance = RequestContext(request)
    )

