import os, dill
#import kivy
from jnius import autoclass

activity = autoclass('org.kivy.android.PythonActivity').mActivity
Context = autoclass('android.content.Context')
Uri = autoclass('android.net.Uri')
Environment=ee=autoclass('android.os.Environment')

VERSION=autoclass('android.os.Build$VERSION')
VERSION_CODES=autoclass('android.os.Build$VERSION_CODES')
#PackageManager=autoclass('android.content.pm.PackageManager')

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

def has_storage_permission():
	return False

if __name__ == '__main__':
    print(has_storage_permission())