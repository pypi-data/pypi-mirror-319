import bitmapmaker.bitmapgui as bmg
class bitmap:
    def __init__(self, bmx: int, bmy: int):
        self.bmx = bmx
        self.bmy = bmy
    
    def createGridGui(self):
        bmg.bitmapgui(self.bmx, self.bmy)
        return (self.bmx, self.bmy)