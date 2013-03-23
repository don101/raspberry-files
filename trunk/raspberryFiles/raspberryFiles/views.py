from django import forms, http
from django.core.files import File
from django.core.urlresolvers import reverse
from django.contrib import auth
from django.http import HttpResponse, Http404, HttpResponseRedirect, HttpResponseRedirect, HttpRequest
from django.shortcuts import render_to_response, render_to_response, redirect
from django.template import Context, RequestContext
from django.template.loader import get_template
from django.contrib.auth.decorators import login_required
from forms import DocumentForm
from models import Document
from os import listdir, remove, chdir, makedirs
from os.path import splitext, exists, isdir, isfile, getmtime, dirname, basename, getsize
from shutil import rmtree
from urlparse import urlsplit
from settings import MEDIA_ROOT

import time
import userSettings
import urllib
import urllib2
import shutil
import threading

from raspberryFiles import userSettings
from django.contrib.auth.models import User


@login_required(login_url='/login/')
def files(request):
	isSubdirectory = False
	validDirectory = True
	buttonsEnabled = False
	
	user = request.user
	username = user.username
	
	currentDir = userSettings.shareDir
	entries = listdir(currentDir)
	entriesList = makeFilesAndFolders(entries, currentDir, isSubdirectory)

	return render_to_response('files/files.html', locals(), context_instance=RequestContext(request))


@login_required(login_url='/login/')
def files_subdirectory(request, path):
	isSubdirectory = True
	validDirectory = False
	buttonsEnabled = True
	path = str(path)
	
	user = request.user
	username = user.username
	
	if not path.endswith('/'):
		path += '/'
	
	
	currentDir = userSettings.shareDir
	
	if exists(userSettings.shareDir + path):    
		currentDir = userSettings.shareDir + path
		currentURL = path
		validDirectory = True
	

	entries = listdir(currentDir)
	entriesList = makeFilesAndFolders(entries, currentDir, isSubdirectory)
	

	return render_to_response('files/files.html', locals(), context_instance=RequestContext(request))   


@login_required(login_url='/login/')
def deleteFile(request, path):
	
	try:
		if exists(userSettings.shareDir + path):
	
				if isdir(userSettings.shareDir + path):
					rmtree(userSettings.shareDir + path)
				else:
					remove(userSettings.shareDir + path)
	
	
		return redirect('/files/' + dirname(path)+ '/')
	except:
		return render_to_response('files/delete/permission_error.html', locals(), context_instance=RequestContext(request))




def makeFilesAndFolders(entries, currentDir, isSubdirectory):
	entries = entries
	entriesList = []  # entry, entryName, entryType, isFolder, entrySize, Size timeModified
	for entry in entries:
		if isfile(currentDir + entry):
			entriesList.append([entry,\
							 splitext(entry)[0],\
							 getFileType(entry),\
							 False, sizeof_fmt(getsize(currentDir + entry)),\
							 time.strftime("%Y-%m-%d : %H:%M:%S",\
							 time.gmtime(getmtime(currentDir + entry)))])
		
		elif isdir(currentDir + entry):
			entriesList.append([entry, entry, 'Folder', True, ' '])
		
	return entriesList

@login_required(login_url='/login/')
def download(request):
		
	if 'downloadURL' in request.POST:
		ensure_dir(userSettings.shareDir + userSettings.downloadDir)
		t = threading.Thread(target = downloadActivity, args = (request,))
		t.daemon = True
		t.start()
		return redirect('/files/'+ userSettings.downloadDir)
	
	else:
		return render_to_response('files/download/no_URL_error.html', locals(), context_instance=RequestContext(request))

@login_required(login_url='/login/')
def downloadActivity(request):
	
		if(request.POST['downloadURL']):
			response = urllib2.urlopen(request.POST['downloadURL'])
			file = response.read()
			
			filename = request.POST['downloadURL'].split('/')[-1] # basename(request.POST['downloadURL']
			
			f = open(userSettings.shareDir + userSettings.downloadDir + filename, 'wb')
		
			f.write(file)
			
			f.close()
		else: 
			return render_to_response('files/dowload/no_URL_entered.html', locals(), context_instance=RequestContext(request))

@login_required(login_url='/login/')
def upload(request):
	try:
		if request.method == 'POST':
			
			fileUpload = request.FILES['fileUpload']
			
			ensure_dir(userSettings.shareDir + userSettings.uploadDir)
			with open(userSettings.shareDir + userSettings.uploadDir + fileUpload.name, 'wb') as destination:
		
				for chunk in fileUpload.chunks():
					
					destination.write(chunk)
			
			return redirect('/files/'+ userSettings.uploadDir)
	except:
			return render_to_response('files/upload/no_file_attached.html', locals(), context_instance=RequestContext(request))




@login_required(login_url='/login/')
def settings(request):

	user = request.user
	username = user.username
	
	return render_to_response('settings/settings.html', locals(), context_instance=RequestContext(request))


def sizeof_fmt(num):
	for x in [' Bytes','KB','MB','GB']:
		if num < 1024.0:
			return "%3.1f%s" % (num, x)
		num /= 1024.0
	return "%3.1f%s" % (num, 'TB')

def getFileType(entry):
	if len(splitext(entry)[1]) > 0:
		return splitext(entry)[1].split('.')[1]
	
	else:
		return ''
	
def ensure_dir(f):
	d = dirname(f)
	if not exists(d):
		makedirs(d)
