from kivy.animation import Animation
from kivy.properties import *
from kivy.uix.scatterlayout import ScatterLayout
from kivy.lang import Builder

Builder.load_string('''

<LoadImg>:
	do_rotation: False
	do_translation:False
	do_scale:False	

''')


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