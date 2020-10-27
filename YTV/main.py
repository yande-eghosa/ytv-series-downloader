SM=None
SM2=None
doCaptcha=None
season_check=None
page_check=1
BOOKTAB=None
b_seasons={}
b_movies_temp={}
app=None
history_entry=[]

from kivymd.app import MDApp
from kivymd.uix.button import *
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.tab import MDTabsBase, MDTabs
from kivymd.uix.label import MDLabel
from kivymd.uix.card import MDCard
from kivymd.uix.bottomsheet import * #MDListBottomSheet
from kivymd.uix.behaviors import * #RectangularRippleBehavior
from kivymd.uix.list import *
from kivymd.uix.bottomnavigation import *

from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import *
from kivy.uix.scatterlayout import ScatterLayout
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.behaviors import *#ButtonBehavior


from kivy.lang import Builder
from kivy.properties import *
from kivy.clock import Clock
from kivy.loader import Loader
from kivy.core.window import Window
from kivy.animation import Animation
from kivy.metrics import dp

from mytextfield import MDTextField as MYText
import ytvApi as ytv
from downloadmanager import dm

from threading import Thread

Builder.load_file('tools.kv')

class MYTextField(MYText):
	pass

class LoadImg(ScatterLayout):
	start_anim=BooleanProperty(False)
	def on_start_anim(self,*a):
		if self.start_anim:
			trans='in_out_quad'
			self.anim=Animation(opacity=.2,duration=1.5,t=trans)+Animation(opacity=1,duration=1.5,t=trans)
			self.anim.repeat=True
			self.anim.start(self)
		else:
			self.anim.cancel(self)
			self.opacity=1

class Sm(ScreenManager):
	def __init__(self,**kw):
		super(Sm,self).__init__(**kw)
		global SM
		SM=self
		
		
class MovieScreen(Screen):
	movie=ObjectProperty()
	title=StringProperty('Loading...')
	info=StringProperty('Loading...')
	
	def on_enter(self,*a):
		global doCaptcha
		if self.movie.info and not doCaptcha:
			bk=ytv.BookMarks()
			self.ids.add_bk.icon='star' if bk.is_bk(self.movie.name) else 'star-outline'
			self.ids.thumb.texture=self.movie.img_texture
			self.title=t=self.movie.name
			history_entry.append(t)
			self.info=self.movie.info
			#self.ids.sm.clear_widgets()
			Thread(target=self.get_seasons,daemon=True).start()
		elif doCaptcha==True:
			doCaptcha=False

	def bookmark(self,*a):
		bk=ytv.BookMarks()
		from kivymd.toast import toast
		if self.ids.add_bk.icon=='star':
			self.ids.add_bk.icon='star-outline'
			bk.del_bk(self.movie.name)
			BOOKTAB.sync()
			toast(f'Bookmark removed ')
		else :
			self.ids.add_bk.icon='star'
			self.movie.bookmark()
			b_seasons[self.movie.name]=self.movie
			BOOKTAB.sync()
			toast(f'Bookmark added')
	
	def get_seasons(self,*a):
		s=self.movie.get_seasons()
		self.ids.sm.get_screen('season_screen').seasons=s
		self.ids.sm.current='season_screen'

	def close_screen(self,*a):
		self.ids.sm.current='season_screen'
		#self.ids.sm.get_screen('season_screen').kill()
		self.manager.current='tmscreen'
	def on_pre_leave(self,*a):
		self.ids.info_scroll_view.scroll_y=1
	def on_leave(self,*a):
		global doCaptcha
		BOOKTAB.bug=True
		BOOKTAB.sync()
		if not doCaptcha:
			self.ids.ss.kill()
			self.ids.thumb.texture=None
			self.title='Loading'
			self.info='Loading'
			global history_entry
			history_entry=[]
			#self.ids.info_scroll_view.scroll_y=1
		

