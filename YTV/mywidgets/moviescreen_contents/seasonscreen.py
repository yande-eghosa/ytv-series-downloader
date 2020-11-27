import cfg
from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.properties import *
from kivy.metrics import dp
import ytvApi as ytv

from threading import Thread

Builder.load_string('''

<SeasonScreen>:
	name:'season_screen'
	MDBoxLayout:
		orientation:'vertical'			
		RecycleView:
			id: season_rv
			size_hint_y:None
			key_viewclass: 'viewclass'
			key_size: 'height'
			bar_width:dp(8)
			bar_inactive_color:.7,.7,.7,.4		
			RecycleBoxLayout:
				id: season_rb
				default_size: None, dp(50)
				default_size_hint: None, None
				size_hint_x: None
				width: self.minimum_width
				orientation: 'horizontal'
				spacing:dp(2)
		RecycleView:
			id: others_rv
			size_hint_y:
			key_viewclass: 'viewclass'
			key_size: 'height'	
			RecycleBoxLayout:
				id: others_rb
				default_size: None, None
				default_size_hint: 1, None
				size_hint_y: None
				height: self.minimum_height
				orientation: 'vertical'
				spacing:dp(2)


''')

class SeasonScreen(Screen):
	seasons=ObjectProperty([])
	episodes=ObjectProperty({})
	count=0
	
	def kill(self,*a):
		self.episodes={}
		self.seasons=''
		self.ids.season_rv.scroll_x=0
	
	def on_seasons(self,*a):
		
		cfg.SM2=self.manager
		self.ids.others_rv.data=[{'viewclass':'YLabel','text':f'Select a Season Above to View its Episodes','halign':'center','markup':True}]
		if self.seasons:
			data=[]
			for no,i in enumerate(self.seasons,0):
				data.append({'viewclass':'PageButton','text':f'{i.text}','group':'season','size_hint':[None,1],'width':dp(100),'season_number':no,'switch_page':self.switch_page,'season_check':no})
				
			self.ids.season_rv.data=data
		elif self.seasons !='':
			self.ids.season_rv.data=[{'viewclass':'YLabel','text':f'Loading failed','size_hint_x':None}]
		
	
	def switch_page(self,no,text):
		self.ids.others_rv.scroll_y=1
		self.count+=1
		url=self.seasons[no].attrs['href']
		def get_episodes(self,urlz,no,count,text):
			self.ids.others_rv.data=[{'viewclass':'YLabel','text':f'Loading {text}...','halign':'center','markup':True}]
			if e:=self.episodes.get(no):
				self.ids.others_rv.data=e
				return
			e=ytv.get_episodes(urlz)
			if e and False not in e:
				data=[]
				for atag in e:
					data.append({'viewclass':'EpisodeButton','season_no':no,'stext':text,'atag': atag,'ripple_scale': 0.0})
				self.episodes[no]=data
				if count==self.count:
					self.ids.others_rv.data=data
			else:
				self.ids.others_rv.data=[{'viewclass':'YLabel','text':f'Failed to Load {text}[u][i][b] \n[ref=retry]Try Again?[/ref] [/u][/i][/b] ','halign':'center','markup':True,'on_ref_press': lambda *a:self.switch_page(no)}]
		
		Thread(target=get_episodes,args=(self,url,no,self.count,text,),daemon=True).start()
