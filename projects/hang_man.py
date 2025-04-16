import tkinter as tk
from tkinter import messagebox
import random

# List of words and hangman drawing stages (from complete drawing to empty scaffold)
word_list = ["python", "hangman", "challenge", "programming", "computer"]
hangman_stages = [
    # Stage 0: Full drawing (lost all lives)
    """
       --------
       |      |
       |      O
       |     \\|/
       |      |
       |     / \\
       -
    """,
    # Stage 1:
    """
       --------
       |      |
       |      O
       |     \\|/
       |      |
       |     /
       -
    """,
    # Stage 2:
    """
       --------
       |      |
       |      O
       |     \\|/
       |      |
       |
       -
    """,
    # Stage 3:
    """
       --------
       |      |
       |      O
       |     \\|
       |      |
       |
       -
    """,
    # Stage 4:
    """
       --------
       |      |
       |      O
       |      |
       |      |
       |
       -
    """,
    # Stage 5:
    """
       --------
       |      |
       |      O
       |
       |
       |
       -
    """,
    # Stage 6: Empty scaffold (all lives available)
    """
       --------
       |      |
       |
       |
       |
       |
       -
    """
]


class HangmanGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Hangman Game")
        # Initialize game variables.
        self.word = ""
        self.word_letters = set()
        self.used_letters = set()
        self.lives = 6

        # Setup GUI elements.
        self.word_label = tk.Label(master, text="Word:", font=("Helvetica", 20))
        self.word_label.pack(pady=10)

        self.used_label = tk.Label(master, text="Used Letters:", font=("Helvetica", 14))
        self.used_label.pack(pady=5)

        self.lives_label = tk.Label(master, text="Lives Left: 6", font=("Helvetica", 14))
        self.lives_label.pack(pady=5)

        # Label to display the Hangman drawing using ASCII art.
        self.hangman_label = tk.Label(master, text=hangman_stages[-1], font=("Courier", 14), justify="left")
        self.hangman_label.pack(pady=10)

        # Entry widget for letter input.
        self.entry = tk.Entry(master, font=("Helvetica", 16))
        self.entry.pack(pady=10)

        # Button to submit the guessed letter.
        self.guess_button = tk.Button(master, text="Guess", command=self.guess_letter, font=("Helvetica", 14))
        self.guess_button.pack(pady=10)

        # Button to start a new game.
        self.new_game_button = tk.Button(master, text="New Game", command=self.new_game, font=("Helvetica", 14))
        self.new_game_button.pack(pady=10)

        self.new_game()

    def new_game(self):
        # Start a new game by choosing a random word and resetting game state.
        self.word = random.choice(word_list).upper()
        self.word_letters = set(self.word)
        self.used_letters = set()
        self.lives = 6
        self.update_display()

    def update_display(self):
        # Update the word display: show guessed letters and underscores for remaining letters.
        display_word = ' '.join([letter if letter in self.used_letters else '_' for letter in self.word])
        self.word_label.config(text=f"Word: {display_word}")
        self.used_label.config(text=f"Used Letters: {' '.join(sorted(self.used_letters))}")
        self.lives_label.config(text=f"Lives Left: {self.lives}")
        # Hangman stage index: more wrong guesses means a higher stage (fewer lives left).
        stage_index = 6 - self.lives if self.lives < 7 else 6
        self.hangman_label.config(text=hangman_stages[stage_index])

    def guess_letter(self):
        # Retrieve the input from the user, ensuring it's a valid single alphabetical character.
        letter = self.entry.get().upper()
        self.entry.delete(0, tk.END)
        if len(letter) != 1 or not letter.isalpha():
            messagebox.showwarning("Invalid Input", "Please enter a single alphabetical character.")
            return

        if letter in self.used_letters:
            messagebox.showinfo("Already Guessed", f"You already guessed the letter {letter}.")
            return

        # Add letter to used letters and check if it is in the word.
        self.used_letters.add(letter)
        if letter in self.word_letters:
            self.word_letters.remove(letter)
        else:
            self.lives -= 1

        self.update_display()
        self.check_game_over()

    def check_game_over(self):
        # Check if the player has won or lost, and display a message accordingly.
        if self.lives <= 0:
            messagebox.showinfo("Game Over", f"You lost! The word was: {self.word}")
            self.new_game()
        elif not self.word_letters:
            messagebox.showinfo("Congratulations!", f"You guessed the word: {self.word}!")
            self.new_game()


if __name__ == '__main__':
    root = tk.Tk()
    game = HangmanGUI(root)
    root.mainloop()
