import os
from tkinter import *
from tkinter import filedialog
import tkinter.scrolledtext as st
import rps_player as rps_plr
import itertools

class RPSTourney:

    def tourny(self):
        for i in itertools.combinations(self.players, 2):
            print(i[0].name, i[1].name)

    def __init__(self, window):
        self.players = []

        frame = Frame(window, borderwidth=2, relief="solid", padx=20, pady=20)
        frame.pack()

        select_folder_btn = Button(frame, text="Select Folder", command=self.select_folder)
        select_folder_btn.grid(row=0, column=1)

        select_file_btn = Button(frame, text="Select File", command=self.select_file)
        select_file_btn.grid(row=0, column=2, padx=6)

        run_tournament_btn = Button(frame, text="Run Tournament")
        run_tournament_btn.grid(row=0, column=3, padx=6)

        speed_label = Label(frame, text="Speed")
        speed_label.grid(row=1, column=1)

        speed_scale = Scale(frame, from_=0, to_=100, tickinterval=.05, orient="horizontal", length=100, showvalue=False)
        speed_scale.grid(row=1, column=2, pady=20)

        image_frame = Frame(window, borderwidth=2, relief="solid")
        image_frame.pack(padx=20, pady=20)

        placeholder1 = Label(image_frame, text="placeholder")
        placeholder1.pack()

        plr_vs_frame = Frame(window, borderwidth=2, relief="solid")
        plr_vs_frame.pack(padx=20, pady=20)

        placeholder2 = Label(plr_vs_frame, text="placeholder")
        placeholder2.pack()

        self.console = st.ScrolledText(window, state="disabled", font=("Courier", 10))
        self.console.pack()

        self.default_folder = "path_to_default_folder"
        if os.path.exists(self.default_folder):
            self.load_players(self.default_folder, is_folder=True)
        
    def add_image(self):
        pass

    def select_folder(self):
        directory = filedialog.askdirectory()
        if directory:
            self.load_players(directory, is_folder=True)

    def select_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("MRPS Files", "*.mrps")])
        if file_path:
            self.load_players(file_path, is_folder=False)

    def load_players(self, path, is_folder):
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

    def print_message(self, message):
        self.console.config(state="normal")
        self.console.delete(1.0, END)
        self.console.insert(END, f"{message}\n")
        self.console.config(state="disabled")

if __name__ == "__main__":
    window = Tk()
    RPSTourney(window=window)
    window.geometry("600x600")
    window.mainloop()
