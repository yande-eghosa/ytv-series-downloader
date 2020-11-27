import cfg
from kivymd.uix.list import *
from kivy.properties import *
from kivy.lang import Builder

Builder.load_string('''

<EpisodeButton>:
	text:
	IconRightWidget:
		icon:'download'
		on_release: root.open_download_options()
	



''')

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
			cfg.SM2.get_screen('format_screen').dlinks_url=url
			cfg.SM2.get_screen('format_screen').season_episode=f' --{self.text}'
