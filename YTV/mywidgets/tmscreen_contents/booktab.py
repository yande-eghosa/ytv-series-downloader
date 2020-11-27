import cfg
from kivymd.uix.bottomnavigation import *
from kivymd.uix.bottomsheet import * 
from kivy.clock import Clock
from kivy.properties import * 
from threading import Thread
import ytvApi as ytv
from kivy.lang import Builder

Builder.load_string('''

<BookTab>:
	name:'s3'
	icon:'star'
	text:'BookMarks'
	
	MDBoxLayout:
		orientation:'vertical'
		MDBoxLayout:
			adaptive_height:True
			MDRectangleFlatButton:
				size_hint_y:None
				md_bg_color:0,0,0,1
				icon:'trash-can'
				text:'Clear Bookmarks'
				on_release:root.confirm_delete()
			MDRectangleFlatButton:
				size_hint_y:None
				md_bg_color:0,0,0,1
				#icon:'trash-can'
				text:'History'
				on_release:root.open_history()
		RecycleView:
			id: book_rv
			size_hint_y:
			key_viewclass: 'viewclass'
			key_size: 'height'	
			RecycleGridLayout:
				id: book_rb
				default_size: None, dp(200)
				default_size_hint: 1, None
				size_hint_y: None
				height: self.minimum_height
				cols:3
				spacing:dp(2)

''')


class BookTab(MDBottomNavigationItem):#FloatLayout, MDTabsBase):
	datum=ObjectProperty([])
	bug=ObjectProperty(False)
	def __init__(self,**kw):
		super(BookTab,self).__init__(**kw)
		global BOOKTAB
		BOOKTAB=cfg.BOOKTAB=self	
		self.clk1=Clock.schedule_interval(self.sync,1)
		
	def open_history(self,*a):
		cfg.SM.current='historyscreen'

	def confirm_delete(self,*a):
		if True:
			self.genre_menu = MDListBottomSheet()
			self.genre_menu.add_item('Cancel',lambda *zz:self.genre_menu.dismiss(),icon='cancel')
			self.genre_menu.add_item('Clear All BookMarks?',lambda *a:self.delete(),icon='delete')
			self.genre_menu.open()
			
		
	
	def delete(self,*a):
		bk=ytv.BookMarks()
		from kivymd.toast import toast
		try:
			b_seasons={}
		except:
			pass
		bk.clear_bk()
		self.bug=True
		self.sync()
		
		toast(f'Bookmarks Cleared')
		
	def on_enter(self,*a):
		self.ids.book_rv.data=self.datum
		self.bug=False
		
	def sync(self,*a):
		self.clk1.cancel()
		def sync(self):
			s=ytv.BookMarks()
			bk=s.get_bk()
			data=[]
			for name in bk.keys():
				data.append({ 'viewclass':'BookCard','name':name })
			if len(data)==0:
				data=[{ 'viewclass':'YLabel','text':'No Bookmarks','halign':'center' }]
			self.datum=data
			if self.bug:
				self.on_enter()
		Thread(target=sync,args=(self,),daemon=True).start()