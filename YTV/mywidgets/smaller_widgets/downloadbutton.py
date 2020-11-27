import cfg
from kivymd.uix.list import *
from kivy.properties import *
from kivymd.uix.button import *
from kivy.lang import Builder
import ytvApi as ytv

Builder.load_string('''
''')

class DownloadButton(MDRectangleFlatButton):
	items=ObjectProperty()
	def on_release(self,*a):
		name,pname,video,activity,intent,Uri=self.items
		ytv.History().set(f'{str(cfg.history_entry[0])} { str(cfg.history_entry[1]) }',name)
		intent.setData(Uri.parse(video.url))
		intent.setPackage(pname)
		activity.startActivity(intent)
