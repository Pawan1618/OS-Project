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
        self.manager.allocate_memory("P1", 30)
        self.manager.allocate_memory("P2", 20)
        self.manager.free_memory("P1")
        frag_info = self.manager.get_fragmentation_info()
        self.assertGreater(frag_info['fragmentation_percentage'], 0)

    def test_memory_map(self):
        self.manager.allocate_memory("P1", 40)
        self.manager.allocate_memory("P2", 20)
        mem_map = self.manager.get_memory_map()
        self.assertEqual(len(mem_map), 2)
        self.assertEqual(mem_map[0]['size'], 40)
        self.assertEqual(mem_map[1]['size'], 20)

if __name__ == '__main__':
    unittest.main()
