import customtkinter as ctk
from datetime import datetime
import os
from tkinter import filedialog
import json  # for saving and loading the file location

# Initialize customtkinter
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class TimePunchApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Timesheet Punch Card")
        self.geometry("600x300")
        self.resizable(True, True)

        # Main frame
        self.frame = ctk.CTkFrame(self)
        self.frame.pack(pady=40, padx=40, fill="both", expand=True)

        self.label = ctk.CTkLabel(self.frame, text="Time Clock In / Out", font=("Arial", 20))
        self.label.pack(pady=(10, 10))

        # Button to select file location
        self.select_location_button = ctk.CTkButton(self.frame, text="Select File Location", command=self.select_location)
        self.select_location_button.pack(pady=(10, 10))

        self.status_label = ctk.CTkLabel(self.frame, text="", font=("Arial", 14), wraplength=500)
        self.status_label.pack(pady=(10, 10))

        # Horizontal frame for buttons
        self.button_frame = ctk.CTkFrame(self.frame)
        self.button_frame.pack(pady=10)

        self.clock_in_button = ctk.CTkButton(self.button_frame, text="Clock In", command=self.clock_in)
        self.clock_in_button.pack(side="left", padx=10)

        self.clock_out_button = ctk.CTkButton(self.button_frame, text="Clock Out", command=self.clock_out, state="disabled")
        self.clock_out_button.pack(side="left", padx=10)

        # Initialize timesheet file (filename starts as None)
        self.filename = None
        self.last_clock_in_time = None

        # Load the saved file location
        self.load_location()

    def clock_in(self):
        if not self.filename:
            self.status_label.configure(text="Please select a file location first.")
            return
        
        self.last_clock_in_time = datetime.now()
        timestamp = self.last_clock_in_time.strftime("%m-%d-%Y %H:%M:%S")
        entry = f"[{timestamp}] Clock IN\n"

        with open(self.filename, "a") as f:
            f.write(entry)

        self.status_label.configure(text=f"Clocked IN at {timestamp}")
        self.clock_in_button.configure(state="disabled")
        self.clock_out_button.configure(state="normal")

    def clock_out(self):
        if not self.last_clock_in_time:
            self.status_label.configure(text="You must clock in first!")
            return

        clock_out_time = datetime.now()
        timestamp = clock_out_time.strftime("%m-%d-%Y %H:%M:%S")
        worked_duration = clock_out_time - self.last_clock_in_time

        total_seconds = int(worked_duration.total_seconds())
        hours, remainder = divmod(total_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)

        entry = (f"[{timestamp}] Clock OUT\n"
                 f"-> Worked: {int(hours)}h {int(minutes)}m {int(seconds)}s\n\n")

        with open(self.filename, "a") as f:
            f.write(entry)

        self.status_label.configure(text=f"Clocked OUT – Worked {int(hours)}h {int(minutes)}m {int(seconds)}s")
        self.last_clock_in_time = None
        self.clock_in_button.configure(state="normal")
        self.clock_out_button.configure(state="disabled")

    def select_location(self):
        selected_directory = filedialog.askdirectory(title="Select Folder for Timesheet")
        if selected_directory:
            self.filename = os.path.join(selected_directory, "timesheet.txt")
            self.status_label.configure(text=f"Timesheet file will be saved to: {self.filename}")
            self.save_location()  # Save the selected location

    def save_location(self):
        # Save the selected file location to a JSON file
        with open("timesheet_location.json", "w") as config_file:
            json.dump({"filename": self.filename}, config_file)

    def load_location(self):
        # Load the saved file location from the JSON file
        if os.path.exists("timesheet_location.json"):
            with open("timesheet_location.json", "r") as config_file:
                data = json.load(config_file)
                self.filename = data.get("filename")
                if self.filename:
                    self.status_label.configure(text=f"Timesheet file will be saved to: {self.filename}")
                else:
                    self.status_label.configure(text="No file location selected. Please choose one.")
        else:
            self.status_label.configure(text="No file location saved. Please choose one.")

if __name__ == "__main__":
    app = TimePunchApp()
    app.mainloop()
