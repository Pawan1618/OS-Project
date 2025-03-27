# Memory Allocation Visualizer

A comprehensive tool for visualizing memory allocation strategies and monitoring system resources in real-time.

![Application Screenshot](screenshot.png) <!-- Add actual screenshot later -->

## Features

- **Memory Allocation Simulation**
  - First-fit, Best-fit, and Worst-fit allocation strategies
  - Visual representation of memory blocks
  - Real-time fragmentation statistics
  - Page/Segment view toggle

- **System Resource Monitoring**
  - Real-time memory usage graph
  - CPU utilization tracking
  - Swap memory statistics
  - Historical data visualization

- **Process Management**
  - Live process list (unsorted)
  - Memory and CPU usage per process
  - Auto-refreshing data

- **Advanced Visualization**
  - Matplotlib integration for professional charts
  - Qt5-based GUI with tabbed interface
  - Color-coded memory blocks

## Installation

### Prerequisites
- Python 3.8+
- pip package manager

### Setup
```bash
# Clone repository
git clone https://github.com/yourusername/memory-visualizer.git
cd memory-visualizer

# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # Linux/MacOS
venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt
