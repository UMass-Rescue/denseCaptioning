from flask import Flask, render_template
# from werkzeug import secure_filename
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from werkzeug.utils import secure_filename
import os
from wtforms.validators import InputRequired
import subprocess

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ipsum' #to have form show in template for CSRF token that comes with the form
app.config['UPLOAD_FOLDER'] = 'imgs'

class UploadeFileForm(FlaskForm): #these var names are used in <form> in index.html
    file = FileField("File", validators=[InputRequired()])
    submit = SubmitField("Upload File")

@app.route('/', methods = ['GET', 'POST'])
@app.route('/home', methods = ['GET', 'POST'])
def home():
    form = UploadeFileForm()
    if form.validate_on_submit():
        file = form.file.data #First grab the file
        file.save(
            os.path.join(
                os.path.abspath(os.path.dirname(__file__)),
                app.config['UPLOAD_FOLDER'],
                secure_filename(file.filename)))
        zsh = ['th', './run_model.lua', '-gpu', '-1' , '-input_image', 'imgs/' + file.filename]
        result = subprocess.run(zsh, stdout = subprocess.PIPE, shell=True)
        return "File " + file.filename + " has been uploaded and processed"
    return render_template('index.html', form = form)

@app.route('/viewresults')
def view():
    return render_template('view_results_template.html')

if __name__ == '__main__':
    app.run(debug=True)