class SeasonScreen(Screen):
	seasons=ObjectProperty([])
	episodes=ObjectProperty({})
	count=0
	
	def kill(self,*a):
		self.episodes={}
		self.seasons=''
		self.ids.season_rv.scroll_x=0
	
	def on_seasons(self,*a):
		global SM2
		SM2=self.manager
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

class FormatScreen(Screen):
	dlinks_url=ObjectProperty('')
	dlinks=ObjectProperty()
	season_episode=ObjectProperty('')
	count=0
	def on_dlinks_url(self,*a):
		if self.dlinks_url:
			global SM2
			SM2.current=self.name

	def on_enter(self,*a):
		history_entry.append(self.season_episode)
		if not doCaptcha:
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
					data.append({'viewclass':'OneLineListItem','text':text,'on_release':lambda *x,y=atag,z=text:(self.goToCaptcha(y,z),history_entry.append(text))})
					
				self.ids.format_rv.data=data
		Thread(target=update_links,args=(self,),daemon=True).start()
	
	def on_leave(self,*a):
		
		if not doCaptcha:
			self.count+=1
			self.ids.format_rv.data=[{'viewclass':'YLabel','text':f'Loading','halign':'center','markup':True}]
			self.dlinks_url=''
			self.season_episode=''
			global history_entry
			name=history_entry[:-1]
			history_entry=name
	
	def goToCaptcha(self,atag,z):
		global SM		
		SM.get_screen('captchascreen').url=atag.attrs.get('href')
		SM.get_screen('captchascreen').season_episode=f'{self.season_episode} {z}'

class EpisodeButton(OneLineAvatarIconListItem):
	atag=ObjectProperty()
	season_no=ObjectProperty()
	stext=ObjectProperty()
	
	def on_atag(self,*a):
		if self.atag:
			self.text=f'{self.atag.text} {self.stext}'
	def open_download_options(self,*a):
		#print(self.atag.attrs.get('href'))
		if url:=self.atag.attrs.get('href'):
			SM2.get_screen('format_screen').dlinks_url=url
			SM2.get_screen('format_screen').season_episode=f' --{self.text}'

