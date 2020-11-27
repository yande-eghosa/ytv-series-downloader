import cfg
from kivymd.uix.bottomnavigation import *
from kivymd.uix.bottomsheet import * 
from kivy.uix.screenmanager import Screen 
from kivy.clock import Clock
from kivy.properties import * 
from threading import Thread
import ytvApi as ytv
from kivy.lang import Builder

Builder.load_string('''

<HomeTab>:
	name:'s2'
	text:'Home'
	icon:'home'
	orientation:'vertical'
	

	MDBoxLayout:
		size_hint_y:
		orientation:'vertical'
		MDBoxLayout:
			size_hint_y:None
			PageButton:
				id:latest_button
				group:'explore_options'
				state:'down'
				allow_no_selection: False
				text: 'Recent Updates'
				size_hint:1,None
				on_release:
					root.ids.sm_for_explore.current='latest'
					root.refresh_latest()
			PageButton:
				id:s1_button
				group:'explore_options'
				state:'normal'
				allow_no_selection: False
				text: 'Search'
				size_hint:1,None
				on_release: root.ids.sm_for_explore.current='s1'
			PageButton:
				group:'explore_options'
				state:'normal'
				allow_no_selection: False
				size_hint:1,None
				text:'Explore'
				on_release: root.ids.sm_for_explore.current='explore_genre'

		ScreenManager:
			id:sm_for_explore
			transition:
			Screen:
				name:'latest'
	
				RecycleView:
					id: latest_rv
					size_hint_y:
					key_viewclass: 'viewclass'
					key_size: 'height'
					bar_width:dp(5)
					bar_inactive_color:.7,.7,.7,.4	
					RecycleBoxLayout:
						id: latest_rb
						default_size: None,None
						default_size_hint: 1, None
						size_hint_y: None
						height: self.minimum_height
						orientation: 'vertical'
						# cols:1
						spacing:dp(5)
			Screen:
				name:'s1'
				text:'Search'
				icon:'search-web'
				cols:1
				padding:dp(5)

				MDBoxLayout:
					orientation:'vertical'
					
					MDBoxLayout:
						#cols:3
						padding:dp(10)
						adaptive_height:True
					
						MYTextField:
							id:text_field
							text:''
							hint_text:'Search TV series by name'
							current_hint_text_color:1,1,1,1
							on_text_validate:root.th_search()
						LoadImg:
							size_hint_x:None
							start_anim:True
							MDIconButton:
								id:search_but
								icon:'search-web'
								on_release: root.th_search()
					RecycleView:
						id: search_rv
						key_viewclass: 'viewclass'
						key_size: 'height'	
						RecycleGridLayout:
							id: search_rb
							default_size: None,dp(200)
							default_size_hint: 1, None
							size_hint_y: None
							height: self.minimum_height
							cols:1
							spacing:dp(5)
			Screen:
				name:'explore_genre'
				BoxLayout:	
					orientation:'vertical'	
					MDFlatButton:
						size_hint:1,None
						markup:True
						text:'Select Genres:'+ root.genre
						on_release: 
							root.show_genres()			
					RecycleView:
						id: explore_rv
						size_hint_y:
						key_viewclass: 'viewclass'
						key_size: 'height'
						bar_width:dp(5)
						bar_inactive_color:.7,.7,.7,.4	
						RecycleGridLayout:
							id: explore_rb
							default_size: None,dp(200)
							default_size_hint: 1, None
							size_hint_y: None
							height: self.minimum_height
							cols:1
							spacing:dp(5)
					RecycleView:
						id: pages_rv
						size_hint_y:None
						key_viewclass: 'viewclass'
						key_size: 'height'
						bar_width:dp(7)
						bar_inactive_color:.7,.7,.7,.4
						
						RecycleBoxLayout:
							id: pages_rb
							default_size: None, dp(40)
							default_size_hint: None, None
							size_hint: None,None
							width: self.minimum_width
							orientation: 
							spacing:dp(2)

''')

