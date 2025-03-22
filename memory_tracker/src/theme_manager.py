import tkinter as tk
from tkinter import ttk
import random
from system_monitor import SystemMemoryMonitor, MemoryGraph
from process_monitor import ProcessListView
from theme_manager import ThemeManager

class MemoryVisualizerGUI:
    def __init__(self, memory_manager):
        self.root = tk.Tk()
        self.root.title("Memory Allocation Tracker")
        self.root.geometry("1200x800")
        self.root.configure(bg=ThemeManager.COLORS['background'])
        
        # Set up the theme
        ThemeManager.setup_theme()
        
        self.memory_manager = memory_manager
        self.system_monitor = SystemMemoryMonitor()
        self.simulation_running = True
        
        # Initialize GUI
        self._setup_gui()
        
    def _setup_gui(self):
        # Main container
        main_container = ttk.Frame(self.root, padding="10")
        main_container.pack(fill='both', expand=True)
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(main_container)
        self.notebook.pack(fill='both', expand=True)
        
        # Create tabs
        self.sim_frame = ttk.Frame(self.notebook, padding="10")
        self.sys_frame = ttk.Frame(self.notebook, padding="10")
        self.process_frame = ttk.Frame(self.notebook, padding="10")
        
        self.notebook.add(self.sim_frame, text="Memory Simulation")
        self.notebook.add(self.sys_frame, text="System Memory")
        self.notebook.add(self.process_frame, text="Process List")
        
        # Setup views
        self._setup_simulation_view()
        self._setup_system_view()
        self._setup_process_view()
        
    def _setup_simulation_view(self):
        # Control Panel
        control_frame = ttk.LabelFrame(self.sim_frame, text="Simulation Controls", padding="10")
        control_frame.pack(fill='x', pady=(0, 10))
        
        # Add controls with styled buttons
        ttk.Button(control_frame, text="▶ Pause/Resume", 
                  command=self._toggle_simulation,
                  style='Primary.TButton').pack(side='left', padx=5)
        ttk.Button(control_frame, text="⟲ Clear All", 
                  command=self._clear_simulation,
                  style='Danger.TButton').pack(side='left', padx=5)
        
        # Speed control
        speed_frame = ttk.Frame(control_frame)
        speed_frame.pack(side='left', padx=20)
        ttk.Label(speed_frame, text="Speed:").pack(side='left')
        self.speed_scale = ttk.Scale(speed_frame, from_=0.1, to=2.0, 
                                   orient='horizontal', length=100)
        self.speed_scale.set(1.0)
        self.speed_scale.pack(side='left', padx=5)
        
        # Memory visualization
        viz_frame = ttk.LabelFrame(self.sim_frame, text="Memory Map", padding="10")
        viz_frame.pack(fill='both', expand=True, pady=(0, 10))
        
        self.canvas = tk.Canvas(viz_frame, height=200, bg=ThemeManager.COLORS['white'])
        self.canvas.pack(fill='both', expand=True)
        
        # Statistics panel
        stats_frame = ttk.LabelFrame(self.sim_frame, text="Memory Statistics", padding="10")
        stats_frame.pack(fill='x')
        
        # Create statistics with modern styling
        self.stats_labels = {}
        stats = [
            ('total', 'Total Memory'),
            ('used', 'Used Memory'),
            ('free', 'Free Memory'),
            ('fragmentation', 'Fragmentation')
        ]
        
        for i, (key, label) in enumerate(stats):
            frame = ttk.Frame(stats_frame)
            frame.grid(row=0, column=i, padx=10, sticky='ew')
            stats_frame.columnconfigure(i, weight=1)
            
            ttk.Label(frame, text=label, style='TLabel').pack()
            self.stats_labels[key] = ttk.Label(frame, text="0 KB", style='Stats.TLabel')
            self.stats_labels[key].pack()
            
    def _setup_system_view(self):
        # System memory statistics
        stats_frame = ttk.LabelFrame(self.sys_frame, text="System Memory Statistics", padding="10")
        stats_frame.pack(fill='x', pady=(0, 10))
        
        # Create system statistics with modern styling
        self.sys_stats_labels = {}
        sys_stats = [
            ('total', 'Total Memory'),
            ('used', 'Used Memory'),
            ('available', 'Available Memory'),
            ('percent', 'Usage')
        ]
        
        for i, (key, label) in enumerate(sys_stats):
            frame = ttk.Frame(stats_frame)
            frame.grid(row=0, column=i, padx=10, sticky='ew')
            stats_frame.columnconfigure(i, weight=1)
            
            ttk.Label(frame, text=label, style='TLabel').pack()
            self.sys_stats_labels[key] = ttk.Label(frame, text="0 MB", style='Stats.TLabel')
            self.sys_stats_labels[key].pack()
        
        # Graph frame
        graph_frame = ttk.LabelFrame(self.sys_frame, text="Memory Usage Graph", padding="10")
        graph_frame.pack(fill='both', expand=True)
        
        # Create memory graph
        self.memory_graph = MemoryGraph(graph_frame, self.system_monitor)
        
    def _setup_process_view(self):
        # Create process list view
        self.process_list = ProcessListView(self.process_frame)
        
    def _toggle_simulation(self):
        self.simulation_running = not self.simulation_running
        
    def _clear_simulation(self):
        # Reset memory manager state
        self.memory_manager.memory_blocks.clear()
        self.memory_manager.processes.clear()
        self.memory_manager.used_memory = 0
        
    def update_visualization(self):
        if self.simulation_running:
            # Update simulation view
            self.canvas.delete("all")
            memory_blocks = self.memory_manager.get_memory_map()
            stats = self.memory_manager.get_fragmentation_info()
            
            # Update statistics with modern formatting
            self.stats_labels['total'].config(
                text=f"{stats['total_memory']:,} KB")
            self.stats_labels['used'].config(
                text=f"{stats['used_memory']:,} KB")
            self.stats_labels['free'].config(
                text=f"{stats['free_memory']:,} KB")
            self.stats_labels['fragmentation'].config(
                text=f"{stats['fragmentation_percentage']:.1f}%")
            
            # Draw memory blocks with improved styling
            canvas_width = self.canvas.winfo_width()
            block_height = 150
            y_start = 25
            
            x_scale = canvas_width / self.memory_manager.total_memory
            
            for block in memory_blocks:
                x1 = block['start'] * x_scale
                x2 = (block['start'] + block['size']) * x_scale
                
                if block['used']:
                    color = ThemeManager.get_process_color(hash(str(block['process_id'])))
                    # Main block
                    self.canvas.create_rectangle(
                        x1, y_start, x2, y_start + block_height,
                        fill=color, outline=ThemeManager.COLORS['dark'],
                        width=2
                    )
                    # Process info
                    self.canvas.create_text(
                        (x1 + x2) / 2, y_start + block_height / 2,
                        text=f"PID: {block['process_id']}\n{block['size']:,} KB",
                        font=('Segoe UI', 10, 'bold'),
                        fill=ThemeManager.COLORS['white']
                    )
                else:
                    # Free block
                    self.canvas.create_rectangle(
                        x1, y_start, x2, y_start + block_height,
                        fill=ThemeManager.COLORS['light'],
                        outline=ThemeManager.COLORS['dark'],
                        width=2,
                        dash=(4, 4)
                    )
                    self.canvas.create_text(
                        (x1 + x2) / 2, y_start + block_height / 2,
                        text=f"Free\n{block['size']:,} KB",
                        font=('Segoe UI', 10),
                        fill=ThemeManager.COLORS['dark']
                    )
        
        # Update system memory view
        sys_stats = self.system_monitor.get_current_stats()
        self.sys_stats_labels['total'].config(
            text=f"{sys_stats['total']:,.0f} MB")
        self.sys_stats_labels['used'].config(
            text=f"{sys_stats['used']:,.0f} MB")
        self.sys_stats_labels['available'].config(
            text=f"{sys_stats['available']:,.0f} MB")
        self.sys_stats_labels['percent'].config(
            text=f"{sys_stats['percent']:.1f}%")
        
        # Update memory graph
        self.memory_graph.update()
        
        # Schedule next update based on speed setting
        update_interval = int(1000 / self.speed_scale.get())
        self.root.after(update_interval, self.update_visualization)
    
    def run(self):
        self.update_visualization()
        self.root.mainloop()