class CaptchaScreen(Screen):
	url=ObjectProperty()
	c_image_src=ObjectProperty()
	res=()
	count=0
	season_episode=ObjectProperty('')
	def on_url(self,*a):
		if self.url:
			#print(self.url)
			
			global doCaptcha
			doCaptcha=True
			self.manager.current=self.name
			self.get_captcha()
	def get_captcha(self,*a):
			self.ids.form.disabled=False
			self.ids.options_rv.data=[]
			im=Image(source='icons/loading.png')
			self.ids.c_image.texture=im.texture
			def get_captcha(self,count):
				try:
					
					self.captcha=ytv.Captcha(self.url)
					if self.captcha.get_image():
						file_name='caps/password.png'
					
					self.c_image_src=file_name
				except:
					self.c_image_src=False
				if count==self.count:
					Clock.schedule_once(self.update_captcha)
			Thread(target=get_captcha ,args=(self,self.count,),daemon=True).start()
	
	def update_captcha(self,*a):
		if src:=self.c_image_src :
			im=Image(source=src ,nocache=True)
			self.ids.c_image.texture=im.texture
		else:
			im=Image(source='icons/404.png')
			self.ids.c_image.texture=im.texture
			self.ids.options_rv.data=[{'viewclass':'MDLabel', 'text':f'''Network Error''','halign':'center'},{'viewclass':'MDRectangleFlatButton', 'text':f''' Retry ''','on_release':self.get_captcha}]
	
	def submit(self,*a):
		self.ids.form.disabled=True
		im=Image(source='icons/loading1.png',nocache=True)
		self.ids.c_image.texture=im.texture
		self.ids.options_rv.data=[{'viewclass':'MDLabel', 'text':f'''Retrieving Download Link''','halign':'center'}]
		
		def submit(self):
			video,size=v,size=self.captcha.submit(self.ids.c_text.text)
			if video.url== self.captcha.r.url:
				error=video.text
				self.ids.options_rv.data=[{'viewclass':'MDLabel', 'text':f'''{error}''','halign':'center'},{'viewclass':'MDRectangleFlatButton', 'text':f''' Try Again ''','on_release':self.get_captcha}]
				return
			else:
				pass
			apps,activity,intent,Uri=self.captcha.get_browsers()
			data=[]
			if size:
				data.append({'viewclass':'MDLabel', 'text':f'''{size} mb'''})
			if dm.get_build_no():
				data.append({'viewclass':'MDRectangleFlatButton', 'text':f'''Download with Download Manager''','on_release':lambda *z:self.start_download(video)})
			for app in apps.keys():
				data.append({'viewclass':'DownloadButton', 'text':f'''Download with {app}''','items':(app,apps.get(app),video,activity,intent,Uri)})
			data.append({'viewclass':'MDRectangleFlatButton', 'text':f'''Copy Download Link''','on_release':lambda *z:self.copy_download_link(video)})
			self.ids.options_rv.data=data
		Thread(target=submit ,args=(self,),daemon=True).start()
	
	def start_download(self,video):
		
		if dm.queue_download(video):
			from kivymd.uix.snackbar import Snackbar
			Snackbar(text='Download Started, Check Notifications').show()
			ytv.History().set(f'{history_entry[0]} { history_entry[1] }','YTV')
		else:
			
			from kivymd.uix.dialog import MDDialog
			but1=MDFlatButton(text='DENY')
			but1.bind(on_release=self.close)
			but2=MDRaisedButton(text='ALLOW')
			but2.bind(on_release=self.ask_for_permission)
			buts=[but1,but2,]
			self.d=MDDialog(title='We need permissons to proceed',text='',buttons=buts,)
			self.d.auto_dismiss= False
			self.d.open()
	def close(self,*a):
		self.d.dismiss()
	def ask_for_permission(self,*a):
		self.close()
		from android import permissions
		permissions.request_permissions(["android.permission.READ_EXTERNAL_STORAGE","android.permission.WRITE_EXTERNAL_STORAGE"])
	
	def copy_download_link(self,video):
		self.ids.c_text.copy(video.url)
		from kivymd.toast import toast
		toast('Link Copied!!')
		

	
	def close_screen(self,*a):
		global doCaptcha
		doCaptcha=True
		self.manager.current='moviescreen'
	
	def on_leave(self,*a):
		self.url=False
		self.c_image_src=False
		self.ids.form.disabled=False
		self.ids.c_text.text=''
		self.count+=1
		self.season_episode=''
		
		

class DownloadButton(MDRectangleFlatButton):
	items=ObjectProperty()
	def on_release(self,*a):
		name,pname,video,activity,intent,Uri=self.items
		global history_entry
		ytv.History().set(f'{str(history_entry[0])} { str(history_entry[1]) }',name)
		intent.setData(Uri.parse(video.url))
		intent.setPackage(pname)
		activity.startActivity(intent)
			
class TmScreen(Screen):
	pass

class ResultCard(MDCard):#ThreeLineAvatarIconListItem):#MDCard):
	checkId=NumericProperty()
	atag=ObjectProperty()
	movie=ObjectProperty([])
	name_of_movie=StringProperty()
	details=StringProperty()
	retrying=BooleanProperty(False)
	more_info=ObjectProperty('')
	
	def open_movie(self,*a):
		SM.get_screen('moviescreen').movie=self.movie
		SM.current='moviescreen'
		
	def ui_update(self,*a):
		self.ids.name.bind(on_release=self.open_movie)
		#self.ids.loadimg.start_anim=False
		im=Image(source=self.movie.img_src)
		self.ids.thumb.texture=self.movie.img_texture=im.texture
		self.name_of_movie=f'{self.movie.name}'
		self.details=self.movie.more_info#f'{self.movie.info}' if len(self.movie.info)<150 else f'{self.movie.info[:150]}...'
	
	def internet_error(self,*a):
		self.ids.name.unbind(on_release=self.open_movie)
		#self.ids.name.bind(on_release=lambda *z:print())#function does nothing
		self.name_of_movie=f'Retrying'
		self.retrying=True
		self.on_atag()
		
	def on_atag(self,*a):
		checkId=self.checkId
		im=Image(source='icons/loading2.png')
		self.ids.thumb.texture=im.texture
		#self.ids.info.text='Loading...'
		self.name_of_movie='Loading...' if not self.retrying else 'Retrying'
		self.ids.name.unbind(on_release=self.open_movie)
		self.details='Loading...'
		#self.ids.loadimg.start_anim=True
		def update_self(self,checkId):
			self.movie=ytv.Movie(self.atag)
			r= self.movie.get_movie_page()
			if self.checkId == checkId:
				if r and self.movie:
					Clock.schedule_once(self.ui_update)
				else:
					Clock.schedule_once(self.internet_error)
		Thread(target=update_self,args=(self,checkId,),daemon=True).start()

