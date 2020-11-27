import cfg
from kivymd.uix.label import MDLabel
class YLabel(MDLabel):
	def __init__(self,*kw):
		super(YLabel,self).__init__(*kw)
		self.theme_text_color= "Custom"
		self.text_color=[1,1,1,1] if cfg.app.theme_cls.theme_style=='Dark' else [1,0,0,1]