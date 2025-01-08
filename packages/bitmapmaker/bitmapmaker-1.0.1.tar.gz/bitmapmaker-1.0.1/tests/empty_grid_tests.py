import bitmapmaker.bitmap as bm
    
def test_answer():
    testbm = bm.bitmap(3,3)
    testbm.createGridGui()
    assert (testbm.bmx, testbm.bmy) == (3,3)
    