import tkinter as tk
import random

# Word banks for random generation
adjectives = ["silly", "fluffy", "angry", "funny"]
nouns = ["dragon", "robot", "pirate", "unicorn"]
verbs = ["jumped", "ran", "danced", "screamed"]
places = ["zoo", "forest", "moon", "school"]

# Multiple templates
templates = [
    "Yesterday, I went to the {place}. It was a really {adjective} day. Suddenly, I saw a {noun}. I {verb} quickly!",
    "At the {place}, a {adjective} {noun} appeared. Everyone {verb} in surprise!",
    "The {noun} at the {place} was so {adjective}, I {verb} with joy!"
]

# Save to file
def save_to_file(data):
    with open("madlibs_log.txt", "a") as f:
        f.write(data + "\n" + "-"*40 + "\n")

# Generate story
def generate_story():
    adjective = adj_input.get() or random.choice(adjectives)
    noun = noun_input.get() or random.choice(nouns)
    verb = verb_input.get() or random.choice(verbs)
    place = place_input.get() or random.choice(places)

    template = random.choice(templates)
    story = template.format(adjective=adjective, noun=noun, verb=verb, place=place)

    output_label.config(text=story)
    save_to_file(story)

# GUI Setup
root = tk.Tk()
root.title("Mad Libs Game")

tk.Label(root, text="Adjective:").grid(row=0, column=0)
adj_input = tk.Entry(root)
adj_input.grid(row=0, column=1)

tk.Label(root, text="Noun:").grid(row=1, column=0)
noun_input = tk.Entry(root)
noun_input.grid(row=1, column=1)

tk.Label(root, text="Verb (past):").grid(row=2, column=0)
verb_input = tk.Entry(root)
verb_input.grid(row=2, column=1)

tk.Label(root, text="Place:").grid(row=3, column=0)
place_input = tk.Entry(root)
place_input.grid(row=3, column=1)

generate_btn = tk.Button(root, text="Generate Mad Lib", command=generate_story)
generate_btn.grid(row=4, column=0, columnspan=2, pady=10)

output_label = tk.Label(root, text="", wraplength=300, justify="left", font=("Arial", 12), fg="blue")
output_label.grid(row=5, column=0, columnspan=2, pady=10)

root.mainloop()
