from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, 
                            QPushButton, QLabel, QComboBox, 
                            QSpinBox, QTextEdit, QTabWidget,QMainWindow)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QColor, QPainter, QBrush, QFont, QPen
from .memory_simulator import MemorySimulator, AllocationStrategy

class MemoryVisualizer(QWidget):
    def __init__(self, simulator, parent=None):
        super().__init__(parent)
        self.simulator = simulator
        self.setMinimumSize(1000, 300)
        self.block_height = 50
        self.margin = 30
        self.show_paging = False
        self.selected_process = None
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        width = self.width() - 2 * self.margin
        height = self.block_height
        total_memory = self.simulator.total_memory
        
        # Draw memory outline (using integers)
        painter.setPen(Qt.black)
        painter.drawRect(self.margin, self.margin, round(width), height)
        
        # Draw memory blocks
        memory = self.simulator.get_memory_state()
        
        if self.show_paging:
            self._draw_pages(painter, width, height, memory)
        else:
            self._draw_segments(painter, width, height, memory)
            
        # Draw legend
        self._draw_legend(painter)
        
    def _draw_segments(self, painter, width, height, memory):
        total_memory = self.simulator.total_memory
        unit_width = width / total_memory

        current_val = memory[0]
        start = 0

        for i in range(1, total_memory):
            if memory[i] != current_val or i == total_memory - 1:
                end = i - 1
                if current_val != 0:
                    color = self._get_process_color(current_val)
                    painter.fillRect(
                        round(self.margin + start * unit_width),
                        self.margin,
                        round((end - start + 1) * unit_width),
                        height,
                        color
                    )

                    # Draw process ID
                    if (end - start + 1) * unit_width > 30:  # Only draw if wide enough
                        painter.setPen(Qt.black)
                        font = QFont()
                        font.setPointSize(8)
                        painter.setFont(font)
                        painter.drawText(
                            round(self.margin + start * unit_width),
                            self.margin,
                            round((end - start + 1) * unit_width),
                            height,
                            Qt.AlignCenter,
                            str(current_val)
                        )

                # Draw block border
                painter.setPen(Qt.black)
                painter.drawRect(
                    round(self.margin + start * unit_width),
                    self.margin,
                    round((end - start + 1) * unit_width),
                    height
                )

                current_val = memory[i]
                start = i
                
    def _draw_pages(self, painter, width, height, memory):
        total_memory = self.simulator.total_memory
        page_size = self.simulator.page_size
        unit_width = width / total_memory

        for page_start in range(0, total_memory, page_size):
            page_end = min(page_start + page_size, total_memory) - 1
            page_val = memory[page_start]

            if page_val != 0:
                color = self._get_process_color(page_val)
                painter.fillRect(
                    round(self.margin + page_start * unit_width),
                    self.margin,
                    round(page_size * unit_width),
                    height,
                    color
                )

                # Draw process ID
                painter.setPen(Qt.black)
                font = QFont()
                font.setPointSize(8)
                painter.setFont(font)
                painter.drawText(
                    round(self.margin + page_start * unit_width),
                    self.margin,
                    round(page_size * unit_width),
                    height,
                    Qt.AlignCenter,
                    str(page_val)
                )

            # Draw page border
            painter.setPen(Qt.black)
            painter.drawRect(
                round(self.margin + page_start * unit_width),
                self.margin,
                round(page_size * unit_width),
                height
            )
            
    def _draw_legend(self, painter):
        painter.setPen(Qt.black)
        font = QFont()
        font.setPointSize(10)
        painter.setFont(font)
        
        y_pos = self.margin * 2 + self.block_height + 10
        x_pos = self.margin
        
        # Draw free memory
        painter.setBrush(Qt.white)
        painter.drawRect(x_pos, y_pos, 20, 20)
        painter.drawText(x_pos + 30, y_pos + 15, "Free Memory")
        
        # Draw used memory
        painter.setBrush(QColor(100, 200, 100))
        painter.drawRect(x_pos + 150, y_pos, 20, 20)
        painter.drawText(x_pos + 180, y_pos + 15, "Allocated Memory")
        
        # Draw selected process
        if self.selected_process:
            painter.setBrush(self._get_process_color(self.selected_process))
            painter.drawRect(x_pos + 350, y_pos, 20, 20)
            painter.drawText(x_pos + 380, y_pos + 15, f"Process {self.selected_process}")
            
    def _get_process_color(self, process_id):
        # Generate a consistent color based on process ID
        hue = (process_id * 137) % 360  # Golden angle approximation
        return QColor.fromHsv(hue, 150, 200)
        
    def toggle_view(self, show_paging):
        self.show_paging = show_paging
        self.update()
        
    def set_selected_process(self, process_id):
        self.selected_process = process_id
        self.update()

