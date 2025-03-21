from memory_manager import MemoryManager
from process import Process
from visualization import MemoryVisualizerGUI
import time
import random
import threading

def simulate_processes(memory_manager, visualizer):
    """Simulate process creation and termination"""
    process_id = 1
    while True:
        # Create a new process
        process_size = random.randint(50, 200)  # Random size between 50-200 KB
        process = Process(process_id, f"Process-{process_id}", process_size)
        
        # Try to allocate memory
        allocation = memory_manager.allocate_memory(process.process_id, process.memory_size)
        if allocation:
            print(f"Created {process}")
            process.add_segment(allocation)
            process.update_state("RUNNING")
        else:
            print(f"Failed to allocate memory for {process}")
        
        # Update visualization
        visualizer.update_visualization()
        
        # Wait for some time
        time.sleep(2)
        
        # Randomly terminate some processes
        if random.random() < 0.3:  # 30% chance to terminate a process
            processes = list(memory_manager.processes.keys())
            if processes:
                process_to_terminate = random.choice(processes)
                freed = memory_manager.free_memory(process_to_terminate)
                print(f"Terminated Process-{process_to_terminate}, freed {freed}KB")
                visualizer.update_visualization()
        
        process_id += 1

def main():
    # Initialize memory manager with 1000 KB total memory
    memory_manager = MemoryManager(1000)
    
    # Create and start the visualization
    visualizer = MemoryVisualizerGUI(memory_manager)
    
    # Start process simulation in a separate thread
    simulation_thread = threading.Thread(target=simulate_processes, 
                                      args=(memory_manager, visualizer),
                                      daemon=True)
    simulation_thread.start()
    
    # Run the GUI
    visualizer.run()

if __name__ == "__main__":
    main() 