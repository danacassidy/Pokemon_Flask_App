from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired



import csv

def convert_to_dict(filename):
    """
    Convert a CSV file to a list of Python dictionaries
    """
    # open a CSV file - note - must have column headings in top row
    datafile = open(filename, newline='', encoding="utf-8")

    # create DictReader object
    my_reader = csv.DictReader(datafile)

    # create a regular Python list containing dicts
    list_of_dicts = list(my_reader)

    # close original csv file
    datafile.close()

    # return the list
    return list_of_dicts





# run tryouts
if __name__ == '__main__':
    pokemon_list = convert_to_dict("pokemon.csv")


app = Flask(__name__)
application = app


Bootstrap(app)
app.config['SECRET_KEY'] = 'Pokemon'


# create a list of dicts from a CSV
pokemon_list = convert_to_dict("pokemon.csv")



pairs_list = []
for p in pokemon_list:
    pairs_list.append((p['name'],p['image'], p['pokedex_number']))

def get_names(source):
    names = []
    for row in source:
        # lowercase all the names for better searching
        name = row["name"].lower()
        names.append(name)
    return sorted(names)
   

def get_id(source, name):
    for row in source:
        # lower() makes the string all lowercase
        if name.lower() == row["name"].lower():
            id = row["pokedex_number"]
            # change number to string
            id = str(id)
            # return id if name is valid
            return id
    # return these if id is not valid - not a great solution, but simple
    return "Unknown"
# first route

class NameForm(FlaskForm):
    name = StringField('Which pokemon do you want to see?', validators=[DataRequired()])
    submit = SubmitField('Submit')
 
@app.route('/')
def index():
    return render_template('index.html', pairs=pairs_list, the_title="Pokemon Index")

# second route

@app.route('/pokemon/<num>')
def detail(num):
    try:
        poke_dict = pokemon_list[int(num) - 1]
    except:
        return f"<h1>Invalid value for Pokemon</h1>"

    # a little bonus function, imported on line 2 above
    return render_template('pokemon.html', poke=poke_dict, ord=ord, the_title=poke_dict['name'])

@app.route('/search', methods=['GET', 'POST'])
def search():
    names = get_names(pokemon_list)
    # you must tell the variable 'form' what you named the class, above
    # 'form' is the variable name used in this template: index.html
    form = NameForm()
    message = ""
    if form.validate_on_submit():
        name = form.name.data
        if name.lower() in names:
            # empty the form field
            form.name.data = ""
            id = get_id(pokemon_list, name)
            # redirect the browser to another route and template
            return redirect(url_for("detail", num =id) )
        else:
            message = "That pokemon does not exist. If you're sure it does, double-check your spelling. "
    return render_template('search.html', names=names, form=form, message=message)

# keep this as is
if __name__ == '__main__':
    app.run(debug=True)
