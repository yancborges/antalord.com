import urllib.request
import pandas as pd
import writter
import url_handler
from urllib.parse import quote_from_bytes, quote

class kanji:

	def __init__(self,name,strokes,frequency,grade,jlpt):
		self.name = name
		self.strokes = strokes
		self.frequency = frequency
		self.grade = grade
		self.jlpt = jlpt

	def frequency(self):
		return self.frequency/2500

	def save(self):
		with open('kanji_dict.txt', 'a') as f:
			f.write(toString())

	def toString(self):
		return self.name + ',' + str(self.strokes) + ',' + str(self.frequency) + ',' + self.grade + ',' + self.jlpt

	def scrap(self):
		url = 'https://jisho.org/search/%23kanji%20'
		#resp = urllib.request.urlopen(url).read().decode("utf-8")
		resp = urllib.request.urlopen(url + quote_from_bytes(self.name.encode('utf-8'))).read().decode("utf-8")
		#writter.hey(resp,'htmltest.html','w',False,True)
		self.strokes = resp.split('<div class="kanji-details__stroke_count">')[1].split('<strong>')[1].split('</strong>')[0]
		self.frequency = resp.split('<div class="frequency">')[1].split('<strong>')[1].split('</strong>')[0]
		self.grade = resp.split('<div class="grade">')[1].split('<strong>')[1].split('</strong>')[0]
		self.jlpt = resp.split('<div class="jlpt">')[1].split('<strong>')[1].split('</strong>')[0]
		writter.hey(self.toString(),'kanji_dict.txt','a',True,False)
		
def create():
	try:
		with open('kanji_dict.txt', 'r') as f:
			size = len(f.read())
	except:
		writter.hey('name,strokes,frequency,grade,jlpt','kanji_dict.txt','w',True,False)


def load():
	kanji_dict = pd.read_csv('kanji_dict.txt')
	kanji_dict.set_index('name')
	return kanji_dict

def seek(kanji, kanji_dict):
	kanji_dict = list(kanji_dict.name)
	if(kanji.name not in kanji_dict):
		kanji.scrap()
		return False
	else:
		kanji.strokes = kanji_dict.ix[kanji.name,1]
		kanji.frequency = kanji_dict.ix[kanji.name,2]
		kanji.grade = kanji_dict.ix[kanji.name,3]
		kanji.jlpt = kanji_dict.ix[kanji.name,4]
		return True


