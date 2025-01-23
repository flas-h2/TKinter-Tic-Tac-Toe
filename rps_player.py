class RPSPlayer:
    def __init__(self, name: str, plays: list):
        self.name = name
        self.plays = plays
        self.wins = 0
        self.losses = 0
        self.ties = 0
        self.series_wins = 0

    def calculate_score(self) -> float:
        """
        Calculates the player's score.
        1 point for every win, 0.5 points for every tie.
        """
        return self.wins + 0.5 * self.ties

    def __str__(self) -> str:
        """
        Returns a string representation of the player, including their name and plays.
        """
        return f"Player {self.name} with plays: {', '.join(self.plays)}"