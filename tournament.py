import os
from tkinter import *
from tkinter import filedialog
import tkinter.scrolledtext as st
import itertools
import rps_player as rps_plr

class RPSTourney:
    def __init__(self, window):
        self.players = []
        self.images = {}
        self.default_folder = r"C:\Users\CMP_ToSzoszorek\Downloads\random_rps_files"

        frame = Frame(window, borderwidth=2, relief="solid", padx=20, pady=20)
        frame.pack()

        Button(frame, text="Select Folder", command=self.select_folder).grid(row=0, column=1)
        Button(frame, text="Select File", command=self.select_file_button).grid(row=0, column=2, padx=6)
        Button(frame, text="Run Tournament", command=self.run_tournament).grid(row=0, column=3, padx=6)

        Label(frame, text="Speed").grid(row=1, column=1)
        self.speed_scale = Scale(frame, from_=0, to_=100, orient="horizontal", showvalue=False)
        self.speed_scale.set(1)
        self.speed_scale.grid(row=1, column=2, pady=20)

        self.add_images(window)
        self.add_info(window)

        self.console = st.ScrolledText(window, state="disabled", font=("Courier", 10))
        self.console.pack()

    def add_images(self, window):
        self.images = {
            "r": PhotoImage(file=r".\resources\rock.png"),
            "p": PhotoImage(file=r".\resources\paper.png"),
            "s": PhotoImage(file=r".\resources\scissors.png"),
            "tbd": PhotoImage(file=r".\resources\tbd.png")
        }

        image_frame = Frame(window, borderwidth=2, relief="solid")
        image_frame.pack(padx=20, pady=20)

        self.player1_image_label = Label(image_frame, image=self.images["tbd"])
        self.player1_image_label.grid(row=0, column=0, padx=10)

        Label(image_frame, text="VS", font=("Arial", 16), padx=10).grid(row=0, column=1, padx=10)

        self.player2_image_label = Label(image_frame, image=self.images["tbd"])
        self.player2_image_label.grid(row=0, column=2, padx=10)

    def add_info(self, window):
        info_frame = Frame(window, borderwidth=2, relief="solid")
        info_frame.pack(padx=20, pady=20)

        self.match_info_label = Label(info_frame, text="Select players to start", font=("Arial", 14), fg="red")
        self.match_info_label.pack(pady=5)

        self.match_result_label = Label(info_frame, text="", font=("Arial", 12), fg="blue")
        self.match_result_label.pack(pady=5)

    def select_folder(self):
        folder_path = filedialog.askdirectory()
        if folder_path:
            self.load_players(folder_path, is_folder=True)

    def select_file_button(self):
        file_path = filedialog.askopenfilename(filetypes=[("MRPS Files", "*.mrps")])
        if file_path:
            self.load_players(file_path, is_folder=False)

    def load_players(self, path=None, is_folder=False):
        self.players.clear()

        files = [os.path.join(path, f) for f in os.listdir(path) if f.endswith(".rps")] if is_folder else [path]
        for file_path in files:
            with open(file_path, "r") as file:
                for line in file:
                    parts = line.strip().split(",")
                    if len(parts) >= 2:
                        name = parts[0]
                        plays = parts[1:]
                        self.players.append(rps_plr.RPSPlayer(name, plays))

        self.print_all_players()

    def print_all_players(self):
        self.console.config(state="normal")
        self.console.delete(1.0, END)

        for player in self.players:
            self.console.insert(END, f"{player.name}\n")
        self.console.insert(END, "\n")

        for player in self.players:
            plays_str = ", ".join([f"'{play}'" for play in player.plays])
            self.console.insert(END, f"{player.name}: plays: [{plays_str}] wins: 0 losses: 0 ties: 0\n")
            self.console.insert(END, f"score: 0.0 series_wins: 0\n\n")

        self.console.config(state="disabled")

    def run_tournament(self):
        if len(self.players) < 2:
            self.match_info_label.config(text="Not enough players for a tournament!")
            return

        self.console.config(state="normal")
        self.console.delete(1.0, END)

        player_pairs = list(itertools.combinations(self.players, 2))
        total_matches = len(player_pairs)
        self.current_match_index = 0  # Initialize the match index

        # Run the tournament loop (single function)
        while self.current_match_index < total_matches:
            player1, player2 = player_pairs[self.current_match_index]
            matchup = f"{player1.name} vs {player2.name}"

            # Update match info and console
            self.match_info_label.config(text=matchup)
            self.console.insert(END, matchup + "\n")
            self.console.update()

            # Get the moves from the players (just using the first move as an example)
            player1_move = player1.plays[0]  # Placeholder for first move
            player2_move = player2.plays[0]  # Placeholder for first move

            # Determine the winner directly within this loop
            if player1_move == player2_move:
                result = "Tie"
            elif (player1_move == "rock" and player2_move == "scissors") or \
                (player1_move == "scissors" and player2_move == "paper") or \
                (player1_move == "paper" and player2_move == "rock"):
                result = "Player 1 Wins"
            else:
                result = "Player 2 Wins"

            # Update the result label with the result
            self.match_result_label.config(text=f"{result} ({player1_move} vs {player2_move})")

            # Update player images based on moves (just an example)
            self.player1_image_label.config(image=self.images[player1_move])
            self.player2_image_label.config(image=self.images[player2_move])

            # Increase the match index
            self.current_match_index += 1

            # Wait for the user-defined speed before proceeding to the next match
            delay = 1000 // max(1, self.speed_scale.get())  # Delay based on speed scale
            self.match_info_label.update()
            self.console.update()
            self.match_result_label.update()

            # Simulate the wait between matches with after method
            window.after(delay)

        # After all matches, declare the tournament complete
        self.console.insert(END, "\nTournament Complete!\n")
        self.console.config(state="disabled")
        self.match_info_label.config(text="Tournament Complete!")


if __name__ == "__main__":
    window = Tk()
    RPSTourney(window=window)
    window.geometry("600x600")
    window.mainloop()
