from flask import Flask, render_template, request, redirect, jsonify
import json
import os

app = Flask(__name__)

FLASHCARD_FILE = 'flashcards.json'

# Ensure flashcard JSON file exists and is valid
if not os.path.exists(FLASHCARD_FILE) or os.stat(FLASHCARD_FILE).st_size == 0:
    with open(FLASHCARD_FILE, 'w') as f:
        json.dump([], f)


def load_flashcards():
    """Load flashcards from the JSON file."""
    try:
        with open(FLASHCARD_FILE, 'r') as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return []


def save_flashcards(flashcards):
    """Save flashcards to the JSON file."""
    with open(FLASHCARD_FILE, 'w') as f:
        json.dump(flashcards, f, indent=4)


@app.route('/')
def index():
    flashcards = load_flashcards()
    return render_template('index.html', flashcards=flashcards)


@app.route('/add', methods=['POST'])
def add_flashcard():
    question = request.form['question']
    answer = request.form['answer']
    if question and answer:
        flashcards = load_flashcards()
        flashcards.append({'question': question, 'answer': answer})
        save_flashcards(flashcards)
    return redirect('/')


@app.route('/flashcards', methods=['GET'])
def get_flashcards():
    flashcards = load_flashcards()
    return jsonify(flashcards)


if __name__ == '__main__':
    app.run(debug=True)
