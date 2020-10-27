ua={"User-Agent": "Mozilla/5.0 (Linux; Android 5.1; A1603 Build/LMY47I; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/43.0.2357.121 Mobile Safari/537.36"}
time_out=15
index='https://tvshows4mobile.com'
#index='https://o2tvseries.com'
imgs='imgs/'
cache='cache/'

book= 'bookmarks/'
bookImg=book+'imgs/'
updater='update/update.json'
import os,dill,certifi
os.environ['SSL_CERT_FILE'] = certifi.where()


def getFolderSize(p):
	from functools import partial
	prepend = partial(os.path.join, p)
	return sum([(os.path.getsize(f) if os.path.isfile(f) else getFolderSize(f)) for f in map(prepend, os.listdir(p))])
	
def optimize_storage():
	from shutil import rmtree
	import os
	if not os.path.exists(cc:=cache):
		os.mkdir(cc)
		
	if not os.path.exists(ii:=imgs):
		os.mkdir(ii)
		
	rmtree(cache,ignore_errors=True)
	os.mkdir(cache)
	size=getFolderSize(imgs)/1_000_000
	#size2=getFolderSize(book)/1_000_000
	
	if size>20:
		rmtree(imgs,ignore_errors=True)
		os.mkdir(imgs)
	dset=BookMarks().get_delete_set()
	if len(dset)>1:
		for i in dset:
			if i != 0:
				try:
					os.remove(i)
				except:
					pass
		os.remove(book+'to_trash.txt')
				
	print('storage optimised')
	

class Updater():
	url="https://ytvseries.firebaseio.com/.json"
	def __init__(self):
		self.version=1
		content=self.read_json()
		self.init(content)

		if self.check_date():
			while True:
				if msg:=self.get():
					if self.check_version(msg):
						d={"version": msg['version'],"details":msg['details'],"type": msg['type'] ,"link":msg['link'],"date":self.today,"show":True}
					else:
						d={"version": msg['version'],"details":msg['details'],"type": msg['type'] ,"link":msg['link'],"date":self.today,"show":False}
					self.write_json(d)
					break
				else:
					continue					
		
		content=self.read_json()
		self.init(content)
		
	def do_update(self):
		if self.vv != self.version:
			return True
		else:
			return False	
	def is_update_forced(self,*a):
		if self.type:
			return True
		else:
			return False	

	def init(self,content):
		self.vv=content['version']
		self.details=content['details']
		self.type=content['type']
		self.link=content['link']
		self.date=content['date']
		self.show=content['show']
		
	def read_json(self):
		import json
		with open(updater,'r') as fd:
			content=json.load(fd)
			return content
	def write_json(self,d):
		import json
		with open(updater,'w') as fd:
			json.dump(d,fd)		
		
	def check_version(self,msg):
		return True if msg['version']!=self.version else False	
	def check_date(self):
		import datetime
		self.today=str(datetime.date.today())
		return False if self.today==self.date else True	
		
	def get(self):
		import requests
		try:
			request = requests.get(self.url)
		except:
			return False
		return request.json()


def req(url):
	import requests as c
	import bs4
	global ua
	global time_out
	res=c.get(url, headers=ua, allow_redirects=True,timeout=time_out)
	soup=bs4.BeautifulSoup(res.text,features='html.parser')
	return (res,soup)
	
def latest():
	try:
		x,soup= req(index+'/search/recently_added')
		recently_added=radd=soup.find_all('div',class_='data main',)
		recent=[]
		for j in recently_added:
			i=j.text
			try:
				a=i[:i.index('- Season')]
			except:
				try:
					a=i[:i.index('Episode')]
				except:
					a=i
					c=' '
					b=' '
				else:
					b=' '
					c=i[i.index('Episode'):-1]
			else:
				try:
					b=i[i.index('Season'):i.index('Episode')]
				except:
					b=i[i.index('Season'):]
					c=' '
				else:
					c=i[i.index('Episode'):-1]
			datum=[a,b,c]
			recent.append(datum)
			
		return recent
	except:
		return None
