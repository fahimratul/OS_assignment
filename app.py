import os
import shutil
import datetime
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext

# File type categories
FILE_TYPES = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff"],
    "PDFs": [".pdf"],
    "Word": [".doc", ".docx"],
    "Excel": [".xls", ".xlsx"],
    "PowerPoint": [".ppt", ".pptx"],
    "Text": [".txt", ".md"],
    "Archives": [".zip", ".rar", ".7z", ".tar", ".gz"],
    "Videos": [".mp4", ".avi", ".mkv", ".mov"],
    "Music": [".mp3", ".wav", ".flac"],
    "Code": [".py", ".cpp", ".c", ".java", ".js", ".html", ".css"]
}


def get_category(file_extension):
    """Return the category name based on file extension."""
    for category, extensions in FILE_TYPES.items():
        if file_extension.lower() in extensions:
            return category
    return "Others"


def sort_files(src_folder, dest_folder, log_widget):
    src_folder = Path(src_folder)
    dest_folder = Path(dest_folder)

    if not src_folder.exists():
        messagebox.showerror("Error", "Source folder does not exist!")
        return

    moved_count = 0
    for file in src_folder.iterdir():
        if file.is_file():
            ext = file.suffix
            category = get_category(ext)

            # Use last modified date
            mod_time = datetime.datetime.fromtimestamp(file.stat().st_mtime)
            date_folder = mod_time.strftime("%Y-%m-%d")

            # Destination path
            target_dir = dest_folder / category / date_folder
            target_dir.mkdir(parents=True, exist_ok=True)

            target_file = target_dir / file.name
            try:
                shutil.move(str(file), str(target_file))
                log_widget.insert(tk.END, f"Moved: {file.name} -> {target_file}\n")
                log_widget.see(tk.END)
                moved_count += 1
            except Exception as e:
                log_widget.insert(tk.END, f"Error moving {file.name}: {e}\n")

    messagebox.showinfo("Done", f"Sorting completed! {moved_count} files moved.")


def choose_folder(entry_widget):
    folder = filedialog.askdirectory()
    if folder:
        entry_widget.delete(0, tk.END)
        entry_widget.insert(0, folder)


# --- GUI ---
root = tk.Tk()
root.title("File Sorter")
root.geometry("650x450")
root.resizable(False, False)

# Source Folder
tk.Label(root, text="Source Folder:").pack(anchor="w", padx=10, pady=5)
src_entry = tk.Entry(root, width=70)
src_entry.pack(padx=10, pady=2, anchor="w")
tk.Button(root, text="Browse", command=lambda: choose_folder(src_entry)).pack(padx=10, pady=2, anchor="w")

# Destination Folder
tk.Label(root, text="Destination Folder:").pack(anchor="w", padx=10, pady=5)
dest_entry = tk.Entry(root, width=70)
dest_entry.pack(padx=10, pady=2, anchor="w")
tk.Button(root, text="Browse", command=lambda: choose_folder(dest_entry)).pack(padx=10, pady=2, anchor="w")

tk.Button(
    root, text="Sort Files", bg="green", fg="white",
    command=lambda: sort_files(src_entry.get(), dest_entry.get(), log_box)
).pack(pady=10)
# Log box
tk.Label(root, text="Log:").pack(anchor="w", padx=10, pady=5)
log_box = scrolledtext.ScrolledText(root, width=80, height=15)
log_box.pack(padx=10, pady=5)

# Sort Button


root.mainloop()
