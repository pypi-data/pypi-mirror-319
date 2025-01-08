import bitmapmaker.bitmapgui as bmg
class bitmapops:
    def __init__(self, bmx: int, bmy: int):
        self.bmx = bmx
        self.bmy = bmy
    
    def createGrid(self):
        bmg.bitmapgui(self.bmx, self.bmy)
        return (self.bmx, self.bmy)