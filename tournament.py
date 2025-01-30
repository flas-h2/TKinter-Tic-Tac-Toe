import os
from tkinter import *
from tkinter import filedialog
import tkinter.scrolledtext as st
import itertools
import rps_player as rps_plr
import utilities as util


class RPSTourney:
    def __init__(self, window):
        self.players = []
        self.images = {}
        self.default_folder = r"C:\Users\CMP_ToSzoszorek\Downloads\random_rps_files"
        self.window = window

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
            self.console.insert(END, f"score: 0.0 series_wins: 0\n")

        self.console.config(state="disabled")

    def run_tournament(self):
        if len(self.players) < 2:
            self.match_info_label.config(text="Not enough players for a tournament!")
            return

        self.console.config(state="normal")
        self.console.delete(1.0, END)

        player_pairs = list(itertools.combinations(self.players, 2))

        for player1, player2 in player_pairs:
            matchup = f"{player1.name} vs {player2.name}"
            self.match_info_label.config(text=matchup)
            self.console.insert(END, matchup + "\n")
            self.console.update()

            player1_wins = 0
            player2_wins = 0
            ties = 0

            for i in range(min(len(player1.plays), len(player2.plays))):
                p1_move = util.convert_to_play(player1.plays[i])  # Convert shorthand
                p2_move = util.convert_to_play(player2.plays[i])  # Convert shorthand
                
                winner = util.determine_winner(p1_move.lower(), p2_move.lower())

                if winner == 1:
                    player1_wins += 1
                    player1.wins += 1
                    player2.losses += 1
                    round_result = f"{player1.name} wins"
                elif winner == -1:
                    player2_wins += 1
                    player2.wins += 1
                    player1.losses += 1
                    round_result = f"{player2.name} wins"
                else:
                    ties += 1
                    player1.ties += 1
                    player2.ties += 1
                    round_result = "Tie"

                round_output = f"Round {i+1}: {player1.name} ({p1_move}) vs {player2.name} ({p2_move}) - {round_result}\n"
                self.console.insert(END, round_output)
                self.console.update()

                self.player1_image_label.config(image=self.images[player1.plays[i]])
                self.player2_image_label.config(image=self.images[player2.plays[i]])
                self.match_result_label.config(text=round_result)

                self.match_info_label.update()
                self.console.update()
                self.match_result_label.update()
                self.window.after(1000 // max(1, self.speed_scale.get()))

            if player1_wins > player2_wins:
                match_winner = f"{player1.name} wins the match!"
                player1.series_wins += 1
            elif player2_wins > player1_wins:
                match_winner = f"{player2.name} wins the match!"
                player2.series_wins += 1
            else:
                match_winner = "Match is a tie!"

            self.console.insert(END, match_winner + "\n\n")
            self.console.update()

        self.print_final_results()
        self.console.config(state="disabled")
        self.match_info_label.config(text="Tournament Complete!")

    def print_final_results(self):
        self.console.insert(END, "\nFinal Tournament Results:\n\n")
        max_wins = max(player.wins for player in self.players)
        max_score = max(player.calculate_score() for player in self.players)
        max_series_wins = max(player.series_wins for player in self.players)

        most_wins = [player.name for player in self.players if player.wins == max_wins]
        highest_score = [player.name for player in self.players if player.calculate_score() == max_score]
        most_series_wins = [player.name for player in self.players if player.series_wins == max_series_wins]

        for player in self.players:
            self.console.insert(END, f"{player.name}: plays: {player.plays} wins: {player.wins} losses: {player.losses} ties: {player.ties}\nscore: {player.calculate_score()} series_wins: {player.series_wins}\n\n")

        self.console.insert(END, f"{', '.join(most_wins)} had the most wins! ({max_wins})\n")
        self.console.insert(END, f"{', '.join(highest_score)} had the highest score! ({max_score})\n")
        self.console.insert(END, f"{', '.join(most_series_wins)} won the most series! ({max_series_wins})\n")
        self.console.config(state="disabled")


if __name__ == "__main__":
    window = Tk()
    RPSTourney(window=window)
    window.geometry("600x600")
    window.mainloop()