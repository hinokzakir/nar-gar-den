import tkinter as tk
from tkinter import ttk
import json
from datetime import datetime
import time
import threading
import subprocess
import os

class BusDisplay:
    def __init__(self, root):
        self.root = root
        self.root.title("Bussavgångar Ålidhem Centrum")
        self.root.configure(bg='black')
        
        # Make window fullscreen
        self.root.attributes('-fullscreen', True)
        
        # Configure style
        self.style = ttk.Style()
        self.style.configure('Platform.TLabel', 
                           font=('Courier', 120, 'bold'),
                           foreground='orange',
                           background='black')
        self.style.configure('Departure.TLabel',
                           font=('Courier', 100),
                           foreground='orange',
                           background='black')
        self.style.configure('LastUpdate.TLabel',
                           font=('Courier', 60),
                           foreground='orange',
                           background='black')
        
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
        
        # Bind escape key to exit
        self.root.bind('<Escape>', lambda e: self.root.quit())

    def update_data(self):
        """Fetch new data from the API and process it."""
        try:
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
                          if datetime.fromisoformat(d['time']) > now][:3]
                
                for dep in upcoming:
                    dep_frame = ttk.Frame(platform_frame, style='Platform.TLabel')
                    dep_frame.pack(fill='x', pady=2)
                    
                    route_label = ttk.Label(dep_frame,
                                          text=f"Linje {dep['route']}",
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
    root.mainloop()

if __name__ == "__main__":
    main() 