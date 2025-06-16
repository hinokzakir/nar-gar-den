import tkinter as tk
from tkinter import ttk, font
import json
from datetime import datetime
import time
import threading
import subprocess
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class FileWatcher(FileSystemEventHandler):
    def __init__(self, callback):
        self.callback = callback

    def on_modified(self, event):
        if not event.is_directory and event.src_path.endswith('settings.txt'):
            print("settings.txt modified, triggering data update")
            self.callback()

class BusDisplay:
    def __init__(self, root):
        self.root = root
        self.root.title("Bussavgångar Ålidhem Centrum")
        self.root.configure(bg='black')
        
        # Make window fullscreen
        self.root.attributes('-fullscreen', True)
        
        # Load settings
        self.load_settings()
        
        # Configure fonts
        self.setup_fonts()
        
        # Create main container
        self.main_frame = ttk.Frame(root, style='Platform.TLabel')
        self.main_frame.pack(expand=True, fill='both', padx=20, pady=20)
        
        # Create last update label
        self.last_update_label = ttk.Label(root,
                                         text="",
                                         style='LastUpdate.TLabel')
        self.last_update_label.pack(side='bottom', pady=5)
        
        # Create platform frames
        self.platform_frames = {}
        
        # Start update threads
        self.display_thread = threading.Thread(target=self.update_display_loop, daemon=True)
        self.data_thread = threading.Thread(target=self.update_data_loop, daemon=True)
        self.display_thread.start()
        self.data_thread.start()
        
        # Start file watcher for settings.txt
        self.start_file_watcher()
        
        # Bind escape key to exit
        self.root.bind('<Escape>', lambda e: self.root.quit())

    def load_settings(self):
        """Load settings from settings.txt file."""
        try:
            with open('settings.txt', 'r') as f:
                for line in f:
                    if line.strip() and not line.startswith('#'):
                        key, value = line.strip().split('=')
                        if key == 'DEPARTURES_TO_SHOW':
                            self.departures_to_show = int(value)
                            break
            if not hasattr(self, 'departures_to_show'):
                print("DEPARTURES_TO_SHOW not found in settings.txt, using default value of 3")
                self.departures_to_show = 3
        except FileNotFoundError:
            print("settings.txt not found, using default value of 3 departures")
            self.departures_to_show = 3
        except Exception as e:
            print(f"Error reading settings.txt: {e}, using default value of 3 departures")
            self.departures_to_show = 3

    def setup_fonts(self):
        """Setup fonts with Minecraft as primary choice."""
        try:
            # Check if Minecraft is available
            available_fonts = font.families()
            if 'Minecraft' in available_fonts:
                platform_font = ('Minecraft', 60, 'bold')
                departure_font = ('Minecraft', 50)
                update_font = ('Minecraft', 30)
            else:
                print("Minecraft font not found, using Courier")
                platform_font = ('Courier', 60, 'bold')
                departure_font = ('Courier', 50)
                update_font = ('Courier', 30)
        except Exception as e:
            print(f"Error setting up fonts: {e}")
            platform_font = ('Courier', 60, 'bold')
            departure_font = ('Courier', 50)
            update_font = ('Courier', 30)

        # Configure styles
        self.style = ttk.Style()
        self.style.configure('Platform.TLabel', 
                           font=platform_font,
                           foreground='orange',
                           background='black')
        self.style.configure('Departure.TLabel',
                           font=departure_font,
                           foreground='orange',
                           background='black')
        self.style.configure('LastUpdate.TLabel',
                           font=update_font,
                           foreground='orange',
                           background='black')

    def update_data(self):
        """Fetch new data from the API and process it."""
        try:
            # Reload settings before fetching data
            self.load_settings()
            # Run bus_times.py
            subprocess.run(['python3', 'bus_times.py'], check=True)
            # Run process_departures.py
            subprocess.run(['python3', 'process_departures.py'], check=True)
            return True
        except subprocess.CalledProcessError as e:
            print(f"Error updating data: {e}")
            return False

    def update_data_loop(self):
        """Update data every 10 minutes."""
        while True:
            if self.update_data():
                self.last_update_label.config(
                    text=f"Senast uppdaterad: {datetime.now().strftime('%H:%M:%S')}"
                )
            time.sleep(600)  # Wait 10 minutes

    def start_file_watcher(self):
        """Start watching settings.txt for changes."""
        try:
            self.observer = Observer()
            self.event_handler = FileWatcher(self.update_data)
            self.observer.schedule(self.event_handler, path='.', recursive=False)
            self.observer.start()
            print("Started file watcher for settings.txt")
        except Exception as e:
            print(f"Error starting file watcher: {e}")

    def format_time_until(self, departure_time):
        now = datetime.now()
        departure = datetime.fromisoformat(departure_time)
        diff = departure - now
        
        if diff.total_seconds() <= 0:
            return "Nu"
        
        minutes = int(diff.total_seconds() // 60)
        seconds = int(diff.total_seconds() % 60)
        return f"{minutes:02d}:{seconds:02d}"

    def update_display(self):
        try:
            with open('departure_lists/platform_departures.json', 'r') as f:
                data = json.load(f)
            
            # Clear existing widgets
            for widget in self.main_frame.winfo_children():
                widget.destroy()
            
            # Create new display
            for platform, departures in data['platforms'].items():
                platform_frame = ttk.Frame(self.main_frame, style='Platform.TLabel')
                platform_frame.pack(fill='x', pady=10)
                
                # Platform header
                platform_label = ttk.Label(platform_frame,
                                         text=f"Plattform {platform}",
                                         style='Platform.TLabel')
                platform_label.pack(anchor='w')
                
                # Departures
                now = datetime.now()
                upcoming = [d for d in departures 
                          if datetime.fromisoformat(d['time']) > now][:self.departures_to_show]
                
                for dep in upcoming:
                    dep_frame = ttk.Frame(platform_frame, style='Platform.TLabel')
                    dep_frame.pack(fill='x', pady=2)
                    
                    route_label = ttk.Label(dep_frame,
                                          text=f"Linje {dep['route']} {dep['direction']} ",
                                          style='Departure.TLabel')
                    route_label.pack(side='left', padx=20)
                    
                    time_label = ttk.Label(dep_frame,
                                         text=self.format_time_until(dep['time']),
                                         style='Departure.TLabel')
                    time_label.pack(side='right', padx=20)
        
        except Exception as e:
            print(f"Error updating display: {e}")

    def update_display_loop(self):
        """Update the display every second."""
        while True:
            self.root.after(0, self.update_display)
            time.sleep(1)

def main():
    root = tk.Tk()
    app = BusDisplay(root)
    try:
        root.mainloop()
    finally:
        # Stop the observer when the application closes
        if hasattr(app, 'observer'):
            app.observer.stop()
            app.observer.join()

if __name__ == "__main__":
    main()