import os
from flask import Flask, render_template, request, redirect, url_for, render_template_string

from crud import Db

app = Flask(__name__, static_folder="static")
app.config.update(
    db=os.environ['POSTGRES_DB'],
    user=os.environ['POSTGRES_USER'],
    password=os.environ['POSTGRES_PASSWORD'],
    host=os.environ['POSTGRES_HOST'],
    port=os.environ['POSTGRES_PORT'],
)

db = Db(db=app.config['db'], user=app.config['user'], password=app.config['password'], host=app.config['host'], port=app.config['port'])
db.create_tables()


@app.route("/", methods=['GET', 'POST'])  # Главная страница
def index():
    return render_template('index.html', notes=db.get_notes_secure())


@app.route("/save_note_insecure", methods=['POST'])
def save_note_insecure():
    text = request.form['text']
    db.add_note_insecure(text)
    return redirect(url_for('index'))


@app.route("/save_note_secure", methods=['POST'])
def save_note_secure():
    text = request.form['text']
    db.add_note_secure(text)
    return redirect(url_for('index'))


@app.route("/notes/<int:id>", methods=['GET'])
def get_note(id):
    return render_template_string("<div>%s</div>" % db.get_note_secure(id))


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')



