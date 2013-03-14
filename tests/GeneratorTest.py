'''
Created on 14-03-2013

@author: jakub
'''
import unittest
import logging
from points_generator.Generator import Generator

class GeneratorTest(unittest.TestCase):
    
    def setUp(self):
        unittest.TestCase.setUp(self)
        self.logger = logging.getLogger("GeneratorTest")
        self.logger.setLevel(logging.INFO)
        self.logger.addHandler(logging.StreamHandler())
        self.gen = Generator()
        
    def test_addMu(self):
        self.gen.addMu((1,2))
        self.gen.addMu((2,2))
        self.gen.addMu((1,2))
        self.assertTrue(self.gen.localMu==[(1,2),(2,2), (1,2)])
        
    def test_addClassCenter(self):
        self.gen.addClassCenter((1,2), 1)
        self.gen.addClassCenter((1,2), 2)
        self.logger.log(logging.INFO, "Check if there can't be 2 class with exactly same coordinates")
        self.assertNotEqual(len(self.gen.classCenters), 2)
        self.gen.addClassCenter((2,1), 2)
        self.logger.log(logging.INFO, "Check if there can be 2 class with 'switched' coordinates")
        self.assertEqual(len(self.gen.classCenters), 2)

if __name__ == '__main__':
    
    unittest.main()