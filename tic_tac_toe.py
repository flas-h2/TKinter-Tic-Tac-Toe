#TJ Szoszorek
from tkinter import *
import random
import tournament as mod

wins = 0
losses = 0
ties = 0

def torunament():
    mod.RPSTourney(window=Toplevel(window))

def update_player_image():
    choice_value = radio_value.get()
    if choice_value == "rock":
        user_move_photo.config(image=logos["rock"])
        computer_move_photo.config(image=logos["tbd"])
    elif choice_value == "paper":
        user_move_photo.config(image=logos["paper"])
        computer_move_photo.config(image=logos["tbd"])
    elif choice_value == "scissors":
        user_move_photo.config(image=logos["scissors"])
        computer_move_photo.config(image=logos["tbd"])

def play():
    global wins, losses, ties
    computer_choice = random.choice(["rock", "paper", "scissors"])
    computer_move_photo.config(image=logos[computer_choice])
    
    player_choice = radio_value.get()

    if player_choice == computer_choice:
        outcome = "Tied"
        ties += 1
    elif player_choice == "rock" and computer_choice == "scissors":
        outcome = "Win"
        wins += 1
    elif player_choice == "paper" and computer_choice == "rock":
        outcome = "Win"
        wins += 1
    elif player_choice == "scissors" and computer_choice == "paper":
        outcome = "Win"
        wins += 1
    else:
        outcome = "Lose"
        losses += 1

    score_label.config(text=f"Wins: {wins}  Losses: {losses}  Ties: {ties}")

    move_label.config(text=f"You {outcome}!")

def reset():
    global wins, losses, ties
    wins == 0
    losses == 0
    ties == 0

    score_label.config(text=f"Wins: 0  Losses: 0  Ties: 0")
    move_label.config(text="Make Your Move!")
    user_move_photo.config(image=logos["tbd"])
    computer_move_photo.config(image=logos["tbd"])
        

root = Tk()
root.title("Rock, Paper, Scissors")
root.geometry("400x400")
root.columnconfigure(0, weight=1)
window = Frame(root)
window.grid(row=0,column=0)

window.grid_columnconfigure(0, weight=1)
window.grid_columnconfigure(1, weight=1)
window.grid_columnconfigure(2, weight=1)


logos = {
    "rock": PhotoImage(file=r".\resources\rock.png"),
    "paper": PhotoImage(file=r".\resources\paper.png"),
    "scissors": PhotoImage(file=r".\resources\scissors.png"),
    "tbd": PhotoImage(file=r".\resources\tbd.png")
}


radio_value = StringVar(value="tbd")


rock = Radiobutton(window, text="Rock", variable=radio_value, value='rock', command=update_player_image)
paper = Radiobutton(window, text="Paper", variable=radio_value, value='paper', command=update_player_image)
scissors = Radiobutton(window, text="Scissors", variable=radio_value, value='scissors', command=update_player_image)

rock.grid(row=0, column=0)
paper.grid(row=0, column=1)
scissors.grid(row=0, column=2)


user_move_photo = Label(window, image= logos["tbd"])
vs_label = Label(window, text="VS", font=("Arial", 14))
computer_move_photo = Label(window, image=logos["tbd"])

user_move_photo.grid(row=1, column=0)
vs_label.grid(row=1, column=1)
computer_move_photo.grid(row=1, column=2)


move_label = Label(window, text="Make Your Move!", font=("Arial", 16, "bold"))
move_label.grid(row=2, column=0, columnspan=3)


score_label = Label(window, text="Wins: 0  Losses: 0  Ties: 0", font=("Arial", 12))
score_label.grid(row=3, column=0, columnspan=3)


play_button = Button(window, text="Play", width=10, command=play)
reset_button = Button(window, text="Reset Scores", width=15, command=reset)

play_button.grid(row=4, column=0, columnspan=1, pady=10)
reset_button.grid(row=4, column=2, columnspan=1, pady=10)

top_level_menubar = Menu(root)
root.config(menu=top_level_menubar)

file_menu = Menu(top_level_menubar, tearoff=0)
top_level_menubar.add_cascade(label="Options", menu=file_menu)
file_menu.add_command(label="Tournament", command=torunament)


window.mainloop()