class SimulationTab(QWidget):
    def __init__(self, simulator, parent=None):
        super().__init__(parent)
        self.simulator = simulator
        self.init_ui()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_stats)
        self.timer.start(500)
        
    def init_ui(self):
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        # Control panel
        control_layout = QHBoxLayout()
        
        self.strategy_combo = QComboBox()
        self.strategy_combo.addItem("First Fit", AllocationStrategy.FIRST_FIT)
        self.strategy_combo.addItem("Best Fit", AllocationStrategy.BEST_FIT)
        self.strategy_combo.addItem("Worst Fit", AllocationStrategy.WORST_FIT)
        self.strategy_combo.currentIndexChanged.connect(self.change_strategy)
        control_layout.addWidget(QLabel("Strategy:"))
        control_layout.addWidget(self.strategy_combo)
        
        self.view_combo = QComboBox()
        self.view_combo.addItem("Segmentation")
        self.view_combo.addItem("Paging")
        self.view_combo.currentIndexChanged.connect(self.toggle_view)
        control_layout.addWidget(QLabel("View:"))
        control_layout.addWidget(self.view_combo)
        
        self.process_id_spin = QSpinBox()
        self.process_id_spin.setRange(1, 100)
        control_layout.addWidget(QLabel("Process ID:"))
        control_layout.addWidget(self.process_id_spin)
        
        self.size_spin = QSpinBox()
        self.size_spin.setRange(1, 512)
        self.size_spin.setValue(64)
        control_layout.addWidget(QLabel("Size:"))
        control_layout.addWidget(self.size_spin)
        
        allocate_btn = QPushButton("Allocate")
        allocate_btn.clicked.connect(self.allocate_memory)
        control_layout.addWidget(allocate_btn)
        
        deallocate_btn = QPushButton("Deallocate")
        deallocate_btn.clicked.connect(self.deallocate_memory)
        control_layout.addWidget(deallocate_btn)
        
        reset_btn = QPushButton("Reset")
        reset_btn.clicked.connect(self.reset_memory)
        control_layout.addWidget(reset_btn)
        
        layout.addLayout(control_layout)
        
        # Visualization
        self.visualizer = MemoryVisualizer(self.simulator)
        layout.addWidget(self.visualizer)
        
        # Stats panel
        stats_layout = QHBoxLayout()
        
        self.stats_label = QLabel()
        stats_layout.addWidget(self.stats_label)
        
        self.history_text = QTextEdit()
        self.history_text.setReadOnly(True)
        self.history_text.setMaximumHeight(100)
        stats_layout.addWidget(self.history_text)
        
        layout.addLayout(stats_layout)
        
    def change_strategy(self, index):
        strategy = self.strategy_combo.currentData()
        self.simulator.set_strategy(strategy)
        
    def toggle_view(self, index):
        self.visualizer.toggle_view(index == 1)
        
    def allocate_memory(self):
        process_id = self.process_id_spin.value()
        size = self.size_spin.value()
        
        if self.view_combo.currentIndex() == 0:  # Segmentation
            success, message = self.simulator.allocate_segment(process_id, size)
        else:  # Paging
            success, message = self.simulator.allocate_pages(process_id, size)
            
        self.update_display()
        self.visualizer.set_selected_process(process_id if success else None)
        
    def deallocate_memory(self):
        process_id = self.process_id_spin.value()
        success, message = self.simulator.deallocate(process_id)
        self.update_display()
        self.visualizer.set_selected_process(None)
        
    def reset_memory(self):
        self.simulator.reset()
        self.update_display()
        self.visualizer.set_selected_process(None)
        
    def update_display(self):
        self.visualizer.update()
        self.update_stats()
        
    def update_stats(self):
        utilization = self.simulator.get_utilization()
        external_frag, internal_frag = self.simulator.get_fragmentation()
        
        stats_text = (
            f"Memory Utilization: {utilization:.1f}%\n"
            f"External Fragmentation: {external_frag:.1f}%\n"
            f"Internal Fragmentation: {internal_frag} units"
        )
        self.stats_label.setText(stats_text)
        
        # Update history
        history = self.simulator.history[-10:]  # Show last 10 entries
        history_text = "\n".join(f"{action}" for action, _ in reversed(history))
        self.history_text.setPlainText(history_text)

class MemoryWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.simulator = MemorySimulator()
        self.init_ui()
        
    def init_ui(self):
        self.setWindowTitle("Memory Allocation Visualizer")
        self.setGeometry(100, 100, 1200, 800)
        
        tab_widget = QTabWidget()
        self.setCentralWidget(tab_widget)
        
        # Simulation Tab
        sim_tab = SimulationTab(self.simulator)
        tab_widget.addTab(sim_tab, "Simulation")
        
        # System Monitor Tab
        from .system_monitor import SystemMonitorTab
        sys_tab = SystemMonitorTab()
        tab_widget.addTab(sys_tab, "System Monitor")
        
        # Process Manager Tab
        from .process_manager import ProcessManagerTab
        proc_tab = ProcessManagerTab()
        tab_widget.addTab(proc_tab, "Process Manager")