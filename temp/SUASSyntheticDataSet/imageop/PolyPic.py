
class PolyPic:
    
    def __init__(self, backgroundImgIn, fieldObjectIn):
        self.backgroundImg = backgroundImgIn
        self.fieldObject = fieldObjectIn
        
    def getImg(self):
        return self.backgroundImg
    
    def getFieldObject(self):
        return self.fieldObject