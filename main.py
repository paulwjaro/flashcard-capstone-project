from tkinter import *
import pandas
import random


BACKGROUND_COLOR = "#B1DDC6"
FRENCH = 0
ENGLISH = 1
LANGUAGES = ("French", "English")
COLORS = ("black", "white")

# -- Set Up Language Data
try:
    language_data = pandas.read_csv("./data/words_to_learn.csv")
except FileNotFoundError:
    language_data = pandas.read_csv("./data/french_words.csv")
    print("Using Default List")
finally:
    f_list = language_data["French"].tolist()
    e_list = language_data["English"].tolist()

word_list = []
current_language = FRENCH
card_language = LANGUAGES[current_language]
current_word = 0

for word in range(len(f_list)):
    new_word = (f_list[word], e_list[word])
    word_list.append(new_word)

random.shuffle(word_list)


def set_card():
    canvas.itemconfig(title_text, text=LANGUAGES[current_language], fill=COLORS[current_language])
    canvas.itemconfig(word_text, text=word_list[current_word][current_language], fill=COLORS[current_language])
    canvas.itemconfig(card, image=card_sides[current_language])


# -- Create a Timer to Change the Card Language
def flip_card():
    global current_language
    if current_language == FRENCH:
        current_language = ENGLISH
        set_card()
    else:
        current_language = FRENCH
        set_card()


# -- Change Word on Card
def change_word():
    global current_word, word_text, flip_timer
    if current_language == ENGLISH:
        window.after_cancel(flip_timer)
        current_word += 1
        if current_word < len(word_list):
            flip_card()
            flip_timer = window.after(3000, flip_card)
        else:
            current_word = 0
            random.shuffle(word_list)
            flip_card()
            flip_timer = window.after(3000, flip_card)
    else:
        window.after_cancel(flip_timer)
        flip_card()


def word_learnt():
    global current_language, current_word
    current_language = ENGLISH
    word_list.pop(current_word)
    change_word()


# -- Set Up Window
window = Tk()
window.config(background=BACKGROUND_COLOR, padx=50, pady=50)
window.title("Flash French")

flip_timer = window.after(3000, flip_card)
# -- Create UI --

# - Create Images
card_sides = (PhotoImage(file="./images/card_front.png"), PhotoImage(file="./images/card_back.png"))
right = PhotoImage(file="./images/right.png")
wrong = PhotoImage(file="./images/wrong.png")

# - Create Canvas
canvas = Canvas()
canvas.config(width=800, height=528, bg=BACKGROUND_COLOR, highlightthickness=0)
card = canvas.create_image(400, 264, image=card_sides[current_language])
canvas.grid(row=0, column=0, columnspan=2)
title_text = canvas.create_text(400, 150, text=card_language, font=("arial", 40, "italic"))
word_text = canvas.create_text(400, 263, text=word_list[current_word][current_language], font=("arial", 50, "bold"))

# - Create Buttons
right_button = Button(image=right, highlightthickness=0, command=word_learnt)
right_button.grid(row=1, column=1)

wrong_button = Button(image=wrong, highlightthickness=0, command=change_word)
wrong_button.grid(row=1, column=0)

window.mainloop()

words_to_learn = pandas.DataFrame(word_list)
words_to_learn.columns = ["French", "English"]
words_to_learn.to_csv("./data/words_to_learn.csv", index=False)
