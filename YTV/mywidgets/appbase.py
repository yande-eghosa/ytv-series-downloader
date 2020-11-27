from kivy.uix.screenmanager import ScreenManager
from kivy.lang import Builder

Builder.load_string('''
<AppBase>:
	BaseScreen:
''')

class AppBase(ScreenManager):
	pass
