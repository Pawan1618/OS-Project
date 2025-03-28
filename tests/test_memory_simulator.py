# tests/test_memory_simulator.py
import unittest
import numpy as np
from modules.memory_simulator import MemorySimulator, AllocationStrategy

class TestMemorySimulator(unittest.TestCase):
    def setUp(self):
        # Initialize a small memory simulator for testing
        self.sim = MemorySimulator(total_memory=256, page_size=32)

    def test_initialization(self):
        # Test initial state
        self.assertEqual(self.sim.total_memory, 256)
        self.assertEqual(self.sim.page_size, 32)
        self.assertTrue(np.all(self.sim.memory == 0))
        self.assertEqual(len(self.sim.free_blocks), 1)
        self.assertEqual(self.sim.free_blocks[0], (0, 255))
        self.assertEqual(self.sim.strategy, AllocationStrategy.FIRST_FIT)

    def test_reset(self):
        # Allocate some memory first
        self.sim.allocate_segment(1, 64)
        self.sim.reset()
        self.assertTrue(np.all(self.sim.memory == 0))
        self.assertEqual(self.sim.free_blocks, [(0, 255)])
        self.assertEqual(self.sim.processes, {})
        self.assertTrue(any("System Reset" in h[0] for h in self.sim.history))

    def test_set_strategy(self):
        # Test changing allocation strategy
        self.sim.set_strategy(AllocationStrategy.BEST_FIT)
        self.assertEqual(self.sim.strategy, AllocationStrategy.BEST_FIT)
        self.sim.set_strategy(AllocationStrategy.WORST_FIT)
        self.assertEqual(self.sim.strategy, AllocationStrategy.WORST_FIT)

    def test_allocate_segment_first_fit(self):
        # Test first fit allocation
        success, msg = self.sim.allocate_segment(1, 64)
        self.assertTrue(success)
        self.assertEqual(self.sim.processes[1], (0, 64))
        self.assertTrue(np.all(self.sim.memory[0:64] == 1))
        self.assertEqual(self.sim.free_blocks, [(64, 255)])

    def test_allocate_segment_best_fit(self):
        self.sim.set_strategy(AllocationStrategy.BEST_FIT)
        self.sim.allocate_segment(1, 64)  # Creates a block at 0-63
        self.sim.allocate_segment(2, 32)  # Should fit in smallest suitable block
        self.assertEqual(self.sim.processes[2], (64, 32))
        self.assertTrue(np.all(self.sim.memory[64:96] == 2))

    def test_allocate_segment_worst_fit(self):
        self.sim.set_strategy(AllocationStrategy.WORST_FIT)
        self.sim.allocate_segment(1, 64)  # Creates a block at 0-63
        self.sim.allocate_segment(2, 32)  # Should fit in largest block
        self.assertEqual(self.sim.processes[2], (64, 32))
        self.assertTrue(np.all(self.sim.memory[64:96] == 2))

    def test_allocate_pages(self):
        # Test page allocation
        success, msg = self.sim.allocate_pages(1, 40)  # Needs 2 pages (64 bytes)
        self.assertTrue(success)
        self.assertEqual(len(self.sim.processes[1]), 2)  # 2 pages allocated
        self.assertTrue(np.all(self.sim.memory[0:32] == 1))
        self.assertTrue(np.all(self.sim.memory[32:64] == 1))

    def test_deallocate_segment(self):
        # Test deallocation of segment
        self.sim.allocate_segment(1, 64)
        success, msg = self.sim.deallocate(1)
        self.assertTrue(success)
        self.assertNotIn(1, self.sim.processes)
        self.assertTrue(np.all(self.sim.memory[0:64] == 0))
        self.assertEqual(self.sim.free_blocks, [(0, 255)])

    def test_deallocate_pages(self):
        # Test deallocation of pages
        self.sim.allocate_pages(1, 40)
        success, msg = self.sim.deallocate(1)
        self.assertTrue(success)
        self.assertNotIn(1, self.sim.processes)
        self.assertTrue(np.all(self.sim.memory[0:64] == 0))

    def test_duplicate_process(self):
        # Test allocation with existing process ID
        self.sim.allocate_segment(1, 64)
        success, msg = self.sim.allocate_segment(1, 32)
        self.assertFalse(success)
        self.assertIn("Process already exists", msg)

    def test_insufficient_memory(self):
        # Test allocation with insufficient memory
        success, msg = self.sim.allocate_segment(1, 300)
        self.assertFalse(success)
        self.assertIn("No suitable block found", msg)

    def test_get_memory_state(self):
        # Test memory state retrieval
        self.sim.allocate_segment(1, 64)
        state = self.sim.get_memory_state()
        self.assertTrue(np.all(state[0:64] == 1))
        self.assertTrue(np.all(state[64:] == 0))

    def test_get_fragmentation(self):
        # Test fragmentation calculation
        self.sim.allocate_segment(1, 64)
        external, internal = self.sim.get_fragmentation()
        self.assertEqual(external, 0)  # One contiguous free block
        self.assertEqual(internal, 0)  # No internal fragmentation in segments

    def test_get_utilization(self):
        # Test memory utilization
        self.sim.allocate_segment(1, 64)
        utilization = self.sim.get_utilization()
        self.assertEqual(utilization, (64 / 256) * 100)  # 25%

if __name__ == '__main__':
    unittest.main()