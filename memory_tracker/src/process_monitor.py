import psutil
import tkinter as tk
from tkinter import ttk
from theme_manager import ThemeManager
import time

class ProcessListView:
    def __init__(self, parent):
        self.parent = parent
        self.max_processes = 50  # Limit to 20 processes
        self.setup_gui()
        
    def setup_gui(self):
        # Create main frame
        self.frame = ttk.Frame(self.parent, padding="10")
        self.frame.pack(fill='both', expand=True)
        
        # Add info label
        self.info_label = ttk.Label(self.frame, 
                                  text=f"Showing top {self.max_processes} processes by memory usage",
                                  style='Stats.TLabel')
        self.info_label.grid(row=0, column=0, columnspan=2, sticky='w', pady=(0, 5))
        
        # Create treeview
        self.tree = ttk.Treeview(self.frame, columns=('pid', 'name', 'memory', 'cpu', 'status'),
                                show='headings', height=self.max_processes)
        
        # Setup scrollbars
        vsb = ttk.Scrollbar(self.frame, orient="vertical", command=self.tree.yview)
        hsb = ttk.Scrollbar(self.frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        
        # Configure columns
        self.tree.heading('pid', text='PID', command=lambda: self._sort_column('pid', False))
        self.tree.heading('name', text='Process Name', command=lambda: self._sort_column('name', False))
        self.tree.heading('memory', text='Memory Usage', command=lambda: self._sort_column('memory_raw', True))
        self.tree.heading('cpu', text='CPU %', command=lambda: self._sort_column('cpu_raw', True))
        self.tree.heading('status', text='Status', command=lambda: self._sort_column('status', False))
        
        self.tree.column('pid', width=100)
        self.tree.column('name', width=200)
        self.tree.column('memory', width=150)
        self.tree.column('cpu', width=100)
        self.tree.column('status', width=100)
        
        # Grid layout
        self.tree.grid(row=1, column=0, sticky='nsew')
        vsb.grid(row=1, column=1, sticky='ns')
        hsb.grid(row=2, column=0, sticky='ew')
        
        # Configure grid weights
        self.frame.grid_columnconfigure(0, weight=1)
        self.frame.grid_rowconfigure(1, weight=1)
        
        # Add control panel
        control_frame = ttk.Frame(self.frame)
        control_frame.grid(row=3, column=0, columnspan=2, pady=(5,0), sticky='ew')
        
        # Add refresh rate control
        ttk.Label(control_frame, text="Refresh Rate:").pack(side='left', padx=(0,5))
        self.refresh_scale = ttk.Scale(control_frame, from_=1, to=5, 
                                     orient='horizontal', length=100)
        self.refresh_scale.set(2)
        self.refresh_scale.pack(side='left', padx=5)
        ttk.Label(control_frame, text="sec").pack(side='left')
        
        # Add total process count label
        self.total_count_label = ttk.Label(control_frame, text="Total Processes: 0", 
                                         style='Stats.TLabel')
        self.total_count_label.pack(side='right', padx=10)
        
        # Add sort controls
        sort_frame = ttk.Frame(control_frame)
        sort_frame.pack(side='right', padx=20)
        ttk.Label(sort_frame, text="Sort by:").pack(side='left', padx=(0,5))
        self.sort_var = tk.StringVar(value="memory")
        sort_options = [
            ("Memory", "memory"),
            ("CPU", "cpu"),
            ("Name", "name"),
            ("PID", "pid")
        ]
        for text, value in sort_options:
            ttk.Radiobutton(sort_frame, text=text, value=value, 
                          variable=self.sort_var).pack(side='left', padx=5)
        
        # Initialize process list
        self.process_data = []  # Store process data for sorting
        self.update_process_list()
        
    def format_memory_size(self, bytes):
        """Convert bytes to human readable format"""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if bytes < 1024:
                return f"{bytes:.1f} {unit}"
            bytes /= 1024
        return f"{bytes:.1f} TB"
    
    def get_process_info(self):
        """Get information about running processes"""
        processes = []
        for proc in psutil.process_iter(['pid', 'name', 'memory_info', 'cpu_percent', 'status']):
            try:
                info = proc.info
                memory = self.format_memory_size(info['memory_info'].rss)
                processes.append({
                    'pid': info['pid'],
                    'name': info['name'],
                    'memory': memory,
                    'memory_raw': info['memory_info'].rss,  # for sorting
                    'cpu': f"{info['cpu_percent']:.1f}%",
                    'cpu_raw': info['cpu_percent'],  # for sorting
                    'status': info['status']
                })
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue
        return processes
    
    def _sort_column(self, col, reverse=True):
        """Sort treeview column"""
        if col in ['memory_raw', 'cpu_raw']:
            # For memory and CPU, sort by raw values
            self.process_data.sort(key=lambda x: x[col], reverse=reverse)
        else:
            # For other columns, sort by display values
            self.process_data.sort(key=lambda x: str(x[col]).lower(), 
                                 reverse=reverse)
        
        # Clear and repopulate the treeview
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        # Show only top processes
        for proc in self.process_data[:self.max_processes]:
            self.tree.insert('', 'end', values=(
                proc['pid'],
                proc['name'],
                proc['memory'],
                proc['cpu'],
                proc['status']
            ))
    
    def update_process_list(self):
        """Update the process list display"""
        # Get process information
        self.process_data = self.get_process_info()
        total_processes = len(self.process_data)
        
        # Sort processes based on selected criterion
        sort_key = self.sort_var.get()
        if sort_key == 'memory':
            self.process_data.sort(key=lambda x: x['memory_raw'], reverse=True)
        elif sort_key == 'cpu':
            self.process_data.sort(key=lambda x: x['cpu_raw'], reverse=True)
        elif sort_key == 'name':
            self.process_data.sort(key=lambda x: x['name'].lower())
        else:  # pid
            self.process_data.sort(key=lambda x: x['pid'])
        
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Add top processes to treeview
        for proc in self.process_data[:self.max_processes]:
            self.tree.insert('', 'end', values=(
                proc['pid'],
                proc['name'],
                proc['memory'],
                proc['cpu'],
                proc['status']
            ))
        
        # Update process count
        self.total_count_label.config(text=f"Total Processes: {total_processes}")
        
        # Schedule next update
        update_interval = int(self.refresh_scale.get() * 1000)  # Convert to milliseconds
        self.parent.after(update_interval, self.update_process_list) 