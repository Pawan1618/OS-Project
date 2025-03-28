import psutil
from PyQt5.QtWidgets import (
    QTableWidget, QTableWidgetItem, QHeaderView, QVBoxLayout, QWidget
)
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QColor, QBrush, QFont


class ProcessListTable(QTableWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setColumnCount(4)
        self.setHorizontalHeaderLabels(["PID", "Name", "CPU %", "Memory %"])
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.setEditTriggers(QTableWidget.NoEditTriggers)
        self.setSelectionBehavior(QTableWidget.SelectRows)
        
        # Font improvements
        self.setFont(QFont("Arial", 12))
        self.setStyleSheet("""
            QTableWidget { background-color: #f8f9fa; border: 1px solid #ccc; }
            QTableWidget::item { padding: 5px; }
            QHeaderView::section { background-color: #007bff; color: white; font-size: 14px; padding: 5px; }
        """)
        
        # Enable sorting
        self.setSortingEnabled(True)

    def update_processes(self, processes):
        self.setRowCount(len(processes))
        for row, (pid, name, cpu, mem) in enumerate(processes):
            # Set text
            self.setItem(row, 0, QTableWidgetItem(str(pid)))
            self.setItem(row, 1, QTableWidgetItem(name))
            self.setItem(row, 2, self._styled_item(cpu))
            self.setItem(row, 3, self._styled_item(mem))

            # Set alternating row colors
            if row % 2 == 0:
                for col in range(4):
                    self.item(row, col).setBackground(QColor(230, 240, 255))

    def _styled_item(self, value):
        """ Returns a styled QTableWidgetItem with color based on value intensity. """
        item = QTableWidgetItem(f"{value:.1f}")
        item.setTextAlignment(Qt.AlignCenter)

        if value > 50:
            item.setForeground(QBrush(QColor(200, 0, 0)))  # High usage in red
        elif value > 20:
            item.setForeground(QBrush(QColor(255, 140, 0)))  # Medium usage in orange
        else:
            item.setForeground(QBrush(QColor(0, 128, 0)))  # Low usage in green

        return item


class ProcessManagerTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_processes)
        self.timer.start(2000)

    def init_ui(self):
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        self.process_table = ProcessListTable()
        layout.addWidget(self.process_table)

    def update_processes(self):
        processes = []
        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
            try:
                processes.append((
                    proc.info['pid'],
                    proc.info['name'],
                    proc.info['cpu_percent'],
                    proc.info['memory_percent']
                ))
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue

        # Sort by memory usage
        processes.sort(key=lambda p: p[3], reverse=True)
        self.process_table.update_processes(processes[:20])
