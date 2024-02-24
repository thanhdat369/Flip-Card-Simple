from tkinter import *
from PIL import Image,ImageTk
import pandas
import random
from style import *

current_card = {}
to_learn = {}

data = pandas.read_csv("data/category.csv")
to_learn = data.to_dict(orient="records")

QUESTION = "Question"
DEFINE = "Define"

def next_card():
    global current_card
    current_card = random.choice(to_learn)
    canvas.itemconfig(card_title, text=QUESTION, fill=LIGHT_COLOR)
    canvas.itemconfig(card_word, text=current_card[QUESTION], fill=LIGHT_COLOR)

def is_known():
    to_learn.remove(current_card)
    data = pandas.DataFrame(to_learn)
    data.to_csv("words_to_learn.csv", index=False)
    next_card()


def flip_card():
    to_filp = DEFINE 
    title = canvas.itemcget(card_title, "text")
    if (title == DEFINE):
        to_filp = QUESTION 

    canvas.itemconfig(card_title, text=to_filp, fill=LIGHT_COLOR)
    canvas.itemconfig(card_word, text=current_card[to_filp], fill=LIGHT_COLOR)


def move_window(event):
    window.geometry('+{0}+{1}'.format(event.x_root, event.y_root))

window = Tk()
window.title("Flashy!")
window.config(padx=0, pady=0, bg=BACKGROUND_COLOR)
window.wm_attributes("-topmost", True)
window.overrideredirect(True)
window.resizable(False, False)

title_bar = Frame(window, bg='white', relief='raised', bd=2)

close_button = Button(title_bar, text='X', command=window.destroy)
move_button = Button(title_bar, text='<>')
title_bar.grid(column=4, row=1)
close_button.pack(side=RIGHT)
move_button.pack(side=LEFT)
move_button.bind('<B1-Motion>',move_window)
title_bar.bind('<B1-Motion>', move_window)

WIDTH = 150
HEIGH = WIDTH/2

FONT_SIZE = 16
TEXT_TITLE_POSITION = (WIDTH/2, 10)
TEXT_WORD_POSITION = (WIDTH/2, FONT_SIZE + TEXT_TITLE_POSITION[1] + 15)


canvas = Canvas(width=WIDTH, height=HEIGH)
card_title = canvas.create_text(
    TEXT_TITLE_POSITION[0], TEXT_TITLE_POSITION[1], text="", font=('Ariel', 10, 'italic'))
card_word = canvas.create_text(
    TEXT_WORD_POSITION[0], TEXT_WORD_POSITION[1], text="", font=("Ariel", FONT_SIZE, "bold"))

canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)

canvas.grid(row=0, column=0, columnspan=4)
# buttons
cross_image = ImageTk.PhotoImage(Image.open("images/wrong.png"))
unknown_button = Button(
    image=cross_image, highlightthickness=0, command=next_card,background="#000000")
unknown_button.grid(row=1, column=0)

flip_image = ImageTk.PhotoImage(Image.open("images/flip.png"))
r_image = Button(image=flip_image, highlightthickness=0, command=flip_card,background="#000000")
r_image.grid(column=1, row=1)

tick_image = ImageTk.PhotoImage(Image.open("images/right.png"))
r_image = Button(image=tick_image, highlightthickness=0, command=is_known,background="#000000")
r_image.grid(column=2, row=1)

next_card()
window.mainloop()
