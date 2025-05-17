![timeclock](https://github.com/user-attachments/assets/95393472-25d9-466f-9a67-80bc2cef5a8e)

**TimeClock** is a lightweight desktop application that lets you track work hours using a simple clock-in and clock-out interface.

Built with Python and CustomTkinter, it's designed for individual users who want a clear, offline record of their working hours without any fluff.

---

## 🕒 Features

- **Clock In / Clock Out**  
  Track work sessions with timestamps and durations automatically calculated.

- **Persistent History**  
  All entries are saved to a local `timesheet.json` file and loaded on startup.

- **Weekly Export**  
  Export your punch history to a clean `.txt` file that includes:
  - Day of the week
  - Clock-in and clock-out times
  - Duration worked

- **Manual Reset**  
  Clear your entire history with a confirmation prompt.

- **Prevents Mistakes**  
  - Export is blocked unless you're clocked out
  - Exit warning if you're still clocked in

---

## 📦 Installation

1. Download the latest `.exe` release (Windows only).
2. Run the application. No installation required.
3. Timesheet data is saved in the same folder as the executable.

---

## 📁 Files

- `timesheet.json` – stores your clock in/out history
- `timesheet_export.txt` – your exported summary file (you choose where to save it)

