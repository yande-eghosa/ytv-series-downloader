import cfg

from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.core.window import Window

Builder.load_string('''

<MDLabel>:
	theme_text_color: "Custom"
	text_color:[1,1,1,1] if app.theme_cls.theme_style=='Dark' else [0,0,0,1]

''')

from mywidgets.custom_textfield.mytext import MYTextField
from mywidgets.appbase import AppBase
from mywidgets.base_screen import BaseScreen
from mywidgets.custom_toolbar import Toolbar
from mywidgets.sm import Sm
from mywidgets.tmscreen_contents.tmscreen import TmScreen
from mywidgets.tmscreen_contents.hometab import HomeTab
from mywidgets.tmscreen_contents.booktab import BookTab
from mywidgets.moviescreen_contents.moviescreen import MovieScreen
from mywidgets.moviescreen_contents.seasonscreen import SeasonScreen
from mywidgets.moviescreen_contents.formatscreen import FormatScreen
from mywidgets.captchascreen import CaptchaScreen
from mywidgets.historyscreen import HistoryScreen
from mywidgets.smaller_widgets.loadimg import LoadImg 
from mywidgets.smaller_widgets.episodebutton import EpisodeButton
from mywidgets.smaller_widgets.downloadbutton import DownloadButton
from mywidgets.smaller_widgets.resultcard import ResultCard
from mywidgets.smaller_widgets.latestbutton import LatestButton
from mywidgets.smaller_widgets.genrebutton import GenreButton
from mywidgets.smaller_widgets.pagebutton import PageButton
from mywidgets.smaller_widgets.bookcard import BookCard
from mywidgets.smaller_widgets.historybutton import HistoryBut
from mywidgets.smaller_widgets.ylabel import YLabel




class Ytv(MDApp):

	def build(self):
		x=['Red', 'Pink', 'Purple', 'DeepPurple', 'Indigo', 'Blue', 'LightBlue', 'Cyan', 'Teal', 'Green', 'LightGreen', 'Lime', 'Yellow', 'Amber', 'Orange', 'DeepOrange', 'Brown', 'Gray', 'BlueGray']
		self.theme_cls.primary_palette ='DeepOrange'
		self.theme_cls.theme_style='Dark'
		Window.bind(on_keyboard=self.on_key)
		return AppBase()
	
	def on_key(self, window, key, *args):
		SM=cfg.SM
		SM2=cfg.SM2

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
						from kivymd.uix.bottomsheet import MDListBottomSheet
						self.quit_menu = MDListBottomSheet()
						self.quit_menu.add_item('Cancel',lambda *zz:self.quit_menu.dismiss(),icon='cancel')
						self.quit_menu.add_item('Quit YTV?',lambda *zz: self.stop(),icon='check-bold')
						self.quit_menu.open()
						return True

if __name__ == '__main__':
	cfg.app=Ytv()
	cfg.app.run()
















