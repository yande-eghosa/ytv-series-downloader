from kivymd.uix.list import ThreeLineListItem
from kivy.properties import ObjectProperty

class HistoryBut(ThreeLineListItem):
	no=ObjectProperty()
	def on_no(self,*a):
		self.ids._lbl_primary.shorten=False
