
# --- Import required modules ---
import os
import shutil
import datetime
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, font
import psutil
import threading
import time


# --- Welcome Screen Class ---
class WelcomeScreen:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Welcome to Flow Bit")
        self.root.geometry("650x600")
        self.root.resizable(False, False)
        self.root.configure(bg="#f0f0f0")
        
        # Center the window
        self.center_window()
        
        self.setup_ui()
        
    def center_window(self):
        """Center the window on the screen"""
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (650 // 2)
        y = (self.root.winfo_screenheight() // 2) - (600 // 2)
        self.root.geometry(f"650x600+{x}+{y}")
    
    def setup_ui(self):
        """Setup the welcome screen UI"""
        # Main container
        main_frame = tk.Frame(self.root, bg="#f0f0f0")
        main_frame.pack(expand=True, fill="both", padx=40, pady=40)
        
        # Title
        title_font = font.Font(family="Arial", size=32, weight="bold")
        title_label = tk.Label(
            main_frame, 
            text="Flow Bit", 
            font=title_font, 
            fg="#2c3e50", 
            bg="#f0f0f0"
        )
        title_label.pack(pady=(0, 10))
        
        # Subtitle
        subtitle_font = font.Font(family="Arial", size=14, slant="italic")
        subtitle_label = tk.Label(
            main_frame, 
            text="Smart File Organization Made Simple", 
            font=subtitle_font, 
            fg="#7f8c8d", 
            bg="#f0f0f0"
        )
        subtitle_label.pack(pady=(0, 30))
        
        # Welcome message
        welcome_font = font.Font(family="Arial", size=11)
        welcome_text = "Welcome to Flow Bit - your intelligent file organizer!\n\nThis application helps you automatically sort and organize your files into categorized folders."
        welcome_label = tk.Label(
            main_frame, 
            text=welcome_text, 
            font=welcome_font, 
            fg="#34495e", 
            bg="#f0f0f0",
            justify="center"
        )
        welcome_label.pack(pady=(0, 25))
        
        # Features frame
        features_frame = tk.Frame(main_frame, bg="#f0f0f0")
        features_frame.pack(pady=(0, 30))
        
        features_title = tk.Label(
            features_frame, 
            text="Key Features:", 
            font=font.Font(family="Arial", size=12, weight="bold"), 
            fg="#2c3e50", 
            bg="#f0f0f0"
        )
        features_title.pack(anchor="w")
        
        features = [
            "📁 Organize files by type (Images, Documents, Videos, etc.)",
            "📅 Sort files by date into subfolders",
            "🔍 Support for multiple source folders",
            "⚙️ Customizable file type selection",
            "🗑️ Optional empty folder cleanup",
            "📝 Detailed operation logging"
        ]
        
        for feature in features:
            feature_label = tk.Label(
                features_frame, 
                text=f"  {feature}", 
                font=font.Font(family="Arial", size=10), 
                fg="#2c3e50", 
                bg="#f0f0f0",
                anchor="w"
            )
            feature_label.pack(anchor="w", pady=1)
        
        # Button frame
        button_frame = tk.Frame(main_frame, bg="#f0f0f0")
        button_frame.pack(pady=(30, 0), anchor="center")
        
        # Continue button
        continue_button = tk.Button(
            button_frame,
            text="Get Started",
            command=self.continue_to_app,
            bg="#3498db",
            fg="white",
            font=font.Font(family="Arial", size=14, weight="bold"),
            relief="flat",
            padx=40,
            pady=15,
            cursor="hand2"
        )
        continue_button.pack(side="left", padx=(0, 15))
        
        # System Monitor button
        monitor_button = tk.Button(
            button_frame,
            text="System Monitor",
            command=self.open_system_monitor,
            bg="#9b59b6",
            fg="white",
            font=font.Font(family="Arial", size=14, weight="bold"),
            relief="flat",
            padx=40,
            pady=15,
            cursor="hand2"
        )
        monitor_button.pack(side="left", padx=(0, 15))
        
        # Exit button
        exit_button = tk.Button(
            button_frame,
            text="Exit",
            command=self.root.quit,
            bg="#e74c3c",
            fg="white",
            font=font.Font(family="Arial", size=14),
            relief="flat",
            padx=40,
            pady=15,
            cursor="hand2"
        )
        exit_button.pack(side="left")
        
        # Add hover effects
        self.add_hover_effect(continue_button, "#2980b9", "#3498db")
        self.add_hover_effect(monitor_button, "#8e44ad", "#9b59b6")
        self.add_hover_effect(exit_button, "#c0392b", "#e74c3c")
        
    def add_hover_effect(self, button, hover_color, normal_color):
        """Add hover effect to buttons"""
        def on_enter(e):
            button.config(bg=hover_color)
        
        def on_leave(e):
            button.config(bg=normal_color)
        
        button.bind("<Enter>", on_enter)
        button.bind("<Leave>", on_leave)
    
    def continue_to_app(self):
        """Close welcome screen and start main application"""
        self.root.destroy()
        start_main_app()
    
    def open_system_monitor(self):
        """Open system monitor screen"""
        self.root.destroy()
        monitor = SystemMonitorScreen()
        monitor.show()
    
    def show(self):
        """Display the welcome screen"""
        self.root.mainloop()


# --- System Monitor Screen Class ---
class SystemMonitorScreen:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Flow Bit - System Monitor")
        self.root.geometry("900x700")
        self.root.resizable(True, True)
        self.root.configure(bg="#f0f0f0")
        
        # Center the window
        self.center_window()
        
        self.setup_ui()
        self.update_system_info()
        
    def center_window(self):
        """Center the window on the screen"""
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (800 // 2)
        y = (self.root.winfo_screenheight() // 2) - (600 // 2)
        self.root.geometry(f"800x600+{x}+{y}")
    
    def setup_ui(self):
        """Setup the system monitor UI"""
        # Main container
        main_frame = tk.Frame(self.root, bg="#f0f0f0")
        main_frame.pack(expand=True, fill="both", padx=20, pady=20)
        
        # Title
        title_font = font.Font(family="Arial", size=24, weight="bold")
        title_label = tk.Label(
            main_frame, 
            text="System Monitor", 
            font=title_font, 
            fg="#2c3e50", 
            bg="#f0f0f0"
        )
        title_label.pack(pady=(0, 20))
        
        # CPU Performance Frame
        cpu_frame = tk.LabelFrame(main_frame, text="CPU Performance", font=font.Font(family="Arial", size=12, weight="bold"), 
                                  bg="#f0f0f0", fg="#2c3e50", padx=10, pady=10)
        cpu_frame.pack(fill="x", pady=(0, 10))
        
        self.cpu_label = tk.Label(cpu_frame, text="CPU Usage: Loading...", 
                                  font=font.Font(family="Arial", size=11), 
                                  bg="#f0f0f0", fg="#2c3e50")
        self.cpu_label.pack(anchor="w")
        
        self.cpu_cores_label = tk.Label(cpu_frame, text="CPU Cores: Loading...", 
                                        font=font.Font(family="Arial", size=11), 
                                        bg="#f0f0f0", fg="#2c3e50")
        self.cpu_cores_label.pack(anchor="w")
        
        self.cpu_freq_label = tk.Label(cpu_frame, text="CPU Frequency: Loading...", 
                                       font=font.Font(family="Arial", size=11), 
                                       bg="#f0f0f0", fg="#2c3e50")
        self.cpu_freq_label.pack(anchor="w")
        
        # Memory Information Frame
        memory_frame = tk.LabelFrame(main_frame, text="Memory Information", 
                                     font=font.Font(family="Arial", size=12, weight="bold"), 
                                     bg="#f0f0f0", fg="#2c3e50", padx=10, pady=10)
        memory_frame.pack(fill="x", pady=(0, 10))
        
        self.memory_label = tk.Label(memory_frame, text="Memory Usage: Loading...", 
                                     font=font.Font(family="Arial", size=11), 
                                     bg="#f0f0f0", fg="#2c3e50")
        self.memory_label.pack(anchor="w")
        
        # Running Processes Frame
        processes_frame = tk.LabelFrame(main_frame, text="Running Processes", 
                                        font=font.Font(family="Arial", size=12, weight="bold"), 
                                        bg="#f0f0f0", fg="#2c3e50", padx=10, pady=10)
        processes_frame.pack(fill="both", expand=True, pady=(0, 10))
        
        # Process count
        self.process_count_label = tk.Label(processes_frame, text="Total Processes: Loading...", 
                                            font=font.Font(family="Arial", size=11, weight="bold"), 
                                            bg="#f0f0f0", fg="#2c3e50")
        self.process_count_label.pack(anchor="w", pady=(0, 5))
        
        # Process list with scrollbar
        process_frame = tk.Frame(processes_frame, bg="#f0f0f0")
        process_frame.pack(fill="both", expand=True)
        
        self.process_text = scrolledtext.ScrolledText(process_frame, height=15, width=90,
                                                      font=font.Font(family="Courier", size=9))
        self.process_text.pack(fill="both", expand=True)
        
        # Control buttons frame
        button_frame = tk.Frame(main_frame, bg="#f0f0f0")
        button_frame.pack(pady=(10, 0))
        
        # Refresh button
        refresh_button = tk.Button(
            button_frame,
            text="Refresh",
            command=self.refresh_data,
            bg="#3498db",
            fg="white",
            font=font.Font(family="Arial", size=12),
            relief="flat",
            padx=20,
            pady=8,
            cursor="hand2"
        )
        refresh_button.pack(side="left", padx=(0, 10))
        
        # Back to welcome button
        back_button = tk.Button(
            button_frame,
            text="Back to Welcome",
            command=self.back_to_welcome,
            bg="#95a5a6",
            fg="white",
            font=font.Font(family="Arial", size=12),
            relief="flat",
            padx=20,
            pady=8,
            cursor="hand2"
        )
        back_button.pack(side="left", padx=(0, 10))
        
        # File Manager button
        file_manager_button = tk.Button(
            button_frame,
            text="File Manager",
            command=self.open_file_manager,
            bg="#27ae60",
            fg="white",
            font=font.Font(family="Arial", size=12),
            relief="flat",
            padx=20,
            pady=8,
            cursor="hand2"
        )
        file_manager_button.pack(side="left")
        
        # Add hover effects
        self.add_hover_effect(refresh_button, "#2980b9", "#3498db")
        self.add_hover_effect(back_button, "#7f8c8d", "#95a5a6")
        self.add_hover_effect(file_manager_button, "#229954", "#27ae60")
    
    def add_hover_effect(self, button, hover_color, normal_color):
        """Add hover effect to buttons"""
        def on_enter(e):
            button.config(bg=hover_color)
        
        def on_leave(e):
            button.config(bg=normal_color)
        
        button.bind("<Enter>", on_enter)
        button.bind("<Leave>", on_leave)
    
    def get_system_info(self):
        """Get system information using psutil or fallback methods"""
        try:
            # Try to use psutil if available
            cpu_percent = psutil.cpu_percent(interval=1)
            cpu_count = psutil.cpu_count()
            cpu_freq = psutil.cpu_freq()
            memory = psutil.virtual_memory()
            processes = list(psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']))
            
            return {
                'cpu_percent': cpu_percent,
                'cpu_count': cpu_count,
                'cpu_freq': cpu_freq.current if cpu_freq else 'N/A',
                'memory_percent': memory.percent,
                'memory_total': memory.total,
                'memory_used': memory.used,
                'processes': processes
            }
        except ImportError:
            # Fallback when psutil is not available
            return self.get_fallback_system_info()
    
    def get_fallback_system_info(self):
        """Get basic system info without psutil"""
        import platform
        
        # Get CPU count
        cpu_count = os.cpu_count()
        
        # Get basic process count using os
        try:
            if platform.system() == "Windows":
                import subprocess
                result = subprocess.run(['tasklist', '/fo', 'csv'], capture_output=True, text=True)
                process_count = len(result.stdout.strip().split('\n')) - 1  # Subtract header
                processes = []
                lines = result.stdout.strip().split('\n')[1:]  # Skip header
                for line in lines[:20]:  # Show first 20 processes
                    parts = line.split('","')
                    if len(parts) >= 2:
                        processes.append({
                            'name': parts[0].strip('"'),
                            'pid': parts[1].strip('"'),
                            'cpu_percent': 'N/A',
                            'memory_percent': 'N/A'
                        })
            else:
                processes = []
                process_count = 0
        except:
            processes = []
            process_count = 0
        
        return {
            'cpu_percent': 'N/A (psutil not installed)',
            'cpu_count': cpu_count,
            'cpu_freq': 'N/A',
            'memory_percent': 'N/A (psutil not installed)',
            'memory_total': 'N/A',
            'memory_used': 'N/A',
            'processes': processes,
            'process_count': process_count
        }
    
    def update_system_info(self):
        """Update system information display"""
        info = self.get_system_info()
        
        # Update CPU information
        self.cpu_label.config(text=f"CPU Usage: {info['cpu_percent']}%")
        self.cpu_cores_label.config(text=f"CPU Cores: {info['cpu_count']}")
        self.cpu_freq_label.config(text=f"CPU Frequency: {info['cpu_freq']} MHz")
        
        # Update memory information
        if info['memory_percent'] != 'N/A (psutil not installed)':
            memory_gb_total = info['memory_total'] / (1024**3)
            memory_gb_used = info['memory_used'] / (1024**3)
            self.memory_label.config(text=f"Memory Usage: {info['memory_percent']:.1f}% ({memory_gb_used:.1f}GB / {memory_gb_total:.1f}GB)")
        else:
            self.memory_label.config(text="Memory Usage: N/A (psutil not installed)")
        
        # Update process information
        processes = info['processes']
        if hasattr(info, 'process_count'):
            process_count = info['process_count']
        else:
            process_count = len(processes)
        
        self.process_count_label.config(text=f"Total Processes: {process_count}")
        
        # Clear and update process list
        self.process_text.delete(1.0, tk.END)
        self.process_text.insert(tk.END, f"{'PID':<8} {'Name':<30} {'CPU%':<8} {'Memory%':<10}\n")
        self.process_text.insert(tk.END, "-" * 60 + "\n")
        
        for proc in processes[:20]:  # Show top 20 processes
            try:
                if hasattr(proc, 'info'):
                    # psutil process object
                    pid = proc.info['pid']
                    name = proc.info['name'][:28]
                    cpu = f"{proc.info['cpu_percent']:.1f}" if proc.info['cpu_percent'] is not None else "N/A"
                    memory = f"{proc.info['memory_percent']:.1f}" if proc.info['memory_percent'] is not None else "N/A"
                else:
                    # Fallback process dict
                    pid = proc['pid']
                    name = proc['name'][:28]
                    cpu = proc['cpu_percent']
                    memory = proc['memory_percent']
                
                self.process_text.insert(tk.END, f"{pid:<8} {name:<30} {cpu:<8} {memory:<10}\n")
            except:
                continue
    
    def refresh_data(self):
        """Refresh system data"""
        self.update_system_info()
    
    def back_to_welcome(self):
        """Go back to welcome screen"""
        self.root.destroy()
        welcome = WelcomeScreen()
        welcome.show()
    
    def open_file_manager(self):
        """Open the file manager (main app)"""
        self.root.destroy()
        start_main_app()
    
    def show(self):
        """Display the system monitor screen"""
        self.root.mainloop()



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
    "Code": [".py", ".cpp", ".c", ".java", ".js", ".html", ".css"],
    "Executables": [".exe", ".bat", ".sh"],
    "Others": []  # Catch-all for uncategorized files
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



# --- Main Application Function ---
def start_main_app():
    """Start the main file sorting application"""
    # --- GUI Setup ---
    root = tk.Tk()
    root.title("Flow Bit - File Manager")
    root.geometry("800x750")
    root.resizable(True, True)
    root.configure(bg="#f0f0f0")
    
    # Center the window
    def center_window():
        root.update_idletasks()
        x = (root.winfo_screenwidth() // 2) - (800 // 2)
        y = (root.winfo_screenheight() // 2) - (750 // 2)
        root.geometry(f"800x750+{x}+{y}")
    
    center_window()
    
    # Main container
    main_frame = tk.Frame(root, bg="#f0f0f0")
    main_frame.pack(expand=True, fill="both", padx=20, pady=20)
    
    # Title
    title_font = font.Font(family="Arial", size=24, weight="bold")
    title_label = tk.Label(
        main_frame, 
        text="File Manager", 
        font=title_font, 
        fg="#2c3e50", 
        bg="#f0f0f0"
    )
    title_label.pack(pady=(0, 20))

    # --- Source Folders Section ---
    source_frame = tk.LabelFrame(
        main_frame, 
        text="Source Folders", 
        font=font.Font(family="Arial", size=12, weight="bold"), 
        bg="#f0f0f0", 
        fg="#2c3e50", 
        padx=15, 
        pady=15
    )
    source_frame.pack(fill="x", pady=(0, 15))
    
    tk.Label(
        source_frame, 
        text="Select source folders (multiple folders separated by semicolon):", 
        font=font.Font(family="Arial", size=10), 
        fg="#2c3e50", 
        bg="#f0f0f0"
    ).pack(anchor="w", pady=(0, 5))
    
    src_entry = tk.Entry(
        source_frame, 
        width=70, 
        font=font.Font(family="Arial", size=10),
        relief="solid",
        borderwidth=1
    )
    src_entry.pack(fill="x", pady=(0, 10))
    
    add_folder_button = tk.Button(
        source_frame, 
        text="📁 Add Folder", 
        command=lambda: choose_folders(src_entry),
        bg="#3498db",
        fg="white",
        font=font.Font(family="Arial", size=10, weight="bold"),
        relief="flat",
        padx=15,
        pady=8,
        cursor="hand2"
    )
    add_folder_button.pack(anchor="w")

    # --- Destination Folder Section ---
    dest_frame = tk.LabelFrame(
        main_frame, 
        text="Destination Folder", 
        font=font.Font(family="Arial", size=12, weight="bold"), 
        bg="#f0f0f0", 
        fg="#2c3e50", 
        padx=15, 
        pady=15
    )
    dest_frame.pack(fill="x", pady=(0, 15))
    
    tk.Label(
        dest_frame, 
        text="Select where organized files should be saved:", 
        font=font.Font(family="Arial", size=10), 
        fg="#2c3e50", 
        bg="#f0f0f0"
    ).pack(anchor="w", pady=(0, 5))
    
    dest_entry = tk.Entry(
        dest_frame, 
        width=70, 
        font=font.Font(family="Arial", size=10),
        relief="solid",
        borderwidth=1
    )
    dest_entry.pack(fill="x", pady=(0, 10))
    
    # Function to select destination folder
    def choose_folder(entry_widget):
        folder = filedialog.askdirectory()
        if folder:
            entry_widget.delete(0, tk.END)
            entry_widget.insert(0, folder)
    
    browse_button = tk.Button(
        dest_frame, 
        text="📂 Browse", 
        command=lambda: choose_folder(dest_entry),
        bg="#27ae60",
        fg="white",
        font=font.Font(family="Arial", size=10, weight="bold"),
        relief="flat",
        padx=15,
        pady=8,
        cursor="hand2"
    )
    browse_button.pack(anchor="w")

    # --- File Type Selection Section ---
    filetype_frame = tk.LabelFrame(
        main_frame, 
        text="File Type Selection", 
        font=font.Font(family="Arial", size=12, weight="bold"), 
        bg="#f0f0f0", 
        fg="#2c3e50", 
        padx=15, 
        pady=15
    )
    filetype_frame.pack(fill="x", pady=(0, 15))
    
    tk.Label(
        filetype_frame, 
        text="Choose which file types to organize:", 
        font=font.Font(family="Arial", size=10), 
        fg="#2c3e50", 
        bg="#f0f0f0"
    ).pack(anchor="w", pady=(0, 10))
    
    file_type_vars = {}
    checkbox_frame = tk.Frame(filetype_frame, bg="#f0f0f0")
    checkbox_frame.pack(fill="x")
    
    for i, category in enumerate(FILE_TYPES.keys()):
        var = tk.BooleanVar(value=True)
        file_type_vars[category] = var
        cb = tk.Checkbutton(
            checkbox_frame, 
            text=category, 
            variable=var,
            font=font.Font(family="Arial", size=10),
            fg="#2c3e50",
            bg="#f0f0f0",
            selectcolor="#ffffff",
            activebackground="#f0f0f0",
            activeforeground="#2c3e50"
        )
        cb.grid(row=i//4, column=i%4, sticky="w", padx=10, pady=5)

    # --- Options Section ---
    options_frame = tk.LabelFrame(
        main_frame, 
        text="Organization Options", 
        font=font.Font(family="Arial", size=12, weight="bold"), 
        bg="#f0f0f0", 
        fg="#2c3e50", 
        padx=15, 
        pady=15
    )
    options_frame.pack(fill="x", pady=(0, 15))

    # --- Sort by date option checkbox ---
    sort_by_date_var = tk.BooleanVar(value=True)
    date_cb = tk.Checkbutton(
        options_frame, 
        text="📅 Sort files by date (create date-based subfolders)", 
        variable=sort_by_date_var,
        font=font.Font(family="Arial", size=10),
        fg="#2c3e50",
        bg="#f0f0f0",
        selectcolor="#ffffff",
        activebackground="#f0f0f0",
        activeforeground="#2c3e50"
    )
    date_cb.pack(anchor="w", pady=5)

    # --- Delete empty folders option checkbox ---
    delete_empty_var = tk.BooleanVar(value=False)
    delete_cb = tk.Checkbutton(
        options_frame,
        text="🗑️ Delete empty source folders after sorting (⚠️ Use with caution)",
        variable=delete_empty_var,
        font=font.Font(family="Arial", size=10),
        fg="#e74c3c",
        bg="#f0f0f0",
        selectcolor="#ffffff",
        activebackground="#f0f0f0",
        activeforeground="#e74c3c"
    )
    delete_cb.pack(anchor="w", pady=5)


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

    # --- Action Buttons Section ---
    action_frame = tk.Frame(main_frame, bg="#f0f0f0")
    action_frame.pack(pady=(20, 15))

    sort_button = tk.Button(
        action_frame,
        text="🔄 Sort Files",
        command=on_sort,
        bg="#3498db",
        fg="white",
        font=font.Font(family="Arial", size=14, weight="bold"),
        relief="flat",
        padx=30,
        pady=12,
        cursor="hand2"
    )
    sort_button.pack(side="left", padx=(0, 15))

    def go_back():
        root.destroy()
        welcome = WelcomeScreen()
        welcome.show()

    back_button = tk.Button(
        action_frame,
        text="🏠 Back to Welcome",
        command=go_back,
        bg="#95a5a6",
        fg="white",
        font=font.Font(family="Arial", size=14),
        relief="flat",
        padx=30,
        pady=12,
        cursor="hand2"
    )
    back_button.pack(side="left", padx=(0, 15))
    
    def open_system_monitor():
        root.destroy()
        monitor = SystemMonitorScreen()
        monitor.show()
    
    monitor_button = tk.Button(
        action_frame,
        text="📊 System Monitor",
        command=open_system_monitor,
        bg="#9b59b6",
        fg="white",
        font=font.Font(family="Arial", size=14),
        relief="flat",
        padx=30,
        pady=12,
        cursor="hand2"
    )
    monitor_button.pack(side="left")

    # Add hover effects to buttons
    def add_hover_effect(button, hover_color, normal_color):
        def on_enter(e):
            button.config(bg=hover_color)
        def on_leave(e):
            button.config(bg=normal_color)
        button.bind("<Enter>", on_enter)
        button.bind("<Leave>", on_leave)
    
    add_hover_effect(add_folder_button, "#2980b9", "#3498db")
    add_hover_effect(browse_button, "#229954", "#27ae60")
    add_hover_effect(sort_button, "#2980b9", "#3498db")
    add_hover_effect(back_button, "#7f8c8d", "#95a5a6")
    add_hover_effect(monitor_button, "#8e44ad", "#9b59b6")

    # --- Log Section ---
    log_frame = tk.LabelFrame(
        main_frame, 
        text="Operation Log", 
        font=font.Font(family="Arial", size=12, weight="bold"), 
        bg="#f0f0f0", 
        fg="#2c3e50", 
        padx=15, 
        pady=15
    )
    log_frame.pack(fill="both", expand=True, pady=(0, 10))
    
    tk.Label(
        log_frame, 
        text="File sorting progress and results will be displayed here:", 
        font=font.Font(family="Arial", size=10), 
        fg="#2c3e50", 
        bg="#f0f0f0"
    ).pack(anchor="w", pady=(0, 5))
    
    log_box = scrolledtext.ScrolledText(
        log_frame, 
        width=80, 
        height=10, 
        state='normal',
        font=font.Font(family="Courier", size=9),
        bg="#ffffff",
        fg="#2c3e50",
        relief="solid",
        borderwidth=1
    )
    log_box.pack(fill="both", expand=True)

    # --- Start the GUI event loop ---
    root.mainloop()


# --- Application Entry Point ---
if __name__ == "__main__":
    # Show welcome screen first
    welcome = WelcomeScreen()
    welcome.show()
