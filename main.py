import random
from tkinter import *
from tkinter import messagebox

import pandas
current_card = {}
to_learn = {}


try:
    data = pandas.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    original_data = pandas.read_csv("data/spanishFreqWords.csv")
    to_learn = original_data.to_dict(orient="records")
else:
    to_learn = data.to_dict(orient="records")


def get_word():
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    if len(to_learn) == 0:
        messagebox.showinfo(title="All done", message="You have learned all the words!")
        return
    current_card = random.choice(to_learn)
    canvas.itemconfig(card_image, image=card_front_img)
    canvas.itemconfig(card_title, text="Spanish", fill="black")
    canvas.itemconfig(card_word, text=current_card["Spanish"], fill="black")
    flip_timer = window.after(3000, func=flip_card)


def flip_card():
    canvas.itemconfig(card_title, text="English", fill="white")
    canvas.itemconfig(card_word, text=current_card["English"], fill="white")
    canvas.itemconfig(card_image, image=card_back_img)


def is_known():
    to_learn.remove(current_card)
    data = pandas.DataFrame(to_learn)
    data.to_csv("data/words_to_learn.csv", index=False)
    get_word()

BACKGROUND_COLOR = "#B1DDC6"
window = Tk()
window.title("Spanish Flash Cards")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

flip_timer = window.after(3000, func=flip_card)

canvas = Canvas(width=800, height=526)

card_front_img = PhotoImage(file="images/card_front.png")
card_back_img = PhotoImage(file="images/card_back.png")
card_image = canvas.create_image(400, 263, image=card_front_img)
card_title = canvas.create_text(400,  150, text="", font=("Arial", 40, "italic"), fill="black")
card_word = canvas.create_text(400, 263, text="",font=("Arial", 60, "bold") , fill="black")
canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)
canvas.grid(column=0,row=0, columnspan=2)

wrong_img = PhotoImage(file="images/wrong.png")
unknown_button = Button(image=wrong_img,highlightthickness=0, command=get_word)
unknown_button.grid(column=0, row=1)

check_img = PhotoImage(file="images/right.png")
known_button = Button(image=check_img,highlightthickness=0,command=is_known)
known_button.grid(column=1, row=1)

get_word()


window.mainloop()