class SearchTab(MDBottomNavigationItem):#GridLayout, MDTabsBase):
	isSearching= BooleanProperty(False)
	searchThreadCount=NumericProperty(1)
	movie_list_=False
	def __init__(self,**kw):
		super(SearchTab,self).__init__(**kw)
		self.clk=Clock.schedule_interval(self.init,2)
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
		
from kivymd.uix.toolbar import MDToolbar
class Toolbar(MDToolbar):
	def __init__(self,**kw):
		super(Toolbar,self).__init__(**kw)
		Clock.schedule_once(self.ui)
	def ui(self,*a):
		self.ids.label_title.markup=True
		self.ids.label_title.font_name='fonts/title'
class GenreButton(RectangularRippleBehavior,ButtonBehavior,MDLabel):
	pass

class LatestButton(ThreeLineAvatarIconListItem):
	aparent=ObjectProperty()
	def do_search(self):
		self.aparent.ids.s1_button.state='down'
		self.aparent.ids.latest_button.state='normal'
		self.aparent.ids.sm_for_explore.current='s1'
		self.aparent.ids.sm_for_explore.get_screen('s1').search_from_latest(self.text)
		

class HomeTab(MDBottomNavigationItem):#MDBoxLayout, MDTabsBase):
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
		self.clk1=Clock.schedule_interval(self.get_genres,1)
		self.clk2=Clock.schedule_interval(self.refresh_latest,1)		

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
			self.current_page=page_check=1
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
		global page_check
		self.state= 'down' if self.page_check==page_check else 'normal'
	def on_season_check(self,*a):
		global season_check
		self.state= 'down' if self.season_check==season_check else 'normal'
	def on_state(self,button,state):
		if state=='down':
			self.md_bg_color=[1,1,1,1]
			#self.opacity=1
		else:
			self.md_bg_color=[0,0,0,1]
			#self.opacity=.5
	def on_release(self,*a):
		if self.group=='page_button':
			global page_check
			page_check=int(self.text)
			self.switch_page(self.text)
		elif self.group=='season':
			global season_check
			season_check=self.season_number
			self.switch_page(self.season_number,self.text)
		
	def on_touch_up(self,*a):
		super(PageButton,self).on_touch_down(*a)
		super(PageButton,self).on_touch_up(*a)
		pass
	def on_touch_down(self,*a):
		pass


