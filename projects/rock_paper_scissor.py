import tkinter as tk
import random

options = ["Rock", "Paper", "Scissors"]

def decide_winner(p1, p2):
    if p1 == p2:
        return "It's a tie!"
    elif (p1 == "Rock" and p2 == "Scissors") or (p1 == "Paper" and p2 == "Rock") or (p1 == "Scissors" and p2 == "Paper"):
        return "Player 1 wins!"
    else:
        return "Player 2 wins!"

def user_vs_user():
    result_label.config(text="Player 1, choose your move.")
    input_frame.pack()
    play_button.config(command=play_user_vs_user)

def user_vs_computer():
    result_label.config(text="Choose your move against the computer.")
    input_frame.pack()
    play_button.config(command=play_user_vs_computer)

def computer_vs_computer():
    p1 = random.choice(options)
    p2 = random.choice(options)
    result = decide_winner(p1, p2)
    result_label.config(text=f"Computer 1 chose {p1}\nComputer 2 chose {p2}\n{result}")
    input_frame.pack_forget()

def play_user_vs_user():
    p1 = player1_var.get()
    p2 = player2_var.get()
    result = decide_winner(p1, p2)
    result_label.config(text=f"Player 1 chose {p1}\nPlayer 2 chose {p2}\n{result}")

def play_user_vs_computer():
    p1 = player1_var.get()
    p2 = random.choice(options)
    result = decide_winner(p1, p2)
    result_label.config(text=f"You chose {p1}\nComputer chose {p2}\n{result}")

# GUI setup
root = tk.Tk()
root.title("Rock Paper Scissors")

# Mode buttons
mode_frame = tk.Frame(root)
tk.Button(mode_frame, text="User vs User", command=user_vs_user).pack(side=tk.LEFT, padx=10, pady=10)
tk.Button(mode_frame, text="User vs Computer", command=user_vs_computer).pack(side=tk.LEFT, padx=10, pady=10)
tk.Button(mode_frame, text="Computer vs Computer", command=computer_vs_computer).pack(side=tk.LEFT, padx=10, pady=10)
mode_frame.pack()

# Input frame
input_frame = tk.Frame(root)
player1_var = tk.StringVar()
player2_var = tk.StringVar()

tk.Label(input_frame, text="Player 1:").grid(row=0, column=0)
tk.OptionMenu(input_frame, player1_var, *options).grid(row=0, column=1)

tk.Label(input_frame, text="Player 2:").grid(row=1, column=0)
tk.OptionMenu(input_frame, player2_var, *options).grid(row=1, column=1)

play_button = tk.Button(input_frame, text="Play")
play_button.grid(row=2, columnspan=2, pady=10)

# Result label
result_label = tk.Label(root, text="Choose a game mode to start!", font=("Arial", 12), wraplength=300, justify="center")
result_label.pack(pady=20)

root.mainloop()