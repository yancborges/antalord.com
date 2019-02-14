def hey(text, target, option, nrow, msg):
	with open(target ,option, encoding='utf8') as f:
		f.write(str(text))
		if(nrow == True):
			f.write('\n')
	if(msg == True):
		print('written to '+ target + ' file')