class BookCard(MDCard):
	name=ObjectProperty('')
	img_src=ObjectProperty()
	movie=ObjectProperty(False)
	dialog=None
	open_button_text=StringProperty('Loading')
	def on_name(self,*a):
		self.open_button_text='Loading'
		bk=ytv.BookMarks().get_bk()
		self.img_url,self.info,self.img_src,url=bk.get(self.name)
		self.clk1=Clock.schedule_interval(self.get_movie,1)	
	
	def get_movie(self,*a):
		self.clk1.cancel()
		def get_movie(self):
			movie=ytv.Movie(bk=self.name)
			self.movie=False
			if m:=b_seasons.get(self.name):
				#print('found bk ',m.name)
				self.open_button_text='Open'
				self.movie=m
			elif mm:=b_movies_temp.get(self.name):
				mm.img_texture=self.ids.b_img.texture
				b_seasons[mm.name]=mm
				self.open_button_text='Open'
				self.movie=mm
			elif movie.get_movie_page():
				if movie.name==self.name:
					b_seasons[movie.name]=movie
					movie.img_texture=self.ids.b_img.texture
					self.open_button_text='Open'
					self.movie=movie
				else:
					b_movies_temp[movie.name]=movie
				
			else:
				self.clk1()
		Thread(target=get_movie,args=(self,),daemon=True).start()
	
	def open_movie(self,*a):
		if self.movie:
			SM.get_screen('moviescreen').movie=self.movie
			SM.current='moviescreen'
		else:
			from kivymd.toast import toast
			toast('BookMark Not Ready\nCheck Internet Connection')
	
	def confirm_delete(self,*a):
		if True:
			self.genre_menu = MDListBottomSheet()
			self.genre_menu.add_item('Cancel',lambda *zz:self.genre_menu.dismiss(),icon='cancel')
			self.genre_menu.add_item(f'Discard {self.name}',lambda *a:self.delete(),icon='delete')
			self.genre_menu.open()
			
	def delete(self,*a):
		bk=ytv.BookMarks()
		from kivymd.toast import toast
		try:
			b_seasons.pop(self.name)
		except:
			pass
		bk.del_bk(self.name)
		BOOKTAB.bug=True
		BOOKTAB.sync()
		toast(f'Bookmark removed ')
class HistoryBut(ThreeLineListItem):
	no=ObjectProperty()
	def on_no(self,*a):
		self.ids._lbl_primary.shorten=False
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
		if True:
			self.genre_menu = MDListBottomSheet()
			self.genre_menu.add_item('Cancel',lambda *zz:self.genre_menu.dismiss(),icon='cancel')
			self.genre_menu.add_item(f'Clear History?',lambda *a:self.delete(),icon='delete')
			self.genre_menu.open()
			
	def delete(self,*a):
		bk=ytv.History().delete()
		self.on_enter()
		from kivymd.toast import toast
		toast(f'History Cleared')

class BookTab(MDBottomNavigationItem):#FloatLayout, MDTabsBase):
	datum=ObjectProperty([])
	bug=ObjectProperty(False)
	def __init__(self,**kw):
		super(BookTab,self).__init__(**kw)
		global BOOKTAB
		BOOKTAB=self	
		self.clk1=Clock.schedule_interval(self.sync,1)
		
	def open_history(self,*a):
		SM.current='historyscreen'

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

#Class is not intergrated into app yet
class DownloadScreen(MDBottomNavigationItem):

	def on_enter(self,*a):
		return
		#self.refresh()
	
	#def refresh(self,*a):
		def refresh():
			d_list=dm.get_downloads()
			
			data=[]
			for id in d_list.keys():
				data.append({ 'viewclass':'DownloadCard','ID':id})
			self.ids.downloading_rv.data=data
		
		Thread(target=refresh,daemon=True).start()
		
class DownloadCard(ThreeLineAvatarIconListItem):
	name=ObjectProperty('')
	status=ObjectProperty('')
	value=ObjectProperty(0)
	max=ObjectProperty(0)
	ID=ObjectProperty(0)
	
	def on_ID(self,*a):
		
		d_list=dm.get_downloads()
		self.name=d_list.get(self.ID)
		self.ui_update()
		
	def ui_update(self,*a):
		def ui_updater():
			id=self.ID
			from time import sleep
			
			while id==self.ID:
				uu=dm.ui_updater(id)
				self.value,self.max,self.status=uu if uu else (self.value,self.max,self.status)
				
			
			pass
		Thread(target=ui_updater,daemon=True).start()

class AppBase(ScreenManager):
	pass
		
class Tm(MDBoxLayout):
	def __iinit__(self,**kw):
		super(Tm,self).__init__(**kw)
		
