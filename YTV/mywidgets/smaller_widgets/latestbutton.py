from kivymd.uix.list import ThreeLineAvatarIconListItem
from kivy.properties import ObjectProperty
from kivy.lang import Builder

Builder.load_string('''

<LatestButton>:
	text:
	IconRightWidget:
		icon:'arrow-top-right-thick'
		on_release: root.do_search()
''')

class LatestButton(ThreeLineAvatarIconListItem):
	aparent=ObjectProperty()
	def do_search(self):
		self.aparent.ids.s1_button.state='down'
		self.aparent.ids.latest_button.state='normal'
		self.aparent.ids.sm_for_explore.current='s1'
		self.aparent.search_from_latest(self.text)
