from kivy.uix.screenmanager import Screen
from kivy.lang import Builder

Builder.load_string('''

<TmScreen>:
	name:'tmscreen'
	MDBoxLayout:
		MDBottomNavigation:
			# lock_swiping:True
			text_color_normal:.3,.3,.3,1
			default_tab:1
			tab_bar_height:dp(35)
			
			HomeTab:
			BookTab:
	

''')

class TmScreen(Screen):
	pass