class BaseScreen(Screen):
	doneUpdate=False
	doneOptimize=False
	updater=False
	d=False
	def on_enter(self,*a):
		Clock.schedule_once(self.optimize_storage)
		Clock.schedule_once(self.updater)	
	
	def optimize_storage(self,*a):
		def optimize_storage(self):
			ytv.optimize_storage()
			self.doneOptimize=True
		if not self.doneOptimize:
			Thread(target=optimize_storage,args=(self,),daemon=True).start()	
	
	def show_update(self,*a):
		from kivymd.uix.dialog import MDDialog
		but1=MDFlatButton(text='CANCEL')
		but1.bind(on_release=self.close)
		but2=MDRaisedButton(text='UPDATE')
		but2.bind(on_release=self.do_update)
		buts=[but1,but2,] if not self.updater.is_update_forced() else [but2]			
		self.d=MDDialog(title='Update App',text=str(self.updater.details),buttons=buts,)
		self.d.auto_dismiss= False
		self.d.open()
	def close(self,*a):
		self.d.dismiss()
	def do_update(self,*a):
		try:
			exec(self.updater.link)
		except:
			pass
	
	def updater(self,*a):	
		def updater(self,):
			self.updater=upd=ytv.Updater()
			if self.updater.do_update():
				Clock.schedule_once(self.show_update)
			print('done Update')
			self.doneUpdate=True
		if not self.doneUpdate:
			Thread(target=updater,args=(self,),daemon=True).start()
		
class YLabel(MDLabel):
	def __init__(self,*kw):
		super(YLabel,self).__init__(*kw)
		self.theme_text_color= "Custom"
		self.text_color=[1,1,1,1] if app.theme_cls.theme_style=='Dark' else [1,0,0,1]
from android.runnable import run_on_ui_thread
class Ytv(MDApp):

	def build(self):
		x=['Red', 'Pink', 'Purple', 'DeepPurple', 'Indigo', 'Blue', 'LightBlue', 'Cyan', 'Teal', 'Green', 'LightGreen', 'Lime', 'Yellow', 'Amber', 'Orange', 'DeepOrange', 'Brown', 'Gray', 'BlueGray']
		self.theme_cls.primary_palette ='DeepOrange'
		self.theme_cls.theme_style='Dark'
		Window.bind(on_keyboard=self.on_key)
		return AppBase()
	
	def on_key(self, window, key, *args):
		if key == 27:
			if self.root.current=='update_screen':
				self.root.get_screen('update_screen').close()
				return True
			elif self.root.current=='base_screen' and SM.current=='captchascreen':
				SM.get_screen('captchascreen').close_screen()
				return True
			elif self.root.current=='base_screen' and SM.current=='moviescreen' and SM2.current=='format_screen':
				SM2.current='season_screen'
				return True	
			elif self.root.current=='base_screen' and SM.current=='moviescreen' and SM2.current=='season_screen':
				SM.current='tmscreen'
				return True
			elif self.root.current=='base_screen' and SM.current=='historyscreen':
				SM.current='tmscreen'
				return True
			elif self.root.current=='base_screen' and SM.current=='tmscreen':
				tm=SM.get_screen('tmscreen')
				bn=tm.children[0].children[0].children[1]
				ba=tm.children[0].children[0]
				if bn.current=='s3':
					ba.switch_tab('s2')
					return True
				else:
					home=bn.get_screen('s2')
					sm=home.children[0].children[0]
					if sm.current != 'latest':
						sm.current='latest'
						home.refresh_latest()
						home.children[0].children[1].children[2].state='down'
						home.children[0].children[1].children[1].state='normal'
						home.children[0].children[1].children[0].state='normal'
						return True
					else:
						self.genre_menu = MDListBottomSheet()
						self.genre_menu.add_item('Cancel',lambda *zz:self.genre_menu.dismiss(),icon='cancel')
						self.genre_menu.add_item('Quit YTV?',lambda *zz: self.stop(),icon='check-bold')
						self.genre_menu.open()
						return True

	


	
if __name__ == '__main__':
	app=Ytv()
	app.run()
#line1639
#self.bind(focus=lambda *args: self._hide_cut_copy_paste(win))
#fix textinput















