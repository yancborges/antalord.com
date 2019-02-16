import writter
import kanji_scrapper
import pandas as pd

class results:

	def __init__(self,df,kanji_list):
		self.df = df
		self.kanji_list = kanji_list
		try:
			self.n5 = [round((self.df.jlpt.value_counts(normalize=True,dropna=False).at['N5'])*100,2),self.df.jlpt.value_counts().at['N5']]
		except:
			self.n5 = [0,0]
		try:
			self.n4 = [round((self.df.jlpt.value_counts(normalize=True,dropna=False).at['N4'])*100,2),self.df.jlpt.value_counts().at['N4']]
		except:
			self.n4 = [0,0]
		try:
			self.n3 = [round((self.df.jlpt.value_counts(normalize=True,dropna=False).at['N3'])*100,2),self.df.jlpt.value_counts().at['N3']]
		except:
			self.n3 = [0,0]
		try:
			self.n2 = [round((self.df.jlpt.value_counts(normalize=True,dropna=False).at['N2'])*100,2),self.df.jlpt.value_counts().at['N2']]
		except:
			self.n2 = [0,0]
		try:
			self.n1 = [round((self.df.jlpt.value_counts(normalize=True,dropna=False).at['N1'])*100,2),self.df.jlpt.value_counts().at['N1']]
		except:
			self.n1 = [0,0]

		self.k_n5 = list(self.df.name[self.df.jlpt=='N5'])
		self.k_n4 = list(self.df.name[self.df.jlpt=='N4'])
		self.k_n3 = list(self.df.name[self.df.jlpt=='N3'])
		self.k_n2 = list(self.df.name[self.df.jlpt=='N2'])
		self.k_n1 = list(self.df.name[self.df.jlpt=='N1'])
		self.mean = None

	def n_mean(self):

		series = self.df.jlpt.value_counts(sort=True)
		mean_value = series.sum()/series.count()
		start = 0
		last = 0
		count = 0
		stop = 0
		#levels = ['N5','N4','N3','N2','N1']
		levels = ['N1','N2','N3','N4','N5']
		while(count < 5):
			try:
				start += series[levels[count]]
				print(start,last)
				if(mean_value >= last and mean_value < start):
					stop = count
					break
				last += series.at[levels[count]]
			except:
				pass
			count += 1
		self.mean = levels[stop]
		return levels[stop]

			

def analyse_text(text):

	kanji_scrapper.create()
	data = kanji_scrapper.load()

	with open('hiraganaChart.txt', 'r', encoding='utf8') as h:
		hiraganaData = h.read()
	with open('katakanaChart.txt', 'r', encoding='utf8') as k:
		katakanaData = k.read()
	with open('punct.txt', 'r', encoding='utf8') as p:
		punctData = p.read()

	kanji_list = []
	kanji_names = []

	roman = '1234567890QWERTYUIOPASDFGHJKLÇZXCVBNMqwertyuiopasdfghjklçzxcvbnm'

	for char in text:

		if(char not in punctData):
			if(char not in hiraganaData and char not in katakanaData and char not in roman):
				if(char not in kanji_names):
					try:
						kanji = kanji_scrapper.kanji(char,'','','','')
						kanji_scrapper.seek(kanji,data)
						kanji_list.append(kanji)
						kanji_names.append(char)
					except:
						pass
						

	kanji_df = kanji_scrapper.load()
	
	tof = []
	for name in kanji_df.name:
		if(name in kanji_names):
			tof.append(True)
		else:
			tof.append(False)

	is_there = pd.Series(tof)
	kanji_df = kanji_df[is_there]

	return results(kanji_df,kanji_list)


#text = '私は子供です。だから、お菓子を食べてが好き！'
#x = analyse_text(text)

#print(x.df.grade.value_counts(normalize=True))





