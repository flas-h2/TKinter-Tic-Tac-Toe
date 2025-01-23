def determine_winner(plr1, plr2):
    if plr1 == plr2:
        return 0
    elif plr1 == "rock" and plr2 == "paper":
        return -1
    elif plr1 == "rock" and plr2 == "scissors":
        return 1
    elif plr1 == "sciccors" and plr2 == "paper":
        return 1
    elif plr1 == "sciccors" and plr2 == "rock":
        return -1
    elif plr1 == "paper" and plr2 == "scissors":
        return -1
    elif plr1 == "paper" and plr2 == "rock":
        return 1
    
def convert_to_play(p:str):
    if p == "r":
        return "Rock"
    elif p == "p":
        return "Paper"
    elif p == "s":
        return "Scissors"
