import cfg
from kivymd.uix.card import MDCard
from kivy.properties import ObjectProperty, StringProperty
from kivy.clock import Clock
from kivymd.uix.bottomsheet import MDListBottomSheet
from threading import Thread
from kivy.lang import Builder
import ytvApi as ytv

Builder.load_string('''

<BookCard>:
	orientation:'vertical'
	Image:
		id:b_img
		nocache:True
		source: root.img_src
		allow_stretch:True
		keep_ratio:True

	MDLabel:
		canvas.before:
			Color:
				rgba:0,0,0,1
			Rectangle:
				size:self.size
				pos: self.pos
		id:b_name
		text:root.name
		font_name:'fonts/movie_name'
		halign:'center'
		size_hint_y:None
	MDBoxLayout:
		size_hint_y:None
		canvas.before:
			Color:
				rgba:app.theme_cls.primary_dark[:-1]+[.4]
			Rectangle:
				size:self.size
				pos: self.pos
		MDRaisedButton:
			icon:'arrow-top-left-thick'
			text:root.open_button_text
			on_release:root.open_movie()
			
		MDIconButton:
			icon:'delete'
			text:'remove'
			on_release:root.confirm_delete()


''')

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
			if m:=cfg.b_seasons.get(self.name):
				#print('found bk ',m.name)
				self.open_button_text='Open'
				self.movie=m
			elif mm:=cfg.b_movies_temp.get(self.name):
				mm.img_texture=self.ids.b_img.texture
				cfg.b_seasons[mm.name]=mm
				self.open_button_text='Open'
				self.movie=mm
			elif movie.get_movie_page():
				if movie.name==self.name:
					cfg.b_seasons[movie.name]=movie
					movie.img_texture=self.ids.b_img.texture
					self.open_button_text='Open'
					self.movie=movie
				else:
					cfg.b_movies_temp[movie.name]=movie
				
			else:
				self.clk1()
		Thread(target=get_movie,args=(self,),daemon=True).start()
	
	def open_movie(self,*a):
		if self.movie:
			cfg.SM.get_screen('moviescreen').movie=self.movie
			cfg.SM.current='moviescreen'
		else:
			from kivymd.toast import toast
			toast('BookMark Not Ready\nCheck Internet Connection')
	
	def confirm_delete(self,*a):
		
		self.genre_menu = MDListBottomSheet()
		self.genre_menu.add_item('Cancel',lambda *zz:self.genre_menu.dismiss(),icon='cancel')
		self.genre_menu.add_item(f'Discard {self.name}',lambda *a:self.delete(),icon='delete')
		self.genre_menu.open()
			
	def delete(self,*a):
		bk=ytv.BookMarks()
		from kivymd.toast import toast
		try:
			cfg.b_seasons.pop(self.name)
		except:
			pass
		bk.del_bk(self.name)
		cfg.BOOKTAB.bug=True
		cfg.BOOKTAB.sync()
		toast(f'Bookmark removed ')
