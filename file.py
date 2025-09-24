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


# --- Pomodoro Timer Class ---
class PomodoroTimer:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Flow Bit - Pomodoro Timer")
        self.root.geometry("600x700")
        self.root.resizable(False, False)
        self.root.configure(bg="#f0f0f0")
        
        # Timer state variables
        self.work_duration = 25 * 60  # 25 minutes in seconds
        self.short_break = 5 * 60     # 5 minutes
        self.long_break = 15 * 60     # 15 minutes
        self.current_duration = self.work_duration
        self.time_left = self.work_duration
        self.is_running = False
        self.is_break = False
        self.session_count = 0
        self.timer_thread = None
        
        # Statistics
        self.completed_sessions = 0
        self.total_focus_time = 0
        
        # Center the window
        self.center_window()
        self.setup_ui()
        self.update_display()
        
    def center_window(self):
        """Center the window on the screen"""
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (600 // 2)
        y = (self.root.winfo_screenheight() // 2) - (700 // 2)
        self.root.geometry(f"600x700+{x}+{y}")
    
    def setup_ui(self):
        """Setup the Pomodoro timer UI"""
        # Main container
        main_frame = tk.Frame(self.root, bg="#f0f0f0")
        main_frame.pack(expand=True, fill="both", padx=30, pady=30)
        
        # Title
        title_font = font.Font(family="Arial", size=28, weight="bold")
        title_label = tk.Label(
            main_frame, 
            text="🍅 Pomodoro Timer", 
            font=title_font, 
            fg="#e74c3c", 
            bg="#f0f0f0"
        )
        title_label.pack(pady=(0, 20))
        
        # Current session type
        self.session_label = tk.Label(
            main_frame,
            text="Work Session",
            font=font.Font(family="Arial", size=16, weight="bold"),
            fg="#2c3e50",
            bg="#f0f0f0"
        )
        self.session_label.pack(pady=(0, 10))
        
        # Timer display
        timer_frame = tk.Frame(main_frame, bg="#ffffff", relief="solid", borderwidth=2)
        timer_frame.pack(pady=(0, 20), padx=20, fill="x")
        
        self.time_display = tk.Label(
            timer_frame,
            text="25:00",
            font=font.Font(family="Arial", size=48, weight="bold"),
            fg="#2c3e50",
            bg="#ffffff",
            pady=30
        )
        self.time_display.pack()
        
        # Progress indicator
        self.progress_label = tk.Label(
            main_frame,
            text="Session 1 of 4",
            font=font.Font(family="Arial", size=12),
            fg="#7f8c8d",
            bg="#f0f0f0"
        )
        self.progress_label.pack(pady=(0, 20))
        
        # Control buttons frame
        control_frame = tk.Frame(main_frame, bg="#f0f0f0")
        control_frame.pack(pady=(0, 30))
        
        # Start/Pause button
        self.start_button = tk.Button(
            control_frame,
            text="▶️ Start",
            command=self.toggle_timer,
            bg="#27ae60",
            fg="white",
            font=font.Font(family="Arial", size=14, weight="bold"),
            relief="flat",
            padx=25,
            pady=12,
            cursor="hand2"
        )
        self.start_button.pack(side="left", padx=(0, 15))
        
        # Reset button
        reset_button = tk.Button(
            control_frame,
            text="🔄 Reset",
            command=self.reset_timer,
            bg="#f39c12",
            fg="white",
            font=font.Font(family="Arial", size=14, weight="bold"),
            relief="flat",
            padx=25,
            pady=12,
            cursor="hand2"
        )
        reset_button.pack(side="left", padx=(0, 15))
        
        # Skip button
        skip_button = tk.Button(
            control_frame,
            text="⏭️ Skip",
            command=self.skip_session,
            bg="#95a5a6",
            fg="white",
            font=font.Font(family="Arial", size=14, weight="bold"),
            relief="flat",
            padx=25,
            pady=12,
            cursor="hand2"
        )
        skip_button.pack(side="left")
        
        # Settings frame
        settings_frame = tk.LabelFrame(
            main_frame,
            text="Timer Settings",
            font=font.Font(family="Arial", size=12, weight="bold"),
            bg="#f0f0f0",
            fg="#2c3e50",
            padx=15,
            pady=15
        )
        settings_frame.pack(fill="x", pady=(0, 20))
        
        # Work duration setting
        work_frame = tk.Frame(settings_frame, bg="#f0f0f0")
        work_frame.pack(fill="x", pady=5)
        
        tk.Label(work_frame, text="Work Duration (minutes):", 
                font=font.Font(family="Arial", size=10), 
                bg="#f0f0f0", fg="#2c3e50").pack(side="left")
        
        self.work_var = tk.StringVar(value="25")
        work_spinbox = tk.Spinbox(work_frame, from_=1, to=60, width=10, 
                                 textvariable=self.work_var,
                                 font=font.Font(family="Arial", size=10))
        work_spinbox.pack(side="right")
        
        # Short break duration setting
        short_break_frame = tk.Frame(settings_frame, bg="#f0f0f0")
        short_break_frame.pack(fill="x", pady=5)
        
        tk.Label(short_break_frame, text="Short Break (minutes):", 
                font=font.Font(family="Arial", size=10), 
                bg="#f0f0f0", fg="#2c3e50").pack(side="left")
        
        self.short_break_var = tk.StringVar(value="5")
        short_break_spinbox = tk.Spinbox(short_break_frame, from_=1, to=30, width=10,
                                        textvariable=self.short_break_var,
                                        font=font.Font(family="Arial", size=10))
        short_break_spinbox.pack(side="right")
        
        # Long break duration setting
        long_break_frame = tk.Frame(settings_frame, bg="#f0f0f0")
        long_break_frame.pack(fill="x", pady=5)
        
        tk.Label(long_break_frame, text="Long Break (minutes):", 
                font=font.Font(family="Arial", size=10), 
                bg="#f0f0f0", fg="#2c3e50").pack(side="left")
        
        self.long_break_var = tk.StringVar(value="15")
        long_break_spinbox = tk.Spinbox(long_break_frame, from_=1, to=60, width=10,
                                       textvariable=self.long_break_var,
                                       font=font.Font(family="Arial", size=10))
        long_break_spinbox.pack(side="right")
        
        # Statistics frame
        stats_frame = tk.LabelFrame(
            main_frame,
            text="Today's Statistics",
            font=font.Font(family="Arial", size=12, weight="bold"),
            bg="#f0f0f0",
            fg="#2c3e50",
            padx=15,
            pady=15
        )
        stats_frame.pack(fill="x", pady=(0, 20))
        
        self.completed_label = tk.Label(
            stats_frame,
            text="Completed Sessions: 0",
            font=font.Font(family="Arial", size=11),
            bg="#f0f0f0",
            fg="#2c3e50"
        )
        self.completed_label.pack(anchor="w", pady=2)
        
        self.focus_time_label = tk.Label(
            stats_frame,
            text="Total Focus Time: 0 minutes",
            font=font.Font(family="Arial", size=11),
            bg="#f0f0f0",
            fg="#2c3e50"
        )
        self.focus_time_label.pack(anchor="w", pady=2)
        
        # Navigation buttons
        nav_frame = tk.Frame(main_frame, bg="#f0f0f0")
        nav_frame.pack(pady=(20, 0))
        
        # Back to welcome button
        back_button = tk.Button(
            nav_frame,
            text="🏠 Back to Welcome",
            command=self.back_to_welcome,
            bg="#3498db",
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
            nav_frame,
            text="📁 File Manager",
            command=self.open_file_manager,
            bg="#27ae60",
            fg="white",
            font=font.Font(family="Arial", size=12),
            relief="flat",
            padx=20,
            pady=8,
            cursor="hand2"
        )
        file_manager_button.pack(side="left", padx=(0, 10))
        
        # System Monitor button
        monitor_button = tk.Button(
            nav_frame,
            text="📊 System Monitor",
            command=self.open_system_monitor,
            bg="#9b59b6",
            fg="white",
            font=font.Font(family="Arial", size=12),
            relief="flat",
            padx=20,
            pady=8,
            cursor="hand2"
        )
        monitor_button.pack(side="left")
        
        # Add hover effects
        self.add_hover_effect(self.start_button, "#229954", "#27ae60")
        self.add_hover_effect(reset_button, "#e67e22", "#f39c12")
        self.add_hover_effect(skip_button, "#7f8c8d", "#95a5a6")
        self.add_hover_effect(back_button, "#2980b9", "#3498db")
        self.add_hover_effect(file_manager_button, "#229954", "#27ae60")
        self.add_hover_effect(monitor_button, "#8e44ad", "#9b59b6")
    
    def add_hover_effect(self, button, hover_color, normal_color):
        """Add hover effect to buttons"""
        def on_enter(e):
            button.config(bg=hover_color)
        
        def on_leave(e):
            button.config(bg=normal_color)
        
        button.bind("<Enter>", on_enter)
        button.bind("<Leave>", on_leave)
    
    def update_settings(self):
        """Update timer durations from settings"""
        if not self.is_running:
            self.work_duration = int(self.work_var.get()) * 60
            self.short_break = int(self.short_break_var.get()) * 60
            self.long_break = int(self.long_break_var.get()) * 60
            
            if not self.is_break:
                self.current_duration = self.work_duration
                self.time_left = self.work_duration
            
            self.update_display()
    
    def toggle_timer(self):
        """Start or pause the timer"""
        if self.is_running:
            self.pause_timer()
        else:
            self.start_timer()
    
    def start_timer(self):
        """Start the timer"""
        self.update_settings()
        self.is_running = True
        self.start_button.config(text="⏸️ Pause", bg="#e74c3c")
        
        # Start timer thread
        self.timer_thread = threading.Thread(target=self.run_timer)
        self.timer_thread.daemon = True
        self.timer_thread.start()
    
    def pause_timer(self):
        """Pause the timer"""
        self.is_running = False
        self.start_button.config(text="▶️ Start", bg="#27ae60")
    
    def reset_timer(self):
        """Reset the timer to initial state"""
        self.is_running = False
        self.is_break = False
        self.session_count = 0
        self.update_settings()
        self.start_button.config(text="▶️ Start", bg="#27ae60")
        self.session_label.config(text="Work Session", fg="#2c3e50")
        self.progress_label.config(text="Session 1 of 4")
        self.update_display()
    
    def skip_session(self):
        """Skip current session"""
        self.time_left = 0
        if not self.is_running:
            self.next_session()
    
    def run_timer(self):
        """Main timer loop"""
        while self.is_running and self.time_left > 0:
            time.sleep(1)
            if self.is_running:
                self.time_left -= 1
                self.root.after(0, self.update_display)
        
        if self.time_left <= 0:
            self.root.after(0, self.timer_finished)
    
    def timer_finished(self):
        """Handle timer completion"""
        self.is_running = False
        
        if not self.is_break:
            # Work session completed
            self.completed_sessions += 1
            self.total_focus_time += int(self.work_var.get())
            self.update_statistics()
            
            # Show completion message
            messagebox.showinfo("Session Complete!", 
                              f"Work session {self.session_count + 1} completed!\nTime for a break!")
        else:
            # Break completed
            messagebox.showinfo("Break Over!", "Break time is over!\nReady for the next work session?")
        
        self.next_session()
    
    def next_session(self):
        """Move to next session"""
        if not self.is_break:
            # Moving from work to break
            self.session_count += 1
            self.is_break = True
            
            # Determine break type (long break every 4 sessions)
            if self.session_count % 4 == 0:
                self.current_duration = self.long_break
                self.session_label.config(text="Long Break", fg="#9b59b6")
            else:
                self.current_duration = self.short_break
                self.session_label.config(text="Short Break", fg="#3498db")
        else:
            # Moving from break to work
            self.is_break = False
            self.current_duration = self.work_duration
            self.session_label.config(text="Work Session", fg="#2c3e50")
        
        self.time_left = self.current_duration
        self.start_button.config(text="▶️ Start", bg="#27ae60")
        
        # Update progress
        current_session = (self.session_count % 4) + 1 if not self.is_break else self.session_count % 4
        if current_session == 0:
            current_session = 4
        self.progress_label.config(text=f"Session {current_session} of 4")
        
        self.update_display()
    
    def update_display(self):
        """Update timer display"""
        minutes = self.time_left // 60
        seconds = self.time_left % 60
        time_string = f"{minutes:02d}:{seconds:02d}"
        self.time_display.config(text=time_string)
        
        # Change color based on time remaining
        if self.time_left <= 60 and self.is_running:  # Last minute
            self.time_display.config(fg="#e74c3c")
        elif self.is_break:
            self.time_display.config(fg="#3498db")
        else:
            self.time_display.config(fg="#2c3e50")
    
    def update_statistics(self):
        """Update statistics display"""
        self.completed_label.config(text=f"Completed Sessions: {self.completed_sessions}")
        hours = self.total_focus_time // 60
        minutes = self.total_focus_time % 60
        if hours > 0:
            time_str = f"{hours}h {minutes}m"
        else:
            time_str = f"{minutes} minutes"
        self.focus_time_label.config(text=f"Total Focus Time: {time_str}")
    
    def back_to_welcome(self):
        """Go back to welcome screen"""
        if self.is_running:
            if messagebox.askyesno("Timer Running", 
                                 "Timer is still running. Are you sure you want to go back?"):
                self.is_running = False
                self.root.destroy()
                welcome = WelcomeScreen()
                welcome.show()
        else:
            self.root.destroy()
            welcome = WelcomeScreen()
            welcome.show()
    
    def open_file_manager(self):
        """Open file manager"""
        if self.is_running:
            if messagebox.askyesno("Timer Running", 
                                 "Timer is still running. Are you sure you want to switch?"):
                self.is_running = False
                self.root.destroy()
                start_main_app()
        else:
            self.root.destroy()
            start_main_app()
    
    def open_system_monitor(self):
        """Open system monitor"""
        if self.is_running:
            if messagebox.askyesno("Timer Running", 
                                 "Timer is still running. Are you sure you want to switch?"):
                self.is_running = False
                self.root.destroy()
                monitor = SystemMonitorScreen()
                monitor.show()
        else:
            self.root.destroy()
            monitor = SystemMonitorScreen()
            monitor.show()
    
    def show(self):
        """Display the Pomodoro timer"""
        # Handle window closing
        def on_closing():
            if self.is_running:
                if messagebox.askyesno("Timer Running", 
                                     "Timer is still running. Are you sure you want to exit?"):
                    self.is_running = False
                    self.root.destroy()
            else:
                self.root.destroy()
        
        self.root.protocol("WM_DELETE_WINDOW", on_closing)
        self.root.mainloop()


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
            text="Smart File Organization & Productivity Suite", 
            font=subtitle_font, 
            fg="#7f8c8d", 
            bg="#f0f0f0"
        )
        subtitle_label.pack(pady=(0, 30))
        
        # Welcome message
        welcome_font = font.Font(family="Arial", size=11)
        welcome_text = "Welcome to Flow Bit - your intelligent productivity companion!\n\nThis application helps you organize files and stay focused with productivity tools."
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
            "🍅 Pomodoro timer for focused work sessions",
            "📊 System performance monitoring",
            "🔍 Support for multiple source folders",
            "⚙️ Customizable settings and preferences"
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
        
        # File Manager button
        file_manager_button = tk.Button(
            button_frame,
            text="📁 File Manager",
            command=self.open_file_manager,
            bg="#3498db",
            fg="white",
            font=font.Font(family="Arial", size=12, weight="bold"),
            relief="flat",
            padx=25,
            pady=12,
            cursor="hand2"
        )
        file_manager_button.grid(row=0, column=0, padx=10, pady=5)
        
        # Pomodoro Timer button
        pomodoro_button = tk.Button(
            button_frame,
            text="🍅 Pomodoro Timer",
            command=self.open_pomodoro,
            bg="#e74c3c",
            fg="white",
            font=font.Font(family="Arial", size=12, weight="bold"),
            relief="flat",
            padx=25,
            pady=12,
            cursor="hand2"
        )
        pomodoro_button.grid(row=0, column=1, padx=10, pady=5)
        
        # System Monitor button
        monitor_button = tk.Button(
            button_frame,
            text="📊 System Monitor",
            command=self.open_system_monitor,
            bg="#9b59b6",
            fg="white",
            font=font.Font(family="Arial", size=12, weight="bold"),
            relief="flat",
            padx=25,
            pady=12,
            cursor="hand2"
        )
        monitor_button.grid(row=1, column=0, padx=10, pady=5)
        
        # Exit button
        exit_button = tk.Button(
            button_frame,
            text="❌ Exit",
            command=self.root.quit,
            bg="#95a5a6",
            fg="white",
            font=font.Font(family="Arial", size=12),
            relief="flat",
            padx=25,
            pady=12,
            cursor="hand2"
        )
        exit_button.grid(row=1, column=1, padx=10, pady=5)
        
        # Add hover effects
        self.add_hover_effect(file_manager_button, "#2980b9", "#3498db")
        self.add_hover_effect(pomodoro_button, "#c0392b", "#e74c3c")
        self.add_hover_effect(monitor_button, "#8e44ad", "#9b59b6")
        self.add_hover_effect(exit_button, "#7f8c8d", "#95a5a6")
        
    def add_hover_effect(self, button, hover_color, normal_color):
        """Add hover effect to buttons"""
        def on_enter(e):
            button.config(bg=hover_color)
        
        def on_leave(e):
            button.config(bg=normal_color)
        
        button.bind("<Enter>", on_enter)
        button.bind("<Leave>", on_leave)
    
    def open_file_manager(self):
        """Close welcome screen and start file manager"""
        self.root.destroy()
        start_main_app()
    
    def open_pomodoro(self):
        """Open Pomodoro timer"""
        self.root.destroy()
        timer = PomodoroTimer()
        timer.show()
    
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
        file_manager_button.pack(side="left", padx=(0, 10))
        
        # Pomodoro Timer button
        pomodoro_button = tk.Button(
            button_frame,
            text="Pomodoro Timer",
            command=self.open_pomodoro_timer,
            bg="#e74c3c",
            fg="white",
            font=font.Font(family="Arial", size=12),
            relief="flat",
            padx=20,
            pady=8,
            cursor="hand2"
        )
        pomodoro_button.pack(side="left")
        
        # Add hover effects
        self.add_hover_effect(refresh_button, "#2980b9", "#3498db")
        self.add_hover_effect(back_button, "#7f8c8d", "#95a5a6")
        self.add_hover_effect(file_manager_button, "#229954", "#27ae60")
        self.add_hover_effect(pomodoro_button, "#c0392b", "#e74c3c")
    
    def add_hover_effect(self, button, hover_color, normal_color):
        """Add hover effect to buttons"""
        def on_enter(e):
            button.config(bg=hover_color)
        
        def on_leave(e):
            button.config(bg=normal_color)
        
        button.bind("<Enter>", on_enter)
        button.bind("<Leave>", on_leave)

        
#    system management info code 
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
    
    def open_pomodoro_timer(self):
        """Open Pomodoro timer"""
        self.root.destroy()
        timer = PomodoroTimer()
        timer.show()
    
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


# --- Application Entry Point ---
if __name__ == "__main__":
    # Show welcome screen first
    welcome = WelcomeScreen()
    welcome.show()