def deep_compare(a,b):

	if a.lower() in b.lower():
		return 1
	else:
		count=len(a)
		total=0
		bb=[i.lower() for i in list(b) if i not in['']]
		for letter in a:
			if letter in bb:
				bb.remove(letter)
				total+=1
		if total==count:
			dn=len(b)
			percent=(total/dn)
			return percent
	return 0

def compare(text,results):
	words=[i.lower() for i in text.split(' ') if i!='']
	res={}
	for result in results:
		dnum=len(words)
		num=0
		rss=result.text.lower().split(' ')
		rss=[i.lower() for i in rss if i!='']
		for word in words:
			for rs in rss:
				if no:=deep_compare(word,rs):
					num+=no
					break
					
		score=int((num/dnum)*100)
		if score==0:
			continue
		if k:=res.get(score):
			k.append(result)
		else:
			res[score]=[result]
	keys=list(res.keys())
	keys.sort()
	keys.reverse()
	r=[]
	for key in keys:
		items=res.get(key)
		for item in items:
			r.append(item)
	return r

def search4(exp,m=False):
	if len(exp)==exp.count(' ') or len(exp)==0:
		return False,False
	try:
		if m:
			movie_list_=m
		else:
			x,soup=req(index+'/search/list_all_tv_series')
			movie_list_= soup.select('div .data a' ,)
	except:
		return False,False

		
	moviez=compare(exp,movie_list_)
	if len(moviez)== 0:
		return False,False
	else:
		return moviez,movie_list_

def get_url_from_name(name):
	name_list=name.split(' ')
	s='-'.join(name_list).replace('---','-').replace('--','-')
	return f"{index}/{s}/index.html"

class BookMarks():
	def clear_bk(self):
		fd=self.create_pkl()
		fd.close()
		a=book+'bk.pkl'
		fd=open(a,'wb')
		dill.dump({},fd)
		fd.close()
		from shutil import rmtree
		rmtree(bookImg)
		import os
		os.mkdir(bookImg)
	def create_pkl(self):
		if not os.path.exists(b:=book):
			os.mkdir(b)
			os.mkdir(bookImg)	
		if not os.path.exists(a:=book+'bk.pkl'):
			fd=open(a,'wb')
			dill.dump({},fd)
			fd.close()		
		return open(book+'bk.pkl','rb')
	
	def get_bk(self):
		fd=self.create_pkl()
		self.bk=dill.load(fd)
		fd.close()
		return self.bk
	def save(self):
		fd=self.create_pkl()
		fd.close()
		a=book+'bk.pkl'
		fd=open(a,'wb')
		dill.dump(self.bk,fd)
		fd.close()						
	
	def add_bk(self,name,content):
		self.get_bk()
		self.bk[name]=content
		self.save()
		img_url,info,img_src,url=self.bk.get(name)
		dset=self.get_delete_set()
		if img_src in dset:
			dset.remove(img_src)
		self.set_delete_set(dset)
	
	def get_delete_set(self):
		if not os.path.exists(p:=book+'to_trash.txt'):
			with open(p,'w') as fd:
				fd.write(str({0}))
				return {0}
		with open(p:=book+'to_trash.txt','r') as fd:
			q=fd.read()
			from ast import literal_eval
			c=literal_eval(q)
			dset=c
			return dset
	
	def set_delete_set(self,dset):
		if not os.path.exists(p:=book+'to_trash.txt'):
			with open(p,'w') as fd:
				fd.write(str(dset))
				return
				
		with open(p:=book+'to_trash.txt','w') as fd:
			fd.write(str(dset))
						
	def del_bk(self,name):
		self.get_bk()
		img_url,info,img_src,url=self.bk.get(name)
		dset=self.get_delete_set()
		dset.add(img_src)
		self.set_delete_set(dset)
		self.bk.pop(name)
		self.save()
		
	def is_bk(self,name):
		self.get_bk()
		return True if name in self.bk.keys() else False
		

