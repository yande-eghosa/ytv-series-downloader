import cfg
from kivy.uix.behaviors import ToggleButtonBehavior
from kivymd.uix.button import MDRectangleFlatButton
from kivy.properties import ObjectProperty,NumericProperty
from kivy.lang import Builder

Builder.load_string('''

<PageButton>:
	allow_no_selection:False
	
''')

class PageButton(ToggleButtonBehavior,MDRectangleFlatButton):
	switch_page=ObjectProperty()
	season_number=NumericProperty()
	season_check=NumericProperty()
	page_check=ObjectProperty()
	def __init__(self,**kw):
		super(PageButton,self).__init__(**kw)
		self.md_bg_color=[0,0,0,1]
		#self.opacity=.5
	def on_page_check(self,*a):
		self.state= 'down' if self.page_check== cfg.page_check else 'normal'
	def on_season_check(self,*a):
		self.state= 'down' if self.season_check== cfg.season_check else 'normal'
	def on_state(self,button,state):
		if state=='down':
			self.md_bg_color=[1,1,1,1]
			#self.opacity=1
		else:
			self.md_bg_color=[0,0,0,1]
			#self.opacity=.5
	def on_release(self,*a):
		if self.group=='page_button':
			cfg.page_check=int(self.text)
			self.switch_page(self.text)
		elif self.group=='season':
			cfg.season_check=self.season_number
			self.switch_page(self.season_number,self.text)
		
	def on_touch_up(self,*a):
		super(PageButton,self).on_touch_down(*a)
		super(PageButton,self).on_touch_up(*a)
		pass
	
	def on_touch_down(self,*a):
		pass
