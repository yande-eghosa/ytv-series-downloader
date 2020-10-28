import os, dill
#import kivy
from jnius import autoclass
Request=autoclass("android.app.DownloadManager$Request")
Query= autoclass("android.app.DownloadManager$Query")
DownloadManager=dm=autoclass("android.app.DownloadManager")
activity = autoclass('org.kivy.android.PythonActivity').mActivity
Context = autoclass('android.content.Context')
Uri = autoclass('android.net.Uri')
Environment=ee=autoclass('android.os.Environment')
VERSION=autoclass('android.os.Build$VERSION')
VERSION_CODES=autoclass('android.os.Build$VERSION_CODES')

def get_build_no():
	try:
		version=VERSION.SDK_INT
		ginger=VERSION_CODES.M#GINGERBREAD
		if version>= ginger:
			return True
		else:
			return False
	except:
		return False

def get_filename(url):
	from urllib.parse import unquote, urlparse
	from pathlib import PurePosixPath
	return PurePosixPath(unquote(urlparse(url).path)).parts[-1]

def queue_download(video):
	request = Request(Uri.parse(video.url))
	request.setDescription("YTVSeries")
	request.setTitle(f"{get_filename(video.url)}")
	request.setNotificationVisibility(Request.VISIBILITY_VISIBLE_NOTIFY_COMPLETED)
	request.setDestinationInExternalPublicDir(Environment.DIRECTORY_DOWNLOADS, os.path.join('YTVSeries',f"{get_filename(video.url)}"))	
	manager =  activity.getSystemService(Context.DOWNLOAD_SERVICE);
	try:
		manager.enqueue(request)
		return True
	except:
		return False
