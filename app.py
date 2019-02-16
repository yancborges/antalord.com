################################################################################################################################################
################################################################################################################################################ IMPORTING
################################################################################################################################################

from flask import Flask, flash, request, render_template, redirect, url_for, session, logging
from wtforms import Form, RadioField, validators, IntegerField, widgets, SelectMultipleField, SelectField, TextAreaField
from random import shuffle
import json
import main_splitter

################################################################################################################################################
################################################################################################################################################ CONFIG
################################################################################################################################################

app = Flask(__name__)
app.secret_key='hiddenpass'

################################################################################################################################################
################################################################################################################################################ CONSTANTS
################################################################################################################################################

DIEGAO = 3730
JOAO_ZIKA = DIEGAO/2

################################################################################################################################################
################################################################################################################################################ LOCAL DATA
################################################################################################################################################

LANGS = (
		('Python',int(75),'F','python.png'),
		('C#',int(60),'N','cs.png'),
		('Java',int(30),'N','java.png'),
		('C',int(20),'N','c.png'),
		('Php',int(5),'N','php.png')
		)

DBS = (
		('MySql',int(80),'N','mysql.png'),
		('Oracle',int(0),'N','oracle.png')
		)

FRAMEWORKS = (
		('Flask',int(75),'F','flask.png'),
		('Bootstrap',int(40),'N','bootstrap.png'),
		('Django',int(5),'N','django.png'),
		('Angular', int(0),'N','angular.png')
	)

################################################################################################################################################
################################################################################################################################################ FUNCTIONS
################################################################################################################################################

def read_db():
	file_json = open('db.json', 'r')
	data = json.load(file_json)
	myth_data = data['myths']

	return myth_data

def get_myth(name):

	m = read_db()
	result = None

	for i in m:
		if( i['name'].lower() == name.lower() ):
			result = i
			break

	return result

def get_gen():
	file_json = open('generations.json', 'r')
	data = json.load(file_json)
	
	gen_table = []
	file_json.close()
	for gen in data['generations']:
		gen_table.append((gen['ID'],gen['Name']))
	return gen_table

def get_genID(value):
	file_json = open('generations.json', 'r')
	data = json.load(file_json)
	
	gen_table = []
	file_json.close()
	for gen in data['generations']:
		if(gen["ID"] == value):
			return gen

################################################################################################################################################
################################################################################################################################################ CLASSES
################################################################################################################################################

class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()

class form_conversor(Form):
	value = IntegerField( 'Value:', [validators.DataRequired()])
	options = MultiCheckboxField( '', [validators.DataRequired()], choices=[('d','Diegão'),('j','João Zika')])

class form_pokemon(Form):
	gen_db = get_gen()
	gen = SelectField( 'Generation wanted: ', [validators.DataRequired()], choices=gen_db )

class form_japanese(Form):
	text = TextAreaField( 'Input text: ', [validators.DataRequired()])

################################################################################################################################################
################################################################################################################################################ ROUTES
################################################################################################################################################

@app.route('/')
def index():
    return render_template("path.html")

@app.route('/work')
def work():

	langs_f = LANGS
	dbs_f = DBS
	fw_f = FRAMEWORKS

	return render_template('work.html', langs=langs_f, dbs=dbs_f, fw=fw_f)

@app.route('/fun')
def fun():
	return render_template('fun.html')

@app.route('/apps')
def apps():
	return render_template('apps.html')

@app.route('/apps/conversor', methods=['GET', 'POST'])
def conversor():
	form = form_conversor(request.form)
	result = None
	if( request.method == 'GET'):
		form.options.data = "d"
	elif( request.method == 'POST' and form.validate() ):
		result = []
		if('d' in form.options.data):
			result.append((form.value.data/DIEGAO))
		else:
			result.append(None)
		if('j' in form.options.data):
			result.append((form.value.data/JOAO_ZIKA))
		else:
			result.append(None)

	return render_template('conversor.html', form=form, result=result)

@app.route('/myths')
def myths():

	m = read_db()
	return render_template('myth-index.html', m=m)

@app.route('/myths/<string:name>')
def myth(name):

	myth_info = get_myth(name)
	if(myth_info):
		return render_template('myth-layout.html', m=myth_info)
	else:
		flash("Ops! this myth is not ready yet! While we work in it, why don't you check your written myths below?", 'alert-warning alert')
		return redirect(url_for('myths'))

@app.route('/maintenance')
def maintenance():
	return render_template('maintenance.html')

@app.route('/noobs')
def noobs():
	return render_template('noobs.html')

@app.route('/apps/poke-gen', methods=['GET', 'POST'])
def poke_gen():
	
	form = form_pokemon(request.form)
	all_poke = None

	if(request.method == "POST"):
		all_pokeData = get_genID(form.gen.data)
		img_link = all_pokeData["Link"]	
		shuffle(all_pokeData["Pokemons"])
		all_poke = all_pokeData["Pokemons"]
		return render_template('poke-gen.html', form=form,all_poke=all_poke,img_link=img_link)
	else:
		return render_template('poke-gen.html', form=form,all_poke=all_poke)

@app.route('/apps/japanese', methods=['GET','POST'])
def japanese_tool():
	
	results = None
	form = form_japanese(request.form)

	if(request.method == "POST" and form.validate()):

		results = main_splitter.analyse_text(form.text.data)

	return render_template('japanese_tool.html',form=form,results=results)

################################################################################################################################################
################################################################################################################################################ HANDLERS
################################################################################################################################################

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html')

################################################################################################################################################
################################################################################################################################################ MAIN RUN
################################################################################################################################################

if __name__ == '__main__':
    app.secret_key='hiddenpass'
    app.run(debug=True)