class Movie():
	def __init__(self,atag=None,bk=None):
		self.url=atag.attrs['href'] if atag else None
		self.name=atag.text if atag else None
		self.img_url=None
		self.info=None
		self.img_src=None
		self.seasons=None
		self.img_texture=None
		self.season_soup=None
		self.season_response=None	
		self.more_info=None
		self.bk=bk
	def get_movie_page(self):
		try:
			if self.bk:
				self.name=self.bk
				bk=BookMarks().get_bk()
				self.img_url,self.info,self.img_src,self.url=bk.get(self.bk)
				self.season_response,self.season_soup=req(self.url)
				self._get_seasons()
				return True
		except:
			return None		
		try:
			if obj:=self.in_cache():
				self.more_info,self.img_url,self.info,self.img_src,text,url=obj
				import bs4
				self.season_soup=bs4.BeautifulSoup(text,features='html.parser')
			else:
				self.season_response,self.season_soup=req(self.url)
				
				self.parse_movie_page(self.season_soup)
						
		except:
			return None
		self._get_seasons()
		self.cache_thumb()
		return True
	
	def parse_movie_page(self,s):
		
		if s:
			data=s.select('div .img img')
			data2=s.select('div .serial_desc')
			data3=s.select('div .row')
			text_=''
			for i in data3:
				text_+=i.text.replace('\n','')
			a=text_
			try:
				cast=a[a.index('Casts:')+6:a.index('Genres:')]
				genres=a[a.index('Genres:')+7:a.index('Run Time:')]
				run_time=a[a.index('Run Time:')+10:a.index('Views:')]
			except:
				cast='Unavaliable'
				genres='Unavaliable'
				run_time='Unavaliable'
			self.more_info=f'[color=BF360C]Casts:[/color]{cast}\n[color=BF360C]Genres:[/color]{genres}\n[color=BF360C]Run Time:[/color]{run_time}'
			self.img_url=data[0].attrs.get('src')
			self.info=data2[0].text
			self.img_src=imgs+self.img_url.split('/')[-1]
			self.cache_self()

	def cache_self(self):
		import dill
		l=( self.more_info,self.img_url,self.info,self.img_src,self.season_response.text,self.url)
		with open(cache+f'{self.name}.pkl','wb') as fd:
			dill.dump(l ,fd)
	def bookmark(self):
			s=BookMarks()
			from shutil import copyfile
			try:
				copyfile(self.img_src,bookImg+self.img_url.split('/')[-1])
			except:
				pass
			try:
				s.add_bk(self.name,( self.img_url,self.info,bookImg+self.img_url.split('/')[-1],self.url))
			except:
				pass
			
		
			
	def in_cache(self):
		import os ,dill
		if True:
			for pkl in os.listdir(cache):
				if f'{self.name}.pkl' == pkl:	
					with open(cache+pkl,'rb') as fd:
						obj=dill.load(fd)
					return obj
			return False
					
	
	def cache_thumb(self):
		global imgs
		import os 
		for pic in os.listdir(imgs):
			if self.img_src == imgs+pic:
				#print(f'Found {self.name} thumbnail in archive')
				return
		try:
			pic,s=req(self.img_url)	
		except:
			#print(f'Failed to archive {self.name} thumbnail')
			return
		with open(self.img_src,'wb') as fd:
			fd.write(pic.content)
			
	def get_seasons(self):
		return self.seasons
	def _get_seasons(self):
		started=False
		if self.season_soup:
			seasons=self.season_soup.select('div .data a')
			seasons.reverse()
			self.seasons=seasons
			return seasons
		else:
			return False

def get_episodes(urlz):
	try:
		z,s=req(urlz)
		episodes=s.select('div .data a')
		if_next=s.select('div .page_nav a')
	except:
		return [False]
		
	for i in if_next:
		if 'Next' in i.text:
			for i in get_episodes(i.attrs['href']):
				episodes.append(i)
	
	return episodes if False not in episodes else []

def get_download_link(url):
	try:
		z,soup=req(url)
	except:
		return False
	all_links=soup.select('div .data a')
	download_links=j=[a for a in all_links if 'download' in a.attrs.get('href').lower()]
	return download_links
def get_genres():
	try:
		r,s=req(f'{index}/search/genre')
	except:
		return None
	genre_list=b=s.select('div .data a' ,)
	return genre_list

