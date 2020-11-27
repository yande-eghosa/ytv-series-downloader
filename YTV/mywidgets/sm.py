from kivy.uix.screenmanager import ScreenManager
from kivy.lang import Builder

Builder.load_string('''

<Sm>:
	TmScreen:
	MovieScreen:
	CaptchaScreen:
	HistoryScreen:

''')

class Sm(ScreenManager):
	def __init__(self,**kw):
		super(Sm,self).__init__(**kw)
		import cfg
		cfg.SM =self
	
