from tkinter import *
import pandas as pd
import random

BACKGROUND_COLOR = "#B1DDC6"
current_card = {}
to_words = {}


def change_word():
    global current_card
    global timer
    window.after_cancel(timer)
    current_card = random.choice(to_words)
    french_word = current_card["French"]
    canvas.itemconfig(front, image=card_front)
    canvas.itemconfig(card_title, text="French", fill="black")
    canvas.itemconfig(card_word, text=french_word, fill="black")
    window.after(3000, func=flip_card)


def flip_card():
    canvas.itemconfig(front, image=new_image)
    english_word = current_card["English"]
    canvas.itemconfig(card_title, text="English", fill="white")
    canvas.itemconfig(card_word, text=english_word, fill="white")


def is_known():
    to_words.remove(current_card)
    change_word()
    data = pd.DataFrame(to_words)
    data.to_csv("data/words_to_learn.csv", index=False)


window = Tk()
window.title("Flash Card")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)
timer = window.after(3000, func=flip_card)

new_image = PhotoImage(file="images/card_back.png")
card_front = PhotoImage(file="images/card_front.png")
try:
    df = pd.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    original_data = pd.read_csv("data/french_words.csv")
    to_words = original_data.to_dict(orient="records")
else:
    to_words = df.to_dict(orient="records")


canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
front = canvas.create_image(400, 263, image=card_front)
canvas.grid(row=0, column=0, columnspan=2)
card_title = canvas.create_text(400, 150, text="French", font=("Ariel", 40, "italic"))
card_word = canvas.create_text(400, 263, text="data", font=("Ariel", 60, "bold"))

wrong = PhotoImage(file="images/wrong.png")
btn_wrong = Button(image=wrong, highlightthickness=0, command=change_word)
btn_wrong.grid(row=1, column=0)

right = PhotoImage(file="images/right.png")
btn_right = Button(image=right, highlightthickness=0, command=is_known)
btn_right.grid(row=1, column=1)

change_word()

window.mainloop()
