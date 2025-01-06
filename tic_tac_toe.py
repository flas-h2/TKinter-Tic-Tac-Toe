#TJ Szoszorek
from tkinter import *
import random

wins = 0
losses = 0
ties = 0

def update_player_image():
    choice_value = radio_value.get()
    if choice_value == "Rock":
        user_move_photo.config(image=logos["Rock"])
        computer_move_photo.config(image=logos["TBD"])
    elif choice_value == "Paper":
        user_move_photo.config(image=logos["Paper"])
        computer_move_photo.config(image=logos["TBD"])
    elif choice_value == "Scissors":
        user_move_photo.config(image=logos["Scissors"])
        computer_move_photo.config(image=logos["TBD"])

def play():
    global wins, losses, ties
    computer_choice = random.choice(["Rock", "Paper", "Scissors"])
    computer_move_photo.config(image=logos[computer_choice])
    
    player_choice = radio_value.get()

    if player_choice == computer_choice:
        outcome = "Tied"
        ties += 1
    elif player_choice == "Rock" and computer_choice == "Scissors":
        outcome = "Win"
        wins += 1
    elif player_choice == "Paper" and computer_choice == "Rock":
        outcome = "Win"
        wins += 1
    elif player_choice == "Scissors" and computer_choice == "Paper":
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
    user_move_photo.config(image=logos["TBD"])
    computer_move_photo.config(image=logos["TBD"])
        

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
    "Rock": PhotoImage(file=r".\resources\rock.png"),
    "Paper": PhotoImage(file=r".\resources\paper.png"),
    "Scissors": PhotoImage(file=r".\resources\scissors.png"),
    "TBD": PhotoImage(file=r".\resources\tbd.png")
}


radio_value = StringVar(value="TBD")


rock = Radiobutton(window, text="Rock", variable=radio_value, value='Rock', command=update_player_image)
paper = Radiobutton(window, text="Paper", variable=radio_value, value='Paper', command=update_player_image)
scissors = Radiobutton(window, text="Scissors", variable=radio_value, value='Scissors', command=update_player_image)

rock.grid(row=0, column=0)
paper.grid(row=0, column=1)
scissors.grid(row=0, column=2)


user_move_photo = Label(window, image= logos["TBD"])
vs_label = Label(window, text="VS", font=("Arial", 14))
computer_move_photo = Label(window, image=logos["TBD"])

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


window.mainloop()