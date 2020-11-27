from kivy.uix.behaviors import ButtonBehavior
from kivymd.uix.behaviors import RectangularRippleBehavior
from kivymd.uix.label import MDLabel
from kivy.lang import Builder

Builder.load_string('''

<GenreButton>:
	ripple_scale: 0.7

''')

class GenreButton(RectangularRippleBehavior,ButtonBehavior,MDLabel):
	pass
