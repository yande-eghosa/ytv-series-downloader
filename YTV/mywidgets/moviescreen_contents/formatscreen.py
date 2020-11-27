import cfg
from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.properties import *
import ytvApi as ytv

from threading import Thread

Builder.load_string('''

<FormatScreen>:
	name:'format_screen'
	MDBoxLayout:
		# size_hint:1,None
		orientation:'vertical'
		MDBoxLayout:
			size_hint:1,None
			MDIconButton:
				icon:"close"
				on_release:
					exec("root.manager.current='season_screen'")
			MDLabel:
				size_hint:1,None
				halign:'center'
				text:'Select Video Format'+root.season_episode	
		RecycleView:
			id: format_rv
			size_hint_y:
			key_viewclass: 'viewclass'
			key_size: 'height'	
			RecycleBoxLayout:
				id: format_rb
				default_size: None, None
				default_size_hint: 1, None
				size_hint_y: None
				height: self.minimum_height
				orientation: 'vertical'
				spacing:dp(2)

''')

class FormatScreen(Screen):
	dlinks_url=ObjectProperty('')
	dlinks=ObjectProperty()
	season_episode=ObjectProperty('')
	count=0
	def on_dlinks_url(self,*a):
		if self.dlinks_url:
			cfg.SM2.current=self.name

	def on_enter(self,*a):
		cfg.history_entry.append(self.season_episode)
		if not cfg.doCaptcha:
			self.ids.format_rv.data=[{'viewclass':'YLabel','text':f'Loading Video Formats...','halign':'center','markup':True}]
			if self.dlinks_url:
				def get_download_links(self,url,count):
					if links:=ytv.get_download_link(url):
						if count==self.count:
							self.dlinks=links
					else:
						self.ids.format_rv.data=[{'viewclass':'YLabel','text':f'Failed to Load Episode[u][i][b] \n[ref=retry]Try Again?[/ref] [/u][/i][/b] ','halign':'center','markup':True,'on_ref_press': lambda *a:self.on_enter()}]
				Thread(target=get_download_links, args=(self,self.dlinks_url,self.count,),daemon=True).start()

	def on_dlinks(self,*a):
		def update_links(self):
			if d:=self.dlinks:
				data=[]
				for atag in d:
					text=f'{atag.text.upper().split("IN")[-1]}'
					data.append({'viewclass':'OneLineListItem','text':text,'on_release':lambda *x,y=atag,z=text:(self.goToCaptcha(y,z),cfg.history_entry.append(text))})
					
				self.ids.format_rv.data=data
		Thread(target=update_links,args=(self,),daemon=True).start()
	
	def on_leave(self,*a):
		
		if not cfg.doCaptcha:
			self.count+=1
			self.ids.format_rv.data=[{'viewclass':'YLabel','text':f'Loading','halign':'center','markup':True}]
			self.dlinks_url=''
			self.season_episode=''
			name=cfg.history_entry[:-1]
			cfg.history_entry=name
	
	def goToCaptcha(self,atag,z):
		cfg.SM.get_screen('captchascreen').url=atag.attrs.get('href')
		cfg.SM.get_screen('captchascreen').season_episode=f'{self.season_episode} {z}'