class Genre():
	def __init__(self,atag):
		self.type=atag.text
		self.url=atag.attrs.get('href')

	def get_movies(self):
		try:
			x,soup=req(self.url)
		except:
			return None
		movie_list_=soup.select('div .data a' ,)
		if len(movie_list_)== 0:
			return None
		else:
			return movie_list_

class Captcha():
	def __init__(self,url):
		from requests import Session,get
		import bs4
		self.c=Session()
		self.url=url
		
	def get_image(self):
		self.r,soup=self.req(self.url)
		if self.r:
			captcha_url_raw=soup.select('img')[0]
			self.captcha_url=index+captcha_url_raw.attrs.get('src')
			return self.cache_cImage()
		else:
			return False
	def cache_cImage(self):
		try:
			captcha_image=self.c.get(self.captcha_url, headers=ua, allow_redirects=True,timeout=time_out)
		except:
			return False
		try:
			import shutil,os
			shutil.rmtree('caps',ignore_errors=True)
		except:
			pass
		finally:
			os.mkdir('caps')
		with open('caps/password.png','wb') as fs:
			fs.write(captcha_image.content)
		return True
	def submit(self,text):
		datum={ "captchainput": text,"submit":"Continue Download"}
		hd={"User-Agent": "Mozilla/5.0 (Linux; Android 5.1; A1603 Build/LMY47I; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/43.0.2357.121 Mobile Safari/537.36",'Range': f'bytes=0-1'}
		try:
			video=r=self.c.post(self.r.url,data=datum, headers=hd, allow_redirects=True,timeout=time_out,stream=True)
		except:
			return False,False		
		
		try:
			con=video.headers["Content-Range"]
			size= int(int(con.split("/")[1])/1_000_000)
		except:
			size=False
		return video,size
			
	def get_browsers(self,*a):
		from jnius import autoclass		
		activity = autoclass('org.kivy.android.PythonActivity').mActivity
		Intent = autoclass('android.content.Intent')
		Uri = autoclass('android.net.Uri')
		packageManager = pm=activity.getPackageManager()
		
		intent =Intent(Intent.ACTION_VIEW)
		intent.setData(Uri.parse('http://www.google.com'))
		intent.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
		
		act1= packageManager.queryIntentActivities(intent,0)
		acts=set([])
		for i in range(act1.size()):
			acts.add(act1.get(i))
			
		apps={}
		for j in acts:	
			pname=j.activityInfo.packageName
			ai=pm.getApplicationInfo(pname,0)
			name=pm.getApplicationLabel(ai)
			apps[name]=pname 
		return apps,activity,intent,Uri			
	
	def req(self,url):
		global ua
		global time_out
		import bs4
		try:
			res=self.c.get(url, headers=ua, allow_redirects=True,timeout=time_out)
			soup=bs4.BeautifulSoup(res.text,features='html.parser') 
		except:
			return [False,False]
		return (res,soup)
class History():
	def init(self):
		import sqlite3,datetime
		conn = sqlite3.connect('history.db',detect_types=sqlite3.PARSE_DECLTYPES)
		try:
			conn.execute('''CREATE TABLE HISTORY (NAME           TEXT    NOT NULL, APP TEXT NOT NULL,DATE TEXT,ID INTEGER PRIMARY KEY  AUTOINCREMENT );''')
		except:
			pass
		return conn
		#a=str(datetime.date.today().strftime("%b %d /%Y"))
	
	def set(self,*info):
		import sqlite3,datetime
		conn=self.init()
		info=info+(datetime.datetime.now(),)
		conn.execute(f"INSERT INTO HISTORY (NAME,APP,DATE) VALUES ( ?,?,?);",info)
		conn.commit()
	def get(self):
		import sqlite3,datetime
		conn=self.init()
		result=conn.execute('select NAME,APP,DATE from HISTORY order by ID desc')
		return result
	def delete(self):
		import sqlite3,datetime
		conn=self.init()
		result=conn.execute('delete from HISTORY where ID !=-1')
		conn.commit()
		
if __name__=='__main__':
	w=latest()
	print(w)
