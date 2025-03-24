import unittest
from src.memory_manager import MemoryManager
class TestMemoryManager(unittest.TestCase):
    def setUp(self):
        self.manager = MemoryManager(100)

    def test_allocation(self):
        block = self.manager.allocate_memory("P1", 30)
        self.assertIsNotNone(block)
        self.assertEqual(block['size'], 30)
        self.assertEqual(block['process_id'], "P1")

    def test_insufficient_memory(self):
        self.manager.allocate_memory("P1", 100)
        block = self.manager.allocate_memory("P2", 10)
        self.assertIsNone(block)

    def test_free_memory(self):
        self.manager.allocate_memory("P1", 30)
        freed = self.manager.free_memory("P1")
        self.assertEqual(freed, 30)
        self.assertEqual(self.manager.used_memory, 0)

    def test_fragmentation(self):
        manager = MemoryManager(100)
        manager.allocate_memory("P1", 30)
        manager.allocate_memory("P2", 40)
        manager.free_memory("P1")  # Free first block to create fragmentation

        # frag_info = manager.get_fragmentation_info()
        # self.assertGreater(frag_info['fragmentation_percentage'], 0)  # Now fragmentation should exist

    # def test_memory_map(self):
    #     manager = MemoryManager(100)
    #     manager.allocate_memory("P1", 30)
    #     manager.allocate_memory("P2", 40)
    #     manager.free_memory("P1")  # Leaves a hole of 30
    
    #     mem_map = manager.get_memory_map()
    
    #     # Now we expect two blocks: one free (30) and one allocated (40)
    #     self.assertEqual(len(mem_map), 2)  

if __name__ == '__main__':
    unittest.main()
