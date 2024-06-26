import pickle

class Statistics:
    def __init__(self):
        self.stats_file = "statistics.pkl"
        self.games_played = 0
        self.total_moves = 0
        self.best_time = float('inf')
        self.player_stats = {}
        self.load_stats()

    def load_stats(self):
        try:
            with open(self.stats_file, "rb") as f:
                stats = pickle.load(f)
                self.games_played = stats["games_played"]
                self.total_moves = stats["total_moves"]
                self.best_time = stats["best_time"]
                self.player_stats = stats["player_stats"]
        except (FileNotFoundError, EOFError):
            self.save_stats()

    def save_stats(self):
        with open(self.stats_file, "wb") as f:
            stats = {
                "games_played": self.games_played,
                "total_moves": self.total_moves,
                "best_time": self.best_time,
                "player_stats": self.player_stats
            }
            pickle.dump(stats, f)

    def update_player_stats(self, player_name, moves, time):
        if player_name not in self.player_stats:
            self.player_stats[player_name] = {
                "games_played": 0,
                "total_moves": 0,
                "best_time": float('inf')
            }

        self.player_stats[player_name]["games_played"] += 1
        self.player_stats[player_name]["total_moves"] += moves
        if time < self.player_stats[player_name]["best_time"]:
            self.player_stats[player_name]["best_time"] = time

        self.save_stats()
