import cfg
from kivymd.uix.list import *
from kivy.properties import *
from kivymd.uix.button import *
from kivymd.uix.card import MDCard
from kivy.lang import Builder
from kivy.clock import Clock
from threading import Thread
import ytvApi as ytv

Builder.load_string('''
<ResultCard>:
	Image:
		id:thumb
		nocache:True
		keep_ratio:True
		allow_stretch:True
	MDBoxLayout:
		orientation:'vertical'	
		GenreButton:
			canvas.before:
				Color:
					rgba:app.theme_cls.primary_dark[:-1]+[.4]
				Rectangle:
					size:self.size
					pos: self.pos
			id:name
			halign:'center'
			valign:'top'
			#font_size:dp(15)
			size_hint:1,None
			font_name:'fonts/movie_name'
			# font_size:dp(20)
			multiline:True
			markup:True
			text:'[u][b]'+root.name_of_movie+'[/u][/b]'
		ScrollView:
			padding:dp(10)
			do_scroll_y:False
			do_scroll_x:False
			MDLabel:
				canvas.before:
					Color:
						rgba:0,0,0,1
					Rectangle:
						size:self.size
						pos: self.pos
				markup:True
				text: root.details
				size_hint_y:None
				font_style: 'Subtitle1'
				#font_size:dp(15)
				height:self.texture_size[1]
	
<ResultCard_@MDCard>:
	orientation:'vertical'
	size_hint:None,None
	LoadImg:
		id:loadimg
		size_hint_y:
		Image:
			id:thumb
			allow_stretch:True
			keep_ratio:  True
			source:
			nocache:True
	GenreButton:
		canvas.before:
			Color:
				rgba:app.theme_cls.primary_dark[:-1]+[.4]
			Rectangle:
				size:self.size
				pos: self.pos
		id:name
		halign:'center'
		valign:'top'
		#font_size:dp(15)
		size_hint:1,None
		font_name:'fonts/movie_name'
		# font_size:dp(20)
		multiline:True
		markup:True
		text:'[u][b]'+root.name_of_movie+'[/u][/b]'
		#on_release: root.open_movie()
<ResultCard2@MDCard>:
	orientation:'vertical'
	size_hint_y:None
	height:dp(100)
	LoadImg:
		id:loadimg
		Image:
			id:thumb
			allow_stretch:True
			keep_ratio: True
			source:
			nocache:True
	BoxLayout:
		orientation:'vertical'
		size_hint_y:1
		MDLabel:
			id:name
			halign:'center'
			valign:'top'
			font_size:dp(15)
			sze_hint:1,None
			markup:True
			text:
			on_ref_press:print('pressed')
	
		MDIconButton:
			icon:
			hlign:'right'
			fnt_size:dp(5)
			sze_hint:1,None
			txt:'See more'
		MDLabel:
			id:info
			sze_hint:
			markup: True
			text:
			shorten: False
			shorten_from:'right'
			valign:'top'
			font_size:dp(13)
			on_ref_press:root.open_movie()

''')


class ResultCard(MDCard):#ThreeLineAvatarIconListItem):#MDCard):
	checkId=NumericProperty()
	atag=ObjectProperty()
	movie=ObjectProperty([])
	name_of_movie=StringProperty()
	details=StringProperty()
	retrying=BooleanProperty(False)
	more_info=ObjectProperty('')
	
	def open_movie(self,*a):
		cfg.SM.get_screen('moviescreen').movie=self.movie
		cfg.SM.current='moviescreen'
		
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
