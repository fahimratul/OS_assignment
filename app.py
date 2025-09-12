
# --- Import required modules ---
import os
import shutil
import datetime
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext



# --- File type categories for sorting ---
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


# --- Get the category name for a file extension ---
def get_category(file_extension):
    """Return the category name based on file extension."""
    for category, extensions in FILE_TYPES.items():
        if file_extension.lower() in extensions:
            return category
    return "Others"


# --- Main function to sort files, move them, and optionally delete empty folders ---
def sort_files(src_folders, dest_folder, log_widget, selected_types, sort_by_date, delete_empty):
    dest_folder = Path(dest_folder)  # Destination directory
    total_moved = 0  # Total files moved counter
    for src_folder in src_folders:
        src_folder = Path(src_folder)
        if not src_folder.exists():
            log_widget.insert(tk.END, f"Source folder does not exist: {src_folder}\n")
            continue
        moved_count = 0  # Files moved from this source folder
        for file in src_folder.iterdir():
            if file.is_file():
                ext = file.suffix
                category = get_category(ext)
                # Only move files of selected types
                if category not in selected_types:
                    continue
                # Sort by date if selected
                if sort_by_date:
                    mod_time = datetime.datetime.fromtimestamp(file.stat().st_mtime)
                    date_folder = mod_time.strftime("%Y-%m-%d")
                    target_dir = dest_folder / category / date_folder
                else:
                    target_dir = dest_folder / category
                target_dir.mkdir(parents=True, exist_ok=True)
                target_file = target_dir / file.name
                try:
                    shutil.move(str(file), str(target_file))
                    log_widget.insert(tk.END, f"Moved: {file.name} -> {target_file}\n")
                    log_widget.see(tk.END)
                    moved_count += 1
                except Exception as e:
                    log_widget.insert(tk.END, f"Error moving {file.name}: {e}\n")
        total_moved += moved_count
        # Optionally delete empty folders after moving
        if delete_empty:
            for root_dir, dirs, files in os.walk(src_folder, topdown=False):
                if not os.listdir(root_dir):
                    try:
                        os.rmdir(root_dir)
                        log_widget.insert(tk.END, f"Deleted empty folder: {root_dir}\n")
                    except Exception as e:
                        log_widget.insert(tk.END, f"Error deleting folder {root_dir}: {e}\n")
    messagebox.showinfo("Done", f"Sorting completed! {total_moved} files moved.")


# --- Function to let user select multiple source folders ---
def choose_folders(entry_widget):
    folders = filedialog.askdirectory(mustexist=True, title="Select a folder (repeat for more)")
    # Use askdirectory for one folder, but allow user to add more via a button
    if folders:
        current = entry_widget.get()
        if current:
            folder_list = current.split(';')
        else:
            folder_list = []
        if folders not in folder_list:
            folder_list.append(folders)
        entry_widget.delete(0, tk.END)
        entry_widget.insert(0, ';'.join(folder_list))



# --- GUI Setup ---
root = tk.Tk()
root.title("Flow Bit")
root.geometry("700x600")
root.resizable(True, True)


# --- Source Folders input (multiple allowed) ---
tk.Label(root, text="Source Folders (multiple, separated by ;):").pack(anchor="w", padx=10, pady=5)
src_entry = tk.Entry(root, width=70)
src_entry.pack(padx=10, pady=2, anchor="w")
tk.Button(root, text="Add Folder", command=lambda: choose_folders(src_entry)).pack(padx=10, pady=2, anchor="w")

# --- Destination Folder input ---
tk.Label(root, text="Destination Folder:").pack(anchor="w", padx=10, pady=5)
dest_entry = tk.Entry(root, width=70)
dest_entry.pack(padx=10, pady=2, anchor="w")
# Function to select destination folder
def choose_folder(entry_widget):
    folder = filedialog.askdirectory()
    if folder:
        entry_widget.delete(0, tk.END)
        entry_widget.insert(0, folder)
tk.Button(root, text="Browse", command=lambda: choose_folder(dest_entry)).pack(padx=10, pady=2, anchor="w")

# --- File type selection checkboxes ---
tk.Label(root, text="Select file types to separate:").pack(anchor="w", padx=10, pady=5)
file_type_vars = {}
file_type_frame = tk.Frame(root)
file_type_frame.pack(anchor="w", padx=20)
for i, category in enumerate(FILE_TYPES.keys()):
    var = tk.BooleanVar(value=True)
    file_type_vars[category] = var
    tk.Checkbutton(file_type_frame, text=category, variable=var).grid(row=i//4, column=i%4, sticky="w", padx=5, pady=2)


# --- Sort by date option checkbox ---
sort_by_date_var = tk.BooleanVar(value=True)
tk.Checkbutton(root, text="Sort by date (create subfolders by date)", variable=sort_by_date_var).pack(anchor="w", padx=10, pady=5)

# --- Delete empty folders option checkbox ---
delete_empty_var = tk.BooleanVar(value=False)
tk.Checkbutton(
    root,
    text="Delete empty source folders after sorting",
    variable=delete_empty_var,
    fg="red"
).pack(anchor="w", padx=10, pady=5)


# --- Sort Button and its callback ---
def on_sort():
    # Gather selected file types
    selected_types = [cat for cat, var in file_type_vars.items() if var.get()]
    # Always include 'Others' if user wants to move unknown types
    if 'Others' not in selected_types and any(var.get() for cat, var in file_type_vars.items()):
        selected_types.append('Others')
    # Get all source folders from entry
    src_folders = [f.strip() for f in src_entry.get().split(';') if f.strip()]
    if not src_folders:
        messagebox.showerror("Error", "Please select at least one source folder.")
        return
    # Call the main sorting function
    sort_files(
        src_folders,
        dest_entry.get(),
        log_box,
        selected_types,
        sort_by_date_var.get(),
        delete_empty_var.get()
    )

tk.Button(
    root, text="Sort Files", bg="green", fg="white",
    command=on_sort
).pack(pady=10)


# --- Log output box ---
tk.Label(root, text="Log:").pack(anchor="w", padx=10, pady=5)
log_box = scrolledtext.ScrolledText(root, width=80, height=15)
log_box.pack(padx=10, pady=5)



# --- Start the GUI event loop ---
root.mainloop()