class HomeTab(MDBottomNavigationItem):#MDBoxLayout, MDTabsBase):
	isSearching= BooleanProperty(False)
	searchThreadCount=NumericProperty(1)
	movie_list_=False

	genre_list=ObjectProperty(None)
	current_page=NumericProperty(1)
	genre=StringProperty(' [u][i][b]Click Here[/b][/i][/u]')
	genre_menu =ObjectProperty(None)
	page_buttons=ListProperty([])
	isPageGenre=BooleanProperty(False)
	list_of_latest_movies=ObjectProperty(None)
	genre_cache= ObjectProperty(False)
	control_size_hint=ObjectProperty([None])
	
	def __init__(self,**kw):
		super(HomeTab,self).__init__(**kw)
		self.network='Syncing Updates'
		self.clk=Clock.schedule_interval(self.init,2)
		self.clk1=Clock.schedule_interval(self.get_genres,1)
		self.clk2=Clock.schedule_interval(self.refresh_latest,1)		
	def init (self,*a):
		self.clk.cancel()
		self.ids.search_rv.data=[{'viewclass':'MDIconButton','icon':'cloud-search'}]
	
	def refresh_bookmarks(self,*a):
		pass	

	def search_from_latest(self,text):
		self.searchThreadCount+=1
		self.isSearching=False
		while '\n' in text:
			text=text.replace('\n','')
		self.ids.text_field.text=text
		self.th_search()
	def th_search(self,*a):
		if not self.isSearching:
			Thread(target=self.search4,args=(self,),daemon=True).start()
		else:
			from kivymd.toast import toast
			toast('Please Wait\nCurrently searching')

	def search4(self,*a):
		self.isSearching=True
		self.ids.search_rv.scroll_y=1
		def cancel(*a):
			self.searchThreadCount+=1
			self.isSearching=False
			self.init()#self.ids.search_rv.data=[]

		self.ids.search_rv.data=[{'viewclass':'YLabel','text':'Searching\n\n[ref=retry][u][i][b]Cancel[/ref][/u][/i][/b] ','halign':'center','markup':True,'on_ref_press':cancel,'size_hint_y':None}]#{'viewclass':'MDRectangleFlatIconButton','text':'Cancel','icon':'cancel','on_release':cancel,'line_color':(0,0,0,0)}]
		
		def search(self,a,_count):
			count=_count
			result,self.movie_list_=ytv.search4(a,self.movie_list_)
			if result:
				data=[]
				for number,atag in enumerate(result,1):
					data.append({'viewclass':'ResultCard','checkId': number,'atag':atag})
				if self.searchThreadCount==count:
					self.ids.search_rv.data=data
					self.isSearching=False
				else:
					#print(f'SearchThread{count} destroyed')
					return
			elif self.searchThreadCount==count:
				self.ids.search_rv.data=[]
				self.ids.search_rv.data=[{'viewclass':'YLabel','text':'No Result Found','halign':'center','markup':True,'on_ref_press':'cancel','size_hint_y':None}]
				self.isSearching=False
			else:
				#print(f'SearchThread{count} destroyed')
				return
				
		th=Thread(target=search,args=(self,self.ids.text_field.text,self.searchThreadCount),daemon=True)
		th.start()
		
	def refresh_latest(self,*a):
		self.ids.latest_rv.data=[{'viewclass':'YLabel','text':self.network,'halign':'center','markup':True,'on_ref_press':self.refresh_latest}, {'viewclass':'MDIconButton','icon':'autorenew','on_pres':self.refresh_latest}]
		if self.list_of_latest_movies:
			self.ids.latest_rv.scroll_y=1
			# self.ids.explore_rb.cols=1
			# self.control_size_hint=[None]
			self.ids.latest_rv.data=self.list_of_latest_movies
			return
		#self.ids.latest_rv.data=[]
		
		self.clk2.cancel()
		def refresh(self):
			recent=ytv.latest()
			# self.control_size_hint=[None]
			# self.ids.explore_rb.cols=1
		
			if recent:
				data=[]
				for datum in recent:
					data.append({'viewclass':'LatestButton','aparent':self,'text':f'{datum[0]}','secondary_text':f'{datum[1]}','tertiary_text':f'{datum[2]}','size_hint_yx':None,'ripple_scale':0.0})
				self.ids.latest_rv.data=self.list_of_latest_movies=data
				
			else:
				self.network='No Internet Connection'
				self.clk2()
				#self.ids.latest_rv.data=[{'viewclass':'YLabel','text':f'Failed to Retrieve Results\n[ref=retry]Retry...[/ref]','halign':'center','markup':True,'on_ref_press':self.refresh_latest}]
	
		Thread(target=refresh,args=(self,),daemon=True).start()
	
	def get_genres(self,*a):
		self.ids.explore_rv.data=[{'viewclass':'YLabel','text':'No Genre Selected','halign':'center'}]
		self.clk1.cancel()
		def _get_genres(self):
			r=ytv.get_genres()
			if r:
				self.genre_list=r
			else:
				self.clk1()
			
		Thread(target=_get_genres,args=(self,),daemon=True).start()
	
	def load_genre(self,list_item,dict_of_atags):
		# self.isPageGenre=True
		self.ids.explore_rv.data=[{'viewclass':'YLabel','text':'Searching','halign':'center','markup':True,'size_hint_y':None}]
		self.ids.pages_rv.data=[]
		self.ids.pages_rv.scroll_x=0
		atags=dict_of_atags.get(list_item.text)
		def _load_genre(self,atags,list_item):
			global page_check
			self.current_page=page_check=cfg.page_check= 1
			g=ytv.Genre(atags)
			r=g.get_movies()
			if r:
				self._data=[]
				sub_data=[]
				pages_data=[]
				for number,atag in enumerate(r,1):
					sub_data.append({'viewclass':'ResultCard','checkId': number,'atag':atag})					
					if not number%20:
						self._data.append(sub_data)
						pages_data.append({'viewclass':'PageButton','text': f'{number//20}','page_check': number//20,'group':'page_button', 'size_hint':[None,None] ,'switch_page':self.switch_page})
						sub_data=[]
				if len(sub_data)!=0:
					self._data.append(sub_data)
					pages_data.append({'viewclass':'PageButton','text': f'{(number//20)+1}','page_check':(number//20)+1,'group':'page_button', 'size_hint':[None,None] ,'switch_page':self.switch_page})
					

				self.ids.explore_rv.scroll_y=1
				
				self.ids.explore_rv.data=self._data[0]
				self.ids.pages_rv.data=pages_data
				
				
				self.genre= f' [u][i][b]{list_item.text}[/b][/i][/u]'
					
			else:
				self.ids.explore_rv.data=[{'viewclass':'YLabel','text':f'No Result Found\nCheck Internet Connection\n [u][i][b] \n[ref=retry]Try Again?[/ref] [/u][/i][/b] ','halign':'center','markup':True,'on_ref_press':self.show_genres}]
			return
				
		Thread(target=_load_genre,args=(self,atags,list_item,),daemon=True).start()
		
	def on_page_buttons(self,*a):
		self.ids.pages_rv.scroll_y=1
		self.ids.pages_rb.clear_widgets()
		if self.page_buttons:
			for but in self.page_buttons:
				self.ids.pages_rb.add_widget(but)
		else:
			pass
	
	def switch_page(self,no):
		
		if self.current_page!=no:
			self.ids.explore_rv.scroll_y=1
			self.ids.explore_rv.data=self._data[int(no)-1]
			self.current_page=no

	def show_genres(self,*a):
		if not self.genre_list:
			self.genre_menu = MDListBottomSheet()
			self.genre_menu.add_item("No Internet Connection\nTry Again?",lambda *a :self.show_genres())	
		else:
			self.genre_menu = MDListBottomSheet()
			dict_of_atags={}
			for no,i in enumerate(self.genre_list,1):
				dict_of_atags[f'{i.text}']=i
				self.genre_menu.add_item(f"{i.text}",lambda list_item:self.load_genre(list_item,dict_of_atags))	
		self.genre_menu.open()
	def switch_screen(self,*a):
		pass#deprecated function
