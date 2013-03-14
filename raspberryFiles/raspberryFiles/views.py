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
from os.path import splitext, exists, isdir, isfile, getmtime

from settings import MEDIA_ROOT
import time
import userSettings

def home(request):
	return render_to_response('home/home.html', locals(), context_instance=RequestContext(request))

def files(request):
	isSubdirectory = False
	validDirectory = True
	
	currentDir = userSettings.shareDir
	entries = listdir(currentDir)
	entriesList = makeFilesAndFolders(entries, currentDir, isSubdirectory)

	return render_to_response('files/files.html', locals(), context_instance=RequestContext(request))



def files_subdirectory(request, directory):
	isSubdirectory = True
	validDirectory = False
	directory = str(directory)
	
	if not directory.endswith('/'):
		directory += '/'
	
	
	currentDir = userSettings.shareDir
	
	if exists(userSettings.shareDir + directory):    
		currentDir = userSettings.shareDir + directory
		currentURL = directory
		validDirectory = True
	

	entries = listdir(currentDir)
	entriesList = makeFilesAndFolders(entries, currentDir, isSubdirectory)
	

	return render_to_response('files/files.html', locals(), context_instance=RequestContext(request))   





def makeFilesAndFolders(entries, currentDir, isSubdirectory):
	entries = entries
	entriesList = []  # entry, entryName, entryType, isFolder, timeModified
	for entry in entries:
		if isfile(currentDir + entry):
			entriesList.append([entry, splitext(entry)[0],splitext(entry)[1], False, time.strftime("%Y-%m-%d : %H:%M:%S", time.gmtime(getmtime(currentDir + entry)))])
		
		elif isdir(currentDir + entry):
			entriesList.append([entry, entry, 'Folder', True, ' '])
		
	return entriesList


def settings(request):

	return render_to_response('settings/settings.html', locals(), context_instance=RequestContext(request))

def test(request, path):
	isSubdirectory = True
	validDirectory = False
	path = str(path)
	
	currentDir = userSettings.shareDir
	
	if exists(userSettings.shareDir + path):    
		currentDir = userSettings.shareDir + path



	return render_to_response('test.html', locals(), context_instance=RequestContext(request))   



def test_root(request):

	return render_to_response('test.html', locals(), context_instance=RequestContext(request))
