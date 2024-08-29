import tkinter as tk
from tkinter import messagebox

class GameApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Game Points Calculator")

        self.kati_point = 0
        self.no_of_players = 0
        self.players = []
        self.seen_players = []
        self.unseen_players = []
        self.player_maal_dict = {}

        self.create_widgets()

    def create_widgets(self):
       
        tk.Label(self.root, text="How much Point game:").grid(row=0, column=0, padx=10, pady=10)
        self.kati_point_entry = tk.Entry(self.root)
        self.kati_point_entry.grid(row=0, column=1, padx=10, pady=10)

        tk.Label(self.root, text="Enter number of players:").grid(row=1, column=0, padx=10, pady=10)
        self.num_players_entry = tk.Entry(self.root)
        self.num_players_entry.grid(row=1, column=1, padx=10, pady=10)

        self.start_button = tk.Button(self.root, text="Start", command=self.setup_players)
        self.start_button.grid(row=2, column=0, columnspan=2, pady=20)

    def setup_players(self):
        try:
            self.kati_point = int(self.kati_point_entry.get())
            self.no_of_players = int(self.num_players_entry.get())
        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid numbers for points and number of players.")
            return

        if self.no_of_players <= 0:
            messagebox.showerror("Input Error", "Number of players must be greater than 0.")
            return

        self.players = []
        for widget in self.root.grid_slaves():
            widget.grid_forget()

        tk.Label(self.root, text="Enter player names:").grid(row=0, column=0, padx=10, pady=10)
        self.player_entries = [tk.Entry(self.root) for _ in range(self.no_of_players)]
        for i, entry in enumerate(self.player_entries):
            tk.Label(self.root, text=f"Player {i+1}:").grid(row=i+1, column=0, padx=10, pady=5)
            entry.grid(row=i+1, column=1, padx=10, pady=5)

        tk.Button(self.root, text="Submit Players", command=self.submit_players).grid(row=self.no_of_players+1, column=0, columnspan=2, pady=20)

    def submit_players(self):
        self.players = [entry.get().strip() for entry in self.player_entries if entry.get().strip()]
        if len(self.players) != self.no_of_players:
            messagebox.showerror("Input Error", "Please enter all player names.")
            return

        self.setup_seen_status()

    def setup_seen_status(self):
        for widget in self.root.grid_slaves():
            widget.grid_forget()

        tk.Label(self.root, text="Player Seen Status (Select Yes or No):").grid(row=0, column=0, padx=10, pady=10)
        self.seen_status_vars = {}
        for i, player in enumerate(self.players):
            tk.Label(self.root, text=f"{player}:").grid(row=i+1, column=0, padx=10, pady=5)
            var = tk.StringVar(value="No")
            tk.Radiobutton(self.root, text="Yes", variable=var, value="Yes").grid(row=i+1, column=1, padx=10, pady=5)
            tk.Radiobutton(self.root, text="No", variable=var, value="No").grid(row=i+1, column=2, padx=10, pady=5)
            self.seen_status_vars[player] = var

        tk.Label(self.root, text="Select Winner:").grid(row=self.no_of_players+1, column=0, padx=10, pady=10)
        self.winner_var = tk.StringVar(value=self.players[0] if self.players else "")
        for player in self.players:
            tk.Radiobutton(self.root, text=player, variable=self.winner_var, value=player).grid(row=self.no_of_players+1, column=self.players.index(player)+1, padx=10, pady=5)

        tk.Button(self.root, text="Submit Seen Status", command=self.submit_seen_status).grid(row=self.no_of_players+2, column=0, columnspan=3, pady=20)

    def submit_seen_status(self):
        self.seen_players = []
        self.unseen_players = []
        for player, var in self.seen_status_vars.items():
            status = var.get()
            if status == 'Yes':
                self.seen_players.append(player)
            elif status == 'No':
                self.unseen_players.append(player)
            else:
                messagebox.showerror("Input Error", "Invalid status. Please select 'Yes' or 'No'.")
                return
        
        self.setup_maal_entry()

    def setup_maal_entry(self):
        for widget in self.root.grid_slaves():
            widget.grid_forget()

        tk.Label(self.root, text="Enter Maal (Points) for each player:").grid(row=0, column=0, padx=10, pady=10)
        self.maal_entries = {}
        for i, player in enumerate(self.players):
            tk.Label(self.root, text=f"{player}:").grid(row=i+1, column=0, padx=10, pady=5)
            entry = tk.Entry(self.root)
            entry.grid(row=i+1, column=1, padx=10, pady=5)
            if player in self.unseen_players:
                entry.config(state=tk.DISABLED)
            self.maal_entries[player] = entry

        tk.Button(self.root, text="Submit Maal", command=self.submit_maal).grid(row=self.no_of_players+1, column=0, columnspan=2, pady=20)

    def submit_maal(self):
        try:
            self.player_maal_dict = {player: int(self.maal_entries[player].get().strip() or 0) for player in self.players}
            for player in self.unseen_players:
                self.player_maal_dict[player] = 0
        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid numbers for Maal.")
            return

        self.calculate_results()

    def calculate_results(self):
        total_maal = sum(self.player_maal_dict.values())
        winner = self.winner_var.get()
        if not winner:
            messagebox.showerror("Input Error", "Please select a winner.")
            return
        seen_player_count = len(self.seen_players)
        unseen_player_count = len(self.unseen_players)

        def handle_winner():
            to_receive = self.no_of_players * self.player_maal_dict.get(winner, 0)
            to_pay = total_maal
            gt = to_receive - to_pay + (3 * (seen_player_count - 1)) + (10 * unseen_player_count)
            return gt * self.kati_point

        def handle_seen_players():
            results = {}
            for player in self.seen_players:
                if player != winner:
                    to_receive = self.player_maal_dict.get(player, 0) * self.no_of_players
                    to_pay = total_maal + 3
                    gt = to_receive - to_pay
                    results[player] = gt * self.kati_point
            return results

        def handle_unseen_players():
            results = {}
            for player in self.unseen_players:
                to_pay = total_maal + 10
                gt = -to_pay
                results[player] = gt * self.kati_point
            return results

        winner_result = handle_winner()
        seen_results = handle_seen_players()
        unseen_results = handle_unseen_players()

        self.show_results(winner, winner_result, seen_results, unseen_results)

    def show_results(self, winner, winner_result, seen_results, unseen_results):
        for widget in self.root.grid_slaves():
            widget.grid_forget()

        tk.Label(self.root, text="Results:").grid(row=0, column=0, padx=10, pady=10)
        
        tk.Label(self.root, text=f"{winner}: {winner_result}").grid(row=1, column=0, padx=10, pady=5)

        row = 2
        for player, points in seen_results.items():
            tk.Label(self.root, text=f"{player}: {points}").grid(row=row, column=0, padx=10, pady=5)
            row += 1

        for player, points in unseen_results.items():
            tk.Label(self.root, text=f"{player}: {points}").grid(row=row, column=0, padx=10, pady=5)
            row += 1

        tk.Button(self.root, text="Start Again", command=self.start_again).grid(row=row, column=0, padx=10, pady=20)
        tk.Button(self.root, text="Exit", command=self.exit_app).grid(row=row, column=1, padx=10, pady=20)

    def start_again(self):
        for widget in self.root.grid_slaves():
            widget.grid_forget()

        self.setup_seen_status()

    def exit_app(self):
        self.root.quit()

if __name__ == "__main__":
    root = tk.Tk()
    app = GameApp(root)
    root.mainloop()
