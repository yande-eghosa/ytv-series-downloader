import cfg
from kivy.uix.screenmanager import Screen
from kivymd.uix.bottomsheet import * 
from kivy.clock import Clock
from kivy.properties import * 
from threading import Thread
import ytvApi as ytv

from kivy.lang import Builder

Builder.load_string('''

<HistoryScreen>:
	name:'historyscreen'
	MDGridLayout:
		cols:1
		spacing:dp(10)
		MDBoxLayout:
			size_hint:1,None
			MDIconButton:
				icon:"arrow-left-bold"
				on_release:app.on_key(1,27,(26))
			MDLabel:
				size_hint:1,None
				halign:'center'
				markup:True
				font_name:'fonts/title'
				text:'[b]'+'History'
			MDTextButton:
				size_hint:1,None
				halign:'center'
				markup:True
				#font_name:'fonts/title'
				text:'[i][u]'+'Clear?'
				on_release:root.confirm_delete()
				
		RecycleView:
			id: hist_rv
			size_hint_y:
			key_viewclass: 'viewclass'
			key_size: 'height'	
			RecycleGridLayout:
				id: hist_rb
				default_size: None, dp(100)
				default_size_hint: 1, None
				size_hint_y: None
				height: self.minimum_height
				cols:1
				spacing:dp(10)

''')

class HistoryScreen(Screen):
	def on_enter(self,*a):
		def sync(self):
			H=ytv.History()
			h=H.get()
			data=[]
			for no,item in enumerate(h,1):
				data.append({ 'viewclass':'HistoryBut','text':item[0] ,'secondary_text':'Downloaded with '+item[1],'tertiary_text':str(item[2]),'no':no})
			if len(data)==0:
				data=[{ 'viewclass':'YLabel','text':'History is Empty','halign':'center' }]		
			self.ids.hist_rv.data=data
		Thread(target=sync,args=(self,),daemon=True).start()
	def confirm_delete(self,*a):
		self.genre_menu = MDListBottomSheet()
		self.genre_menu.add_item('Cancel',lambda *zz:self.genre_menu.dismiss(),icon='cancel')
		self.genre_menu.add_item(f'Clear History?',lambda *a:self.delete(),icon='delete')
		self.genre_menu.open()
			
	def delete(self,*a):
		bk=ytv.History().delete()
		self.on_enter()
		from kivymd.toast import toast
		toast(f'History Cleared')
