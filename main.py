import random
import tkinter as tk
from tkinter import simpledialog, messagebox

# Constants
MAX_LINES = 3
MAX_BET = 100
MIN_BET = 1
ROWS = 3
COLS = 3

# Symbol counts and values
symbol_count = {
    "A": 2,
    "B": 4,
    "C": 6,
    "D": 8
}

symbol_value = {
    "A": 5,
    "B": 4,
    "C": 3,
    "D": 2
}

# Function to check winnings
def checking_winnings(columns, lines, bet, values):
    winnings = 0
    winning_lines = []
    for line in range(lines):
        symbol = columns[0][line]
        for column in columns:
            symbols_to_check = column[line]
            if symbol != symbols_to_check:
                break
        else:
            winnings += values[symbol] * bet
            winning_lines.append(line + 1)
    return winnings, winning_lines

# Function to get the slot machine spin
def get_slot_machine_spin(rows, cols, symbols):
    all_symbols = []
    for symbol, symbol_count in symbols.items():
        for _ in range(symbol_count):
            all_symbols.append(symbol)

    columns = [[], [], []]
    for col in range(cols):
        column = []
        current_symbols = all_symbols[:]  # using the slice operator to copy a list
        for _ in range(rows):
            value = random.choice(current_symbols)
            current_symbols.remove(value)
            column.append(value)
        columns[col] = column  # Assign the filled column to the correct position
    return columns

# GUI Class
class SlotMachineApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Slot Machine Game")
        self.geometry("600x400")

        self.balance = 0

        self.create_widgets()

    def create_widgets(self):
        self.balance_label = tk.Label(self, text="Current Balance: N$0")
        self.balance_label.pack(pady=10)

        self.deposit_button = tk.Button(self, text="Deposit", command=self.deposit)
        self.deposit_button.pack(pady=10)

        self.lines_label = tk.Label(self, text=f"Lines to bet on (1-{MAX_LINES}):")
        self.lines_label.pack(pady=10)
        self.lines_entry = tk.Entry(self)
        self.lines_entry.pack(pady=10)

        self.bet_label = tk.Label(self, text=f"Bet amount per line (N${MIN_BET}-{MAX_BET}):")
        self.bet_label.pack(pady=10)
        self.bet_entry = tk.Entry(self)
        self.bet_entry.pack(pady=10)

        self.spin_button = tk.Button(self, text="Spin", command=self.spin)
        self.spin_button.pack(pady=20)

        self.result_text = tk.Text(self, height=10, width=50)
        self.result_text.pack(pady=10)

    def update_balance(self, amount):
        self.balance += amount
        self.balance_label.config(text=f"Current Balance: N${self.balance}")

    def deposit(self):
        amount = simpledialog.askinteger("Deposit", "Enter amount to deposit:")
        if amount is not None:
            if amount > 0:
                self.update_balance(amount)
            else:
                messagebox.showerror("Error", "Amount must be greater than zero.")
        else:
            messagebox.showerror("Error", "Please enter a valid number.")

    def get_lines(self):
        lines = self.lines_entry.get()
        if lines.isdigit():
            lines = int(lines)
            if 1 <= lines <= MAX_LINES:
                return lines
        messagebox.showerror("Error", f"Enter a valid number of lines (1-{MAX_LINES}).")
        return None

    def get_bet(self):
        bet = self.bet_entry.get()
        if bet.isdigit():
            bet = int(bet)
            if MIN_BET <= bet <= MAX_BET:
                return bet
        messagebox.showerror("Error", f"Bet amount must be between N${MIN_BET} and N${MAX_BET}.")
        return None

    def spin(self):
        lines = self.get_lines()
        if lines is None:
            return

        bet = self.get_bet()
        if bet is None:
            return

        total_bet = bet * lines
        if total_bet > self.balance:
            messagebox.showerror("Error", f"You do not have enough to bet that amount. Current balance: N${self.balance}")
            return

        self.update_balance(-total_bet)
        slot = get_slot_machine_spin(ROWS, COLS, symbol_count)
        winnings, winning_lines = checking_winnings(slot, lines, bet, symbol_value)
        self.update_balance(winnings)

        self.result_text.delete(1.0, tk.END)
        for row in range(len(slot[0])):
            row_text = " | ".join(column[row] for column in slot)
            self.result_text.insert(tk.END, row_text + "\n")

        self.result_text.insert(tk.END, f"\nYou won N${winnings}\n")
        if winning_lines:
            self.result_text.insert(tk.END, f"You won on lines: {', '.join(map(str, winning_lines))}\n")
        else:
            self.result_text.insert(tk.END, "No winning lines.\n")

# Run the GUI
if __name__ == "__main__":
    app = SlotMachineApp()
    app.mainloop()
