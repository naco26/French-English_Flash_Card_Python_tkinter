#-------------------------------IMPORTS-----------------------------
from tkinter import *
import random
import pandas
#------------------------------CONSTANTS-----------------------------
BACKGROUND_COLOR = "#B1DDC6"
FONT_TITLE = ("Arial",40,"italic")
FONT_WORD = ("Arial",60,"bold")
WAIT_PERIOD=10000
DATA_LENGTH=1000
reveal_timer = None
to_learn={}
current_card={}
#--------------------------------Language Dat-------------------------
try:
    data = pandas.read_csv("data\wordsLearned.csv")
except FileNotFoundError:
    print("in exception")
    data =  pandas.read_csv("data\/french_words.csv")
finally:
    to_learn = data.to_dict(orient="records")
    DATA_LENGTH = len(data)-1


#------------------------------METHODS FOR BUTTONS------------------
def DoesNotKnow():
    nextFrenchWord()

def KnowWord():
    global DATA_LENGTH,current_card
    try:
        to_learn.remove(current_card)
    except ValueError:
        print("All words learned!")
    else:
        new_data = pandas.DataFrame(to_learn)
        new_data.to_csv("data\wordsLearned.csv",index=False)
        DATA_LENGTH = len(new_data)-1
        nextFrenchWord()

#------------------------------RANDOM WORD PICKER-----------------------
def nextFrenchWord():
    global current_card
    global reveal_timer,DATA_LENGTH
    window.after_cancel(reveal_timer)
    current_card = random.choice(to_learn)
    canvas.itemconfig(flash_Card,image=card_front_img)
    canvas.itemconfig(word,text=f"{current_card["French"]}",fill="black")
    canvas.itemconfig(title,text="French",fill="black")
    reveal_timer = window.after(WAIT_PERIOD,RevealTranslation)

#--------------------------Show Translation---------------------------
def RevealTranslation():
    global current_card
    global reveal_timer
    canvas.itemconfig(flash_Card,image=card_back_img)
    canvas.itemconfig(title,text="English",fill="white")
    canvas.itemconfig(word,text=f"{current_card["English"]}",fill="white")


#-------------------------------UI--------------------------------------
window = Tk()
window.title("English-French Flash Card")
window.config(padx=50,pady=50,bg=BACKGROUND_COLOR)
reveal_timer = window.after(WAIT_PERIOD,RevealTranslation)

card_front_img = PhotoImage(file="images\card_front.png")
card_back_img = PhotoImage(file="images\card_back.png")
correct_img = PhotoImage(file="images\/right.png")
wrong_img = PhotoImage(file="images\wrong.png")

canvas = Canvas(height=526,width=800,bg=BACKGROUND_COLOR,highlightthickness=0)
flash_Card = canvas.create_image(400,263,image=card_front_img)
title = canvas.create_text(400,150,font=FONT_TITLE)
word = canvas.create_text(400,263,font=FONT_WORD)
canvas.grid(row=0,column=0,columnspan=2)

nextFrenchWord()

#correct button
correct_button = Button(image=correct_img,highlightthickness=0,command=KnowWord)
correct_button.grid(row=1,column=1)

#wrong button
wrong_button = Button(image=wrong_img,highlightthickness=0,command=DoesNotKnow)
wrong_button.grid(row=1,column=0)


window.mainloop()