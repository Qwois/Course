import os
import pickle

class Statistics:
    def __init__(self):
        self.stats_file = "stats.dat"
        self.games_played = 0
        self.total_moves = 0
        self.best_time = float('inf')
        self.load_stats()

    def load_stats(self):
        if os.path.exists(self.stats_file):
            with open(self.stats_file, "rb") as f:
                stats = pickle.load(f)
                self.games_played = stats.get("games_played", 0)
                self.total_moves = stats.get("total_moves", 0)
                self.best_time = stats.get("best_time", float('inf'))
        else:
            self.save_stats()

    def save_stats(self):
        with open(self.stats_file, "wb") as f:
            stats = {
                "games_played": self.games_played,
                "total_moves": self.total_moves,
                "best_time": self.best_time,
            }
            pickle.dump(stats, f)

    def update(self, moves, time_taken=float('inf')):
        self.games_played += 1
        self.total_moves += moves
        if time_taken < self.best_time:
            self.best_time = time_taken
        self.save_stats()
