import tkinter as tk
import threading
import winsound  # Windows only; for cross-platform usage consider other libraries


class CountdownTimer:
    def __init__(self, master, count):
        self.master = master
        self.original_count = count  # Stores the initial timer value for reset.
        self.count = count  # Current time (in seconds).
        self.running = False  # Indicates if the timer is currently running.

        # Label to display the timer in MM:SS format.
        self.label = tk.Label(master, text=self.format_time(self.count), font=("Helvetica", 48))
        self.label.pack(pady=20)

        # Frame containing the increase (+) and decrease (-) buttons.
        adjust_frame = tk.Frame(master)
        self.increase_button = tk.Button(adjust_frame, text="+", command=self.increase_timer,
                                         font=("Helvetica", 14), width=3)
        self.increase_button.pack(side=tk.LEFT, padx=5)
        self.decrease_button = tk.Button(adjust_frame, text="-", command=self.decrease_timer,
                                         font=("Helvetica", 14), width=3)
        self.decrease_button.pack(side=tk.LEFT, padx=5)
        adjust_frame.pack(pady=10)

        # Start button to begin the countdown.
        self.start_button = tk.Button(master, text="Start", command=self.start, font=("Helvetica", 14))
        self.start_button.pack(pady=10)

        # Reset button to revert the timer to its original duration.
        self.reset_button = tk.Button(master, text="Reset", command=self.reset, font=("Helvetica", 14))
        self.reset_button.pack(pady=10)

    def start(self):
        """Starts the countdown if it is not already running."""
        if not self.running:
            self.running = True
            self.countdown()

    def reset(self):
        """Stops the countdown and resets the timer to the original count."""
        self.running = False
        self.count = self.original_count
        self.label.config(text=self.format_time(self.count))

    def increase_timer(self):
        """Increase the timer by 10 seconds."""
        increment = 10
        self.count += increment
        self.original_count += increment
        self.label.config(text=self.format_time(self.count))

    def decrease_timer(self):
        """Decrease the timer by 10 seconds, not allowing it to drop below 0."""
        decrement = 10
        if self.count - decrement >= 0 and self.original_count - decrement >= 0:
            self.count -= decrement
            self.original_count -= decrement
        else:
            self.count = 0
            self.original_count = 0
        self.label.config(text=self.format_time(self.count))

    def countdown(self):
        """Update the timer once per second until the count reaches 0."""
        self.label.config(text=self.format_time(self.count))
        if self.count > 0 and self.running:
            self.count -= 1
            # Schedule the countdown method to run again after 1000 ms (1 second).
            self.master.after(1000, self.countdown)
        else:
            self.running = False
            # Timer finished; start the alarm sound in a separate thread.
            threading.Thread(target=self.play_alarm, daemon=True).start()

    def play_alarm(self):
        """Play a beep sound repeatedly for 5 seconds when the timer reaches zero."""
        beep_duration = 250  # Duration of each beep in milliseconds.
        frequency = 1000  # Frequency of beep in Hz.
        iterations = 5000 // beep_duration  # Total beeps for approximately 5 seconds.
        for _ in range(iterations):
            winsound.Beep(frequency, beep_duration)

    def format_time(self, seconds):
        """Convert seconds into a MM:SS formatted string."""
        minutes, sec = divmod(seconds, 60)
        return f"{minutes:02d}:{sec:02d}"


if __name__ == '__main__':
    # Set an initial countdown value, for example, 2 minutes (120 seconds).
    initial_count = 120
    root = tk.Tk()
    root.title("Countdown Timer")
    timer = CountdownTimer(root, initial_count)
    root.mainloop()
