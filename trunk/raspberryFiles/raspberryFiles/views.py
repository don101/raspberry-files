
from django.http import HttpResponse, Http404, HttpResponseRedirect 
from django.template.loader import get_template
from django.template import Context, RequestContext
from django.shortcuts import render_to_response

import userSettings

from os import listdir


def home(request):

    return render_to_response('home/home.html',locals(), context_instance=RequestContext(request))

def files(request):


    files = listdir(userSettings.shareDir)

    return render_to_response('files/files.html',locals(), context_instance=RequestContext(request))

