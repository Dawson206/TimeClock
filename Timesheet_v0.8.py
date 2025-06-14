import customtkinter as ctk
from datetime import datetime, timedelta
from tkinter import filedialog, messagebox
from collections import defaultdict
import json
import os

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class TimePunchApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Timesheet Punch Card | V0.8")
        self.geometry("800x400")
        self.resizable(True, True)

        self.data_file = "timesheet.json"
        self.export_file = "timesheet_export.txt"
        self.history = []
        self.last_clock_in_time = None

        # Main frame
        self.frame = ctk.CTkFrame(self)
        self.frame.pack(pady=30, padx=30, fill="both", expand=True)

        self.label = ctk.CTkLabel(self.frame, text="Time Clock In / Out", font=("Arial", 20))
        self.label.pack(pady=(10, 10))

        self.status_label = ctk.CTkLabel(self.frame, text="", font=("Arial", 14), wraplength=400)
        self.status_label.pack(pady=(10, 10))

        # Button frame
        self.button_frame = ctk.CTkFrame(self.frame)
        self.button_frame.pack(pady=10)

        self.clock_in_button = ctk.CTkButton(self.button_frame, text="Clock In", command=self.clock_in)
        self.clock_in_button.pack(side="left", padx=10)

        self.clock_out_button = ctk.CTkButton(self.button_frame, text="Clock Out", command=self.clock_out, state="disabled")
        self.clock_out_button.pack(side="left", padx=10)

        self.button_frame_2 = ctk.CTkFrame(self.frame)
        self.button_frame_2.pack(pady=10)

        self.export_button = ctk.CTkButton(self.button_frame_2, text="Export to TXT", command=self.export_to_txt)
        self.export_button.pack(side="left", padx=10)

        self.clear_button = ctk.CTkButton(self.button_frame_2, text="Reset Timesheet", command=self.clear_history)
        self.clear_button.pack(side="left", padx=10)
       
        # Handle window close
        self.protocol("WM_DELETE_WINDOW", self.on_close)

        # History display
        self.history_box = ctk.CTkTextbox(self.frame, height=120, width=500)
        self.history_box.pack(pady=(10, 0))
        self.history_box.configure(state="disabled")
        self.load_history()

    def clock_in(self):
        if self.last_clock_in_time:
            self.status_label.configure(text="Already clocked in.")
            return

        self.last_clock_in_time = datetime.now()
        self.status_label.configure(text=f"Clocked IN at {self.last_clock_in_time.strftime('%m-%d-%Y %H:%M:%S')}")
        self.clock_in_button.configure(state="disabled")
        self.clock_out_button.configure(state="normal")
        self.save_history()
        self.update_history_display()

    def clock_out(self):
        if not self.last_clock_in_time:
            self.status_label.configure(text="You must clock in first.")
            return

        clock_out_time = datetime.now()
        duration = clock_out_time - self.last_clock_in_time
        total_seconds = int(duration.total_seconds())
        hours, remainder = divmod(total_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)

        record = {
            "in": self.last_clock_in_time.strftime("%m-%d-%Y %H:%M:%S"),
            "out": clock_out_time.strftime("%m-%d-%Y %H:%M:%S"),
            "duration": f"{hours}h {minutes}m {seconds}s"
        }

        self.history.append(record)
        self.save_history()

        self.status_label.configure(text=f"Clocked OUT – Worked {hours}h {minutes}m {seconds}s")
        self.last_clock_in_time = None
        self.clock_in_button.configure(state="normal")
        self.clock_out_button.configure(state="disabled")
        self.update_history_display()

    def update_history_display(self):
        self.history_box.configure(state="normal")
        self.history_box.delete("1.0", "end")
        for entry in self.history:
            try:
                clock_in_dt = datetime.strptime(entry["in"], "%m-%d-%Y %H:%M:%S")
                day_of_week = clock_in_dt.strftime("%A")
            except Exception:
                day_of_week = "Unknown Day"

            self.history_box.insert("end", f"{day_of_week}\n")
            self.history_box.insert("end", f"Clock In:  {entry['in']}\n")
            self.history_box.insert("end", f"Clock Out: {entry['out']}\n")
            self.history_box.insert("end", f"Worked:    {entry['duration']}\n\n")
        self.history_box.configure(state="disabled")

    def save_history(self):
        data = {
            "history": self.history,
            "last_clock_in_time": self.last_clock_in_time.strftime("%m-%d-%Y %H:%M:%S") if self.last_clock_in_time else None
        }
        with open(self.data_file, "w") as f:
            json.dump(data, f, indent=4)

    def load_history(self):
        if os.path.exists(self.data_file):
            with open(self.data_file, "r") as f:
                data = json.load(f)
                self.history = data.get("history", [])
                last_time = data.get("last_clock_in_time")
                if last_time:
                    try:
                        self.last_clock_in_time = datetime.strptime(last_time, "%m-%d-%Y %H:%M:%S")
                        self.status_label.configure(text=f"Recovered clock-in from {self.last_clock_in_time.strftime('%m-%d-%Y %H:%M:%S')}")
                        self.clock_in_button.configure(state="disabled")
                        self.clock_out_button.configure(state="normal")
                    except Exception:
                        self.last_clock_in_time = None
                else:
                    self.last_clock_in_time = None
        else:
            self.history = []
            self.last_clock_in_time = None

        self.update_history_display()

    def clear_history(self):
        if messagebox.askyesno("Confirm Reset", "Are you sure you want to reset? This will delete the entire history."):
            self.history = []
            self.last_clock_in_time = None
            self.save_history()
            self.status_label.configure(text="History cleared.")
            self.clock_in_button.configure(state="normal")
            self.clock_out_button.configure(state="disabled")
            self.update_history_display()

    def export_to_txt(self):
        if self.last_clock_in_time:
            self.status_label.configure(text="You must clock out before exporting.")
            return

        if not self.history:
            self.status_label.configure(text="No history to export.")
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text Files", "*.txt")],
            title="Export Timesheet As"
        )

        if not file_path:
            self.status_label.configure(text="Export canceled.")
            return

        weekly_entries = defaultdict(list)

        try:
            for entry in self.history:
                try:
                    clock_in_dt = datetime.strptime(entry["in"], "%m-%d-%Y %H:%M:%S")
                    week_start = clock_in_dt - timedelta(days=clock_in_dt.weekday())
                    week_key = week_start.strftime("%Y-%m-%d")  # Use string key to normalize
                    weekly_entries[week_key].append(entry)
                except Exception:
                    continue

            with open(file_path, "w") as f:
                for week_key in sorted(weekly_entries.keys()):
                    week_start_dt = datetime.strptime(week_key, "%Y-%m-%d")
                    f.write(f"=== Week of {week_start_dt.strftime('%B %d, %Y')} ===\n\n")

                    total_duration = timedelta()

                    for entry in sorted(weekly_entries[week_key], key=lambda e: datetime.strptime(e["in"], "%m-%d-%Y %H:%M:%S")):
                        try:
                            clock_in_dt = datetime.strptime(entry["in"], "%m-%d-%Y %H:%M:%S")
                            clock_out_dt = datetime.strptime(entry["out"], "%m-%d-%Y %H:%M:%S")
                            duration = clock_out_dt - clock_in_dt
                            total_duration += duration

                            day_of_week = clock_in_dt.strftime("%A")
                            f.write(f"{day_of_week}\n")
                            f.write(f"Clock In:  {entry['in']}\n")
                            f.write(f"Clock Out: {entry['out']}\n")
                            f.write(f"Worked:    {entry['duration']}\n\n")
                        except Exception:
                            continue

                    total_seconds = int(total_duration.total_seconds())
                    hours, remainder = divmod(total_seconds, 3600)
                    minutes, seconds = divmod(remainder, 60)
                    f.write(f"Weekly Total Hours Worked: {hours}h {minutes}m {seconds}s\n\n")

            self.status_label.configure(text=f"Timesheet exported to: {file_path}")

        except Exception as e:
            messagebox.showerror("Export Failed", f"Could not export timesheet:\n{e}")

    def on_close(self):
        if self.last_clock_in_time:
            if messagebox.askyesno("Still Clocked In", "You're still clocked in. Do you want to exit anyway?"):
                self.save_history()
                self.destroy()
                
        else:
            self.save_history()
            self.destroy()

if __name__ == "__main__":
    app = TimePunchApp()
    app.mainloop()
