from flask import Flask, render_template, request, redirect, url_for
import json

FILENAME = 'qnotes.json'
app = Flask(__name__)


def get_notes():
    notes = []
    try:
        with open(FILENAME, 'r') as file:
            notes = json.load(file)
    except FileNotFoundError:
        print('No notes found.')
        notes = []
    except Exception as err:
        print(f'Error: {err}, {type(err)}')
    return notes


@app.route('/')
def index():
    return render_template('index.html', notes=get_notes())


@app.route('/quicknotes/<int:note_id>', methods=['POST'])
def delete_note(note_id):
    command = request.form.get('command')
    if command == 'DELETE':
        notes = get_notes()
        del notes[note_id]
        save_notes(notes)
    return render_template('index.html', notes=get_notes())


@app.route('/quicknotes/', methods=['POST'])
def add_note():
    command = request.form.get('command')
    if command == 'ADD':
        note_text = request.form['note_text']
        note_color = request.form['note_color']
        notes = get_notes()
        notes.append({'text': note_text,
                      'color': note_color})
        save_notes(notes)
    return index()

def save_notes(notes):
    with open(FILENAME, 'w') as file:
        json.dump(notes, file, indent=4)


if __name__ == '__main__':
    app.run(debug=True)
