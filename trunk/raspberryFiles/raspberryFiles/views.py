from django import forms, http
from django.core.files import File
from django.core.urlresolvers import reverse
from django.http import HttpResponse, Http404, HttpResponseRedirect, HttpResponseRedirect
from django.shortcuts import render_to_response, render_to_response
from django.template import Context, RequestContext
from django.template.loader import get_template
from forms import DocumentForm
from models import Document
from os import listdir
from os.path import splitext, exists, isdir, isfile
from settings import MEDIA_ROOT

import userSettings

def home(request):
	return render_to_response('home/home.html', locals(), context_instance=RequestContext(request))

def files(request):
	isSubdirectory = False
	validDirectory = True
	
	currentDir = userSettings.shareDir
	entries = listdir(currentDir)
	entriesFiles, entriesFolders = makeFilesAndFolders(entries, currentDir, isSubdirectory)

	return render_to_response('files/files.html', locals(), context_instance=RequestContext(request))



def files_subdirectory(request, directory):
	isSubdirectory = True
	validDirectory = False
	
	currentDir = userSettings.shareDir
	
	if exists(userSettings.shareDir + directory):    
		currentDir = userSettings.shareDir + directory
		currentURL = directory + '/'
		validDirectory = True
	

	entries = listdir(currentDir)
	entriesFiles, entriesFolders = makeFilesAndFolders(entries, currentDir, isSubdirectory)
	

	return render_to_response('files/files.html', locals(), context_instance=RequestContext(request))   





def makeFilesAndFolders(entries, currentDir, isSubdirectory):

	entriesFiles = []  # filesPass index: 1 = name, 2 = ext
	entriesFolders = []
	

	for entry in entries:
		if isfile(currentDir + entry):
			entriesFiles.append([entry, splitext(entry)[0],splitext(entry)[1]])
		
		elif isdir(currentDir + entry):
			entriesFolders.append(entry)
		
	return entriesFiles, entriesFolders


def settings(request):

	return render_to_response('settings/settings.html', locals(), context_instance=RequestContext(request))

def test(request, directory):
	dir = directory
	
	return render_to_response('test.html', locals(), context_instance=RequestContext(request))

def test_root(request):

	return render_to_response('test.html', locals(), context_instance=RequestContext(request))
def list(request):
	# Handle file upload
	if request.method == 'POST':
		form = DocumentForm(request.POST, request.FILES)
		if form.is_valid():
			newdoc = Document(docfile=request.FILES['docfile'])
			newdoc.save()

			# Redirect to the document list after POST
			return HttpResponseRedirect(reverse('raspberryFiles.views.list'))
		else:
			form = DocumentForm()  # A empty, unbound form

	# Load documents for the list page
	documents = Document.objects.all()

	# Render list page with the documents and the form
	return render_to_response(
        'list/list.html',
        {'documents': documents, 'form': form},
        context_instance=RequestContext(request)
    )
# def upload_file(request):
#    files = listdir(userSettings.shareDir)
#    # Handle file upload
#    if request.method == 'POST':
#        form = UploadFileForm(request.POST, request.FILES)
#        if form.is_valid():
#            newdoc = Document(docfile = request.FILES['docfile'])
#            newdoc.save()
#
#            # Redirect to the document list after POST
#            return render_to_response('files/upload.html',locals(), context_instance=RequestContext(request))
#    else:
#        form = UploadFileForm() # A empty, unbound form
#
#    # Load documents for the list page
#    documents = Document.objects.all()
#
#    # Render list page with the documents and the form
#    return render_to_response('files/upload.html',locals(), context_instance=RequestContext(request)
#    )
