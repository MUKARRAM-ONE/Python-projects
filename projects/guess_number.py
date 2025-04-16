
import tkinter as tk
import random

class GuessNumberGame:
    def __init__(self, master):
        self.master = master
        master.title("Guess the Number Game")

        self.mode = tk.StringVar(value="user")
        self.difficulty = tk.StringVar(value="easy")
        self.attempts_left = 0
        self.secret_number = 0
        self.low = 1
        self.high = 10
        self.computer_guess = 0

        # Mode selection
        tk.Label(master, text="Select Mode:").pack()
        tk.Radiobutton(master, text="User Guesses", variable=self.mode, value="user").pack()
        tk.Radiobutton(master, text="Computer Guesses", variable=self.mode, value="computer").pack()

        # Difficulty selection
        tk.Label(master, text="Select Difficulty:").pack()
        tk.Radiobutton(master, text="Easy (1-10)", variable=self.difficulty, value="easy").pack()
        tk.Radiobutton(master, text="Medium (1-50)", variable=self.difficulty, value="medium").pack()
        tk.Radiobutton(master, text="Hard (1-100)", variable=self.difficulty, value="hard").pack()

        # Start button
        tk.Button(master, text="Start Game", command=self.start_game).pack()

        # Feedback label
        self.feedback = tk.Label(master, text="")
        self.feedback.pack()

        # Entry and submit button
        self.entry = tk.Entry(master)
        self.submit_button = tk.Button(master, text="Submit", command=self.submit_guess)

    def start_game(self):
        difficulty = self.difficulty.get()
        if difficulty == "easy":
            self.low, self.high, self.attempts_left = 1, 10, 5
        elif difficulty == "medium":
            self.low, self.high, self.attempts_left = 1, 50, 7
        else:
            self.low, self.high, self.attempts_left = 1, 100, 10

        mode = self.mode.get()
        if mode == "user":
            self.secret_number = random.randint(self.low, self.high)
            self.feedback.config(text=f"Guess a number between {self.low} and {self.high}")
            self.entry.pack()
            self.submit_button.pack()
        else:
            self.computer_guess = (self.low + self.high) // 2
            self.feedback.config(text=f"Is your number {self.computer_guess}? (Enter 'h' for higher, 'l' for lower, 'c' for correct)")
            self.entry.pack()
            self.submit_button.pack()

    def submit_guess(self):
        guess = self.entry.get()
        mode = self.mode.get()
        if mode == "user":
            try:
                guess = int(guess)
                self.attempts_left -= 1
                if guess < self.secret_number:
                    self.feedback.config(text="Too low!")
                elif guess > self.secret_number:
                    self.feedback.config(text="Too high!")
                else:
                    self.feedback.config(text="Correct! You win!")
                    self.entry.pack_forget()
                    self.submit_button.pack_forget()
                    return
                if self.attempts_left == 0:
                    self.feedback.config(text=f"Out of attempts! The number was {self.secret_number}.")
                    self.entry.pack_forget()
                    self.submit_button.pack_forget()
            except ValueError:
                self.feedback.config(text="Please enter a valid number.")
        else:
            if guess.lower() == 'h':
                self.low = self.computer_guess + 1
            elif guess.lower() == 'l':
                self.high = self.computer_guess - 1
            elif guess.lower() == 'c':
                self.feedback.config(text="Yay! I guessed it!")
                self.entry.pack_forget()
                self.submit_button.pack_forget()
                return
            else:
                self.feedback.config(text="Please enter 'h', 'l', or 'c'.")
                return
            if self.low > self.high:
                self.feedback.config(text="Hmm, something doesn't add up. Let's restart.")
                self.entry.pack_forget()
                self.submit_button.pack_forget()
                return
            self.computer_guess = (self.low + self.high) // 2
            self.feedback.config(text=f"Is your number {self.computer_guess}? (Enter 'h' for higher, 'l' for lower, 'c' for correct)")

# Create the main window
root = tk.Tk()
game = GuessNumberGame(root)
root.mainloop()
