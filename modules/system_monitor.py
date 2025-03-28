import sys
import psutil
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QFrame, QHBoxLayout, QProgressBar
from PyQt5.QtCore import QTimer, Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

class SystemMemoryGraph(FigureCanvas):
    def __init__(self, parent=None):
        self.fig, self.ax = plt.subplots(figsize=(9, 5), dpi=100)
        super().__init__(self.fig)
        self.setParent(parent)

        self.max_points = 60  # Keep last 60 seconds of data
        self.data_used = []
        self.data_available = []
        self.total_memory = psutil.virtual_memory().total / (1024 ** 3)  # Convert to GB

        self.ax.set_title("Memory Usage Over Time", fontsize=14, fontweight="bold")
        self.ax.set_xlabel("Time (s)", fontsize=10)
        self.ax.set_ylabel("Memory (GB)", fontsize=10)
        self.ax.set_ylim(0, self.total_memory)
        self.ax.set_xlim(0, self.max_points)
        self.ax.grid(True, linestyle="--", alpha=0.6)

        # Line plots
        self.line_used, = self.ax.plot([], [], label="Used Memory (GB)", color="#FF5733", linewidth=2.5)
        self.line_available, = self.ax.plot([], [], label="Available Memory (GB)", color="#33A1FF", linewidth=2.5)

        # Fill under lines (Initially None)
        self.fill_used = None
        self.fill_available = None

        self.ax.legend(fontsize=10, loc="upper right")

    def update_graph(self, used_memory, available_memory):
        self.data_used.append(used_memory)
        self.data_available.append(available_memory)

        if len(self.data_used) > self.max_points:
            self.data_used.pop(0)
            self.data_available.pop(0)

        x_range = range(len(self.data_used))

        self.line_used.set_data(x_range, self.data_used)
        self.line_available.set_data(x_range, self.data_available)

        # Remove old fill areas before creating new ones
        if self.fill_used:
            self.fill_used.remove()
        if self.fill_available:
            self.fill_available.remove()

        self.fill_used = self.ax.fill_between(x_range, self.data_used, color="#FF5733", alpha=0.3)
        self.fill_available = self.ax.fill_between(x_range, self.data_available, color="#33A1FF", alpha=0.3)

        self.ax.set_xlim(0, max(10, len(self.data_used) - 1))
        self.draw()

class SystemMonitorTab(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_stats)
        self.timer.start(1000)  # Update every second

    def init_ui(self):
        layout = QVBoxLayout()
        self.setLayout(layout)

        # Larger Memory Graph (Task Manager Style)
        self.memory_graph = SystemMemoryGraph()
        layout.addWidget(self.memory_graph)

        # Add a separator line
        frame = QFrame()
        frame.setFrameShape(QFrame.HLine)
        frame.setFrameShadow(QFrame.Sunken)
        layout.addWidget(frame)

        # Stats Container (Bottom)
        self.stats_layout = QHBoxLayout()
        layout.addLayout(self.stats_layout)

        # Memory Stats Labels
        self.stats_label = QLabel()
        self.stats_label.setAlignment(Qt.AlignLeft)
        self.stats_label.setStyleSheet("font-size: 14px; font-weight: bold;")
        self.stats_layout.addWidget(self.stats_label)

        # Progress Bar for Visual Memory Usage
        self.progress_bar = QProgressBar()
        self.progress_bar.setTextVisible(True)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: 1px solid #000;
                border-radius: 5px;
                height: 20px;
            }
            QProgressBar::chunk {
                background-color: #FF5733;
                width: 10px;
            }
        """)
        self.stats_layout.addWidget(self.progress_bar)

    def update_stats(self):
        mem = psutil.virtual_memory()
        total = mem.total / (1024 ** 3)  # Convert to GB
        used = mem.used / (1024 ** 3)
        available = mem.available / (1024 ** 3)
        swap = psutil.swap_memory()

        self.memory_graph.update_graph(used, available)

        # Update Progress Bar
        used_percentage = (used / total) * 100
        self.progress_bar.setValue(int(used_percentage))

        # Update Stats Label
        stats_text = (
            f"🖥 Physical Memory: {used:.2f} GB / {total:.2f} GB  (Available: {available:.2f} GB)\n"
            f"💾 Swap Memory: {swap.used / (1024 ** 3):.2f} GB / {swap.total / (1024 ** 3):.2f} GB\n"
            f"⚡ CPU Usage: {psutil.cpu_percent()}%"
        )
        self.stats_label.setText(stats_text)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SystemMonitorTab()
    window.setWindowTitle("System Monitor")
    window.resize(800, 500)
    window.show()
    sys.exit(app.exec_())
