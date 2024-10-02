import tkinter as tk
from tkinter import filedialog
import json
import functionality

def launch(model, gemini):
    screen = tk.Tk()
    colors = _get_colors()

    screen.geometry("1080x720")
    screen.title('TestSolve')
    screen.configure(bg=colors['bg'])
    screen.resizable(False, False)

    question = tk.Text(screen, width=10, height=1, borderwidth=0, highlightthickness=0, font=("Arial", 48), bg=colors['bg'], foreground=colors['header'])
    question.insert(tk.END, " TestSolve")
    question.configure(state=tk.DISABLED)
    question.pack(pady=50)

    question_box = tk.Text(screen, width=40, height=5, font=("Arial", 12), wrap="word", bg=colors['header'], fg=colors['bg'])
    question_box.place(x=350, y=200)
    question_box.delete('1.0', 'end')
    question_box.insert('1.0', 'question here...')

    options_box = tk.Text(screen, width=40, height=10, font=("Arial", 12), wrap="word", bg=colors['header'], fg=colors['bg'])
    options_box.place(x=350, y=350)
    options_box.delete('1.0', 'end')
    options_box.insert('1.0', 'options here...')

    answer_box = tk.Text(screen, width=40, height=5, font=("Arial", 12), wrap="word", bg=colors['header'], fg=colors['bg'])
    answer_box.place(x=350, y=590)
    answer_box.delete('1.0', 'end')
    answer_box.insert('1.0', 'answer will be there...')

    ask = tk.Button(screen, width=10, height=2, text='ask', command=lambda :answer_question(question_box, options_box, answer_box, model))
    ask.place(x=720, y=254)

    from_image = tk.Button(screen, width=20, height=2, text='upload from image', command=lambda :upload_question(question_box, options_box, model, gemini))
    from_image.place(x=196, y=254)

    return screen


def _get_colors():
    colors = {}

    with open('config.json', 'r') as f:
        config = json.load(f)

    if config['theme'] == 'dark':
        colors['bg'] = '#000000'
        colors['header'] = '#ffffff'
    elif config['theme'] == 'light':
        colors['bg'] = '#ffffff'
        colors['header'] = '#000000'

    return colors

def answer_question(question_box, option_box, answer_box, model):
    question = question_box.get('1.0', 'end-1c')
    options = option_box.get('1.0', 'end-1c').split('\n')

    result = functionality.answer(question, options, model)

    answer_box.delete('1.0', 'end')
    answer_box.insert('1.0', result)

def upload_question(question_box, options_box, model, gemini):
    file_path = filedialog.askopenfilename(
        title="Select a File",
        filetypes=(("Image files", "*.jpg;*.jpeg;*.png"), ("All files", "*.*"))  # Filter options
    )

    if file_path:
        media = gemini.upload_file(file_path)
        result = model.send_message([
            media,
            '\n\n',
            'only give me the text on the picture, no extra explanation'
        ]).text

        question = model.send_message('in this text, only give me the question, no further explaination: {}'.format(result)).text
        options = model.send_message('in this text, only give me the options, no further explaination: {}'.format(result)).text

        question_box.delete('1.0', 'end')
        question_box.insert('1.0', question)

        options_box.delete('1.0', 'end')
        options_box.insert('1.0', options)