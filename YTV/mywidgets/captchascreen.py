import cfg
from kivy.uix.screenmanager import Screen
from kivy.uix.image import *
from kivy.clock import Clock
from kivy.properties import * 
from threading import Thread
import ytvApi as ytv
from downloadmanager import dm
from kivy.lang import Builder
from kivy import platform

Builder.load_string('''

<CaptchaScreen>:
	name:'captchascreen'
	MDBoxLayout:
		orientation:'vertical'
		spacing:dp(20)
		MDBoxLayout:
			size_hint:1,None
			MDIconButton:
				icon:"arrow-left-bold"
				on_release:root.close_screen()
			MDLabel:
				size_hint:1,None
				halign:'center'
				text:'Solve Captcha'+root.season_episode
		MDBoxLayout:
			padding:dp(5)
			size_hint:1,.25
			Image:
				id:c_image
				nocache:True
				allow_stretch:True
				keep_ratio:True
				#source:''
		MDBoxLayout:
			id:form
			size_hint:1,None
			padding:dp(20)
			spacing:dp(10)
			MYTextField:
				id:c_text
				use_bubble:True
				on_text_validate:root.submit()
				current_hint_text_color:1,1,1,1
				hint_text:'What do you see?'
			MDRaisedButton:
				text:'Submit'
				on_release:root.submit()
		RecycleView:
			id: options_rv
			size_hint_y:
			key_viewclass: 'viewclass'
			key_size: 'height'	
			RecycleBoxLayout:
				id: options_rb
				default_size: None, None
				default_size_hint: 1, None
				size_hint_y: None
				height: self.minimum_height
				orientation: 'vertical'
				spacing:dp(10)
				padding:dp(20)

''')

class CaptchaScreen(Screen):
	url=ObjectProperty()
	c_image_src=ObjectProperty()
	res=()
	count=0
	season_episode=ObjectProperty('')
	def on_url(self,*a):
		if self.url:
			#print(self.url)
			cfg.doCaptcha=True
			self.manager.current=self.name
			self.get_captcha()
	def get_captcha(self,*a):
			self.ids.form.disabled=False
			self.ids.options_rv.data=[]
			im=Image(source='icons/loading.png')
			self.ids.c_image.texture=im.texture
			def get_captcha(self,count):
				try:
					
					self.captcha=ytv.Captcha(self.url)
					if self.captcha.get_image():
						file_name='caps/password.png'
					
					self.c_image_src=file_name
				except:
					self.c_image_src=False
				if count==self.count:
					Clock.schedule_once(self.update_captcha)
			Thread(target=get_captcha ,args=(self,self.count,),daemon=True).start()
	
	def update_captcha(self,*a):
		if src:=self.c_image_src :
			im=Image(source=src ,nocache=True)
			self.ids.c_image.texture=im.texture
		else:
			im=Image(source='icons/404.png')
			self.ids.c_image.texture=im.texture
			self.ids.options_rv.data=[{'viewclass':'MDLabel', 'text':f'''Network Error''','halign':'center'},{'viewclass':'MDRectangleFlatButton', 'text':f''' Retry ''','on_release':self.get_captcha}]
	
	def submit(self,*a):
		self.ids.form.disabled=True
		im=Image(source='icons/loading1.png',nocache=True)
		self.ids.c_image.texture=im.texture
		self.ids.options_rv.data=[{'viewclass':'MDLabel', 'text':f'''Retrieving Download Link''','halign':'center'}]
		
		def submit(self):
			video,size=v,size=self.captcha.submit(self.ids.c_text.text)
			if video.url== self.captcha.r.url:
				error=video.text
				self.ids.options_rv.data=[{'viewclass':'MDLabel', 'text':f'''{error}''','halign':'center'},{'viewclass':'MDRectangleFlatButton', 'text':f''' Try Again ''','on_release':self.get_captcha}]
				return
			else:
				pass
			data=[]
			if size:
				data.append({'viewclass':'MDLabel', 'text':f'''{size} mb'''})
			if platform == 'android':
				apps,activity,intent,Uri=self.captcha.get_browsers()
				
				if dm.get_build_no():
					data.append({'viewclass':'MDRectangleFlatButton', 'text':f'''Download with Download Manager''','on_release':lambda *z:self.start_download(video)})
				for app in apps.keys():
					data.append({'viewclass':'DownloadButton', 'text':f'''Download with {app}''','items':(app,apps.get(app),video,activity,intent,Uri)})
				
			else:
				data.append({'viewclass':'MDRectangleFlatButton', 'text':f'''Download with Web Browser''','on_release':lambda *z:self.start_download(video)})
			data.append({'viewclass':'MDRectangleFlatButton', 'text':f'''Copy Download Link''','on_release':lambda *z:self.copy_download_link(video)})
			self.ids.options_rv.data=data
			
		Thread(target=submit ,args=(self,),daemon=True).start()
	
	def start_download(self,video):
		if platform !='android':
			import webbrowser
			webbrowser.open(video.url)
			ytv.History().set(f'{cfg.history_entry[0]} { cfg.history_entry[1] }','Web Browser')
		else:
			if dm.queue_download(video):
				from kivymd.uix.snackbar import Snackbar
				Snackbar(text='Download Started, Check Notifications').show()
				ytv.History().set(f'{cfg.history_entry[0]} { cfg.history_entry[1] }','YTV')
			else:			
				from kivymd.uix.dialog import MDDialog
				from kivymd.uix.button import MDFlatButton, MDRaisedButton
				but1=MDFlatButton(text='DENY')
				but1.bind(on_release=self.close)
				but2=MDRaisedButton(text='ALLOW')
				but2.bind(on_release=self.ask_for_permission)
				buts=[but1,but2,]
				self.d=MDDialog(title='We need permissons to proceed',text='',buttons=buts,)
				self.d.auto_dismiss= False
				self.d.open()
	def close(self,*a):
		self.d.dismiss()
	def ask_for_permission(self,*a):
		self.close()
		from android import permissions
		permissions.request_permissions(["android.permission.READ_EXTERNAL_STORAGE","android.permission.WRITE_EXTERNAL_STORAGE"])
	
	def copy_download_link(self,video):
		self.ids.c_text.copy(video.url)
		from kivymd.toast import toast
		toast('Link Copied!!')
	
	def close_screen(self,*a):
		cfg.doCaptcha=True
		self.manager.current='moviescreen'
	
	def on_leave(self,*a):
		self.url=False
		self.c_image_src=False
		self.ids.form.disabled=False
		self.ids.c_text.text=''
		self.count+=1
		self.season_episode=''
