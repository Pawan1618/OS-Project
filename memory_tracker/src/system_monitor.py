import psutil
import time
from collections import deque
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from theme_manager import ThemeManager

class SystemMemoryMonitor:
    def __init__(self, max_points=100):
        self.max_points = max_points
        self.times = deque(maxlen=max_points)
        self.total_memory = deque(maxlen=max_points)
        self.used_memory = deque(maxlen=max_points)
        self.available_memory = deque(maxlen=max_points)
        self.start_time = time.time()
        
        # Get total system memory once at initialization
        self.system_total_memory = psutil.virtual_memory().total / (1024 * 1024)  # MB

    def update(self):
        """Update memory statistics"""
        memory = psutil.virtual_memory()
        current_time = time.time() - self.start_time

        self.times.append(current_time)
        self.total_memory.append(memory.total / (1024 * 1024))  # Convert to MB
        self.used_memory.append(memory.used / (1024 * 1024))
        self.available_memory.append(memory.available / (1024 * 1024))

    def get_current_stats(self):
        """Get current memory statistics"""
        memory = psutil.virtual_memory()
        return {
            'total': memory.total / (1024 * 1024),  # MB
            'used': memory.used / (1024 * 1024),
            'available': memory.available / (1024 * 1024),
            'percent': memory.percent
        }

class MemoryGraph:
    def __init__(self, parent, monitor):
        self.monitor = monitor
        
        # Create figure with custom style
        self.figure = Figure(figsize=(10, 5), dpi=100, facecolor=ThemeManager.COLORS['background'])
        
        self.canvas = FigureCanvasTkAgg(self.figure, master=parent)
        self.canvas.get_tk_widget().pack(fill='both', expand=True)
        
        # Create subplot with custom style
        self.ax = self.figure.add_subplot(111)
        self.ax.set_facecolor(ThemeManager.COLORS['surface'])
        
        # Set custom grid
        self.ax.grid(True, linestyle='--', alpha=0.3, color=ThemeManager.COLORS['dark'])
        
        # Initialize empty lines with custom colors
        self.used_line, = self.ax.plot([], [], '-', 
                                     color=ThemeManager.COLORS['danger'],
                                     linewidth=2, 
                                     label='Used Memory')
        self.available_line, = self.ax.plot([], [], '-',
                                          color=ThemeManager.COLORS['success'],
                                          linewidth=2,
                                          label='Available Memory')
        
        # Add total memory line
        self.total_line = self.ax.axhline(y=self.monitor.system_total_memory,
                                        color=ThemeManager.COLORS['info'],
                                        linestyle='--',
                                        linewidth=1.5,
                                        label='Total Memory')
        
        # Initialize fill between artists
        self.used_fill = None
        self.available_fill = None
        
        # Customize the plot
        self.ax.set_title('System Memory Usage Over Time',
                         fontsize=12, pad=15,
                         color=ThemeManager.COLORS['dark'])
        self.ax.set_xlabel('Time (seconds)',
                          fontsize=10,
                          color=ThemeManager.COLORS['dark'])
        self.ax.set_ylabel('Memory (MB)',
                          fontsize=10,
                          color=ThemeManager.COLORS['dark'])
        
        # Customize tick colors
        self.ax.tick_params(colors=ThemeManager.COLORS['dark'])
        for spine in self.ax.spines.values():
            spine.set_color(ThemeManager.COLORS['dark'])
            spine.set_linewidth(0.5)
        
        # Customize legend
        self.ax.legend(loc='upper right',
                      fancybox=True,
                      shadow=True,
                      framealpha=0.9)
        
        # Set y-axis limits based on total system memory
        total_memory_gb = self.monitor.system_total_memory / 1024  # Convert to GB
        y_limit = (int(total_memory_gb) + 1) * 1024  # Round up to next GB in MB
        self.ax.set_ylim(0, y_limit)
        
        # Add memory size indicators on y-axis
        self.ax.yaxis.set_major_formatter(plt.FuncFormatter(self._memory_formatter))
        
        # Tight layout
        self.figure.tight_layout()

    def _memory_formatter(self, x, p):
        """Format memory values on y-axis"""
        if x >= 1024:
            return f'{x/1024:.1f} GB'
        return f'{int(x)} MB'

    def update(self):
        """Update the graph with new data"""
        self.monitor.update()
        
        times = list(self.monitor.times)
        used = list(self.monitor.used_memory)
        available = list(self.monitor.available_memory)
        
        # Update line data
        self.used_line.set_data(times, used)
        self.available_line.set_data(times, available)
        
        # Remove old fill_between patches
        if self.used_fill is not None:
            self.used_fill.remove()
        if self.available_fill is not None:
            self.available_fill.remove()
        
        # Create new fill_between patches
        self.used_fill = self.ax.fill_between(times, used, 0,
                                            color=ThemeManager.COLORS['danger'],
                                            alpha=0.1)
        self.available_fill = self.ax.fill_between(times, available, 0,
                                                 color=ThemeManager.COLORS['success'],
                                                 alpha=0.1)
        
        # Adjust x-axis if needed
        if len(times) > 0:
            self.ax.set_xlim(min(times), max(times))
            
            # Update grid
            self.ax.grid(True, linestyle='--', alpha=0.3, color=ThemeManager.COLORS['dark'])
        
        self.canvas.draw() 