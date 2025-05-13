import customtkinter as ctk
from datetime import datetime
import os

# Initialize customtkinter
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class TimePunchApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Timesheet Punch Card")
        self.geometry("400x250")
        self.resizable(False, False)

        # Main frame
        self.frame = ctk.CTkFrame(self)
        self.frame.pack(pady=40, padx=40, fill="both", expand=True)

        self.label = ctk.CTkLabel(self.frame, text="Punch In / Out", font=("Arial", 20))
        self.label.pack(pady=(20, 10))

        # Horizontal frame for buttons
        self.button_frame = ctk.CTkFrame(self.frame)
        self.button_frame.pack(pady=10)

        self.clock_in_button = ctk.CTkButton(self.button_frame, text="Clock In", command=self.clock_in)
        self.clock_in_button.pack(side="left", padx=10)

        self.clock_out_button = ctk.CTkButton(self.button_frame, text="Clock Out", command=self.clock_out)
        self.clock_out_button.pack(side="left", padx=10)

        self.status_label = ctk.CTkLabel(self.frame, text="", font=("Arial", 14), wraplength=300)
        self.status_label.pack(pady=(20, 10))

        # Initialize timesheet file
        self.filename = "timesheet.txt"
        self.last_clock_in_time = None

        if not os.path.exists(self.filename):
            with open(self.filename, "w") as f:
                f.write("=== Timesheet Records ===\n\n")

    def clock_in(self):
        self.last_clock_in_time = datetime.now()
        timestamp = self.last_clock_in_time.strftime("%m-%d-%Y %H:%M:%S")
        entry = f"[{timestamp}] Clock IN\n"

        with open(self.filename, "a") as f:
            f.write(entry)

        self.status_label.configure(text=f"Clocked IN at {timestamp}")

    def clock_out(self):
        if not self.last_clock_in_time:
            self.status_label.configure(text="You must clock in first!")
            return

        clock_out_time = datetime.now()
        timestamp = clock_out_time.strftime("%m-%d-%Y %H:%M:%S")
        worked_duration = clock_out_time - self.last_clock_in_time
        hours, remainder = divmod(worked_duration.total_seconds(), 3600)
        minutes = remainder // 60

        entry = (f"[{timestamp}] Clock OUT\n"
                 f"-> Worked: {int(hours)}h {int(minutes)}m\n\n")

        with open(self.filename, "a") as f:
            f.write(entry)

        self.status_label.configure(text=f"Clocked OUT – Worked {int(hours)}h {int(minutes)}m")
        self.last_clock_in_time = None  # Reset

if __name__ == "__main__":
    app = TimePunchApp()
    app.mainloop()
