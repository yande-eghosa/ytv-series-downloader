import cfg
from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.properties import *
import ytvApi as ytv

from threading import Thread

Builder.load_string('''

<MovieScreen>:
	name:'moviescreen'
	MDBoxLayout:
		orientation:'vertical'
		spacing:dp(10)
		MDBoxLayout:
			size_hint:1,None
			MDIconButton:
				icon:"arrow-left-bold"
				on_release:root.close_screen()
			MDLabel:
				size_hint:1,None
				halign:'center'
				markup:True
				font_name:'fonts/title'
				text:'[b][u]'+root.title
			MDIconButton:
				id:add_bk
				icon:
				on_release:root.bookmark()
		MDBoxLayout:
			size_hint_y:.4
			canvas.before:
				Color:
					rgba:app.theme_cls.primary_dark[:-1]+[.2]
				RoundedRectangle:
					size:self.size
					pos: self.pos
			LoadImg:
				id:loadimg
				Image:
					id:thumb
					allow_stretch:True
					keep_ratio: True
					source:
					nocache:True
			ScrollView:
				id:info_scroll_view
				#bar_pos_y:'left'
				bar_width:dp(5)
				bar_inactive_color:.7,.7,.7,.4
				padding:dp(10)	
				MDLabel:
					canvas.before:
						Color:
							rgba:0,0,0,.2
						RoundedRectangle:
							size:self.size
							pos: self.pos
					id:info
					text:root.info
					font_name:'fonts/movie_info'
					font_style: 'Subtitle1'
					valign:'top'
					size_hint_y:None
					height:self.texture_size[1]
		ScreenManager:
			id:sm
			SeasonScreen:
				id:ss
			FormatScreen:
				id:fs


''')

class MovieScreen(Screen):
	movie=ObjectProperty()
	title=StringProperty('Loading...')
	info=StringProperty('Loading...')
	
	def on_enter(self,*a):
		if self.movie.info and not cfg.doCaptcha:
			bk=ytv.BookMarks()
			self.ids.add_bk.icon='star' if bk.is_bk(self.movie.name) else 'star-outline'
			self.ids.thumb.texture=self.movie.img_texture
			self.title=t=self.movie.name
			cfg.history_entry.append(t)
			self.info=self.movie.info
			#self.ids.sm.clear_widgets()
			Thread(target=self.get_seasons,daemon=True).start()
		elif cfg.doCaptcha==True:
			cfg.doCaptcha=False

	def bookmark(self,*a):
		bk=ytv.BookMarks()
		from kivymd.toast import toast
		if self.ids.add_bk.icon=='star':
			self.ids.add_bk.icon='star-outline'
			bk.del_bk(self.movie.name)
			cfg.BOOKTAB.sync()
			toast(f'Bookmark removed ')
		else :
			self.ids.add_bk.icon='star'
			self.movie.bookmark()
			cfg.b_seasons[self.movie.name]=self.movie
			cfg.BOOKTAB.sync()
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
		cfg.BOOKTAB.bug=True
		cfg.BOOKTAB.sync()
		if not cfg.doCaptcha:
			self.ids.ss.kill()
			self.ids.thumb.texture=None
			self.title='Loading'
			self.info='Loading'
			cfg.history_entry=[]
			#self.ids.info_scroll_view.scroll_y=1
