import unittest
from anchorscad_lib.test_tools import IterableAssert, iterable_assert


VALUESA = list(range(10))
VALUESB = list(range(10))
VALUESC = list(range(9))
VALUESD = list(range(10))
VALUESD[5] = VALUESD[5] + 1

DVALUES1 = [VALUESA, VALUESB, VALUESC]
DVALUES2 = [VALUESA, VALUESB, VALUESC]
DVALUES3 = [VALUESA, VALUESD, VALUESC]

FLOATS1 = [1.0, 2.0, 3.0]
FLOATS2 = [1.0, 2.0, 3.001]

class MyTestObj:
    '''Something iterable than isn't Iterable.'''
    
    def __init__(self, v):
        self.v = v
        
    def __getitem__(self, index):
        return self.v[index]
    
    def __len__(self):
        return len(self.v)
        
TEST_OBJ1 = MyTestObj(FLOATS1)

class TestToolsTest(unittest.TestCase):
        
    def test_same(self):
        iterable_assert(self.assertEqual, VALUESA, VALUESB)
        
    def test_different_length(self):
        try:
            iterable_assert(self.assertEqual, VALUESA, VALUESC)
            self.fail('IterableAssert not raised')
        except IterableAssert as e:
            self.assertTrue(str(e).endswith('Lengths different depth=() len(va)=10 != len(vb)=9'))
    
    def test_different_values(self):
        try:
            iterable_assert(self.assertEqual, VALUESA, VALUESD)
            self.fail('IterableAssert not raised')
        except IterableAssert as e:
            self.assertTrue(str(e).startswith('depth=(5,)\nva=[0, 1, '))
            
    def test_different_values_depth(self):
        try:
            iterable_assert(self.assertEqual, DVALUES1, DVALUES3)
            self.fail('IterableAssert not raised')
        except IterableAssert as e:
            self.assertTrue(str(e).startswith('depth=(1, 5)'))
            
    def test_same_depth(self):
        iterable_assert(self.assertEqual, DVALUES1, DVALUES2)
        
    def test_same_depth_float(self):
        iterable_assert(self.assertAlmostEqual, FLOATS1, FLOATS2, places=1)
        
    def test_same_depth_float_fails(self):
        try:
            iterable_assert(self.assertAlmostEqual, FLOATS1, FLOATS2, places=3)
            self.fail('IterableAssert not raised')
        except IterableAssert as e:
            self.assertTrue(str(e).endswith(
                '3.0 != 3.001 within 3 places (0.0009999999999998899 difference)'))
            
    def test_ducks(self):
        iterable_assert(self.assertEqual, TEST_OBJ1, FLOATS1)
            
if __name__ == '__main__':
    unittest.main()

