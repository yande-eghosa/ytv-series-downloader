from kivy.uix.screenmanager import Screen
from kivy.clock import Clock
import ytvApi as ytv
from kivy.lang import Builder
from threading import Thread

Builder.load_string('''
<BaseScreen>:
	name:'base_screen'
	MDBoxLayout:
		orientation:'vertical'
		
		Toolbar:
			title:'[b][i]YTV'
			anchor_title:'center'
		Sm:		

''')

class BaseScreen(Screen):
	doneOptimize=False
	
	def on_enter(self,*a):
		Clock.schedule_once(self.optimize_storage)	
	
	def optimize_storage(self,*a):
		def optimize_storage(self):
			ytv.optimize_storage()
			self.doneOptimize=True
		if not self.doneOptimize:
			Thread(target=optimize_storage,args=(self,),daemon=True).start()	
	

