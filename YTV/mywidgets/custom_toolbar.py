from kivymd.uix.toolbar import MDToolbar
from kivy.clock import Clock

class Toolbar(MDToolbar):
	def __init__(self,**kw):
		super(Toolbar,self).__init__(**kw)
		Clock.schedule_once(self.ui)
	def ui(self,*a):
		self.ids.label_title.markup=True
		self.ids.label_title.font_name='fonts/title'