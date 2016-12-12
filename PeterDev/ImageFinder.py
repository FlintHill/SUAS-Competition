import os
from time import sleep
from PIL import Image

class ImageFinder:
    
    def __init__(self, baseDir, format):
        self.baseDir = baseDir
        self.dirContents = []
        self.imgFormat = format
    
    def waitUntilImagePresent(self):
        while(self.dirIsEmpty()):
            print("not done!")
            sleep(0.1)
        print("done!")
    
    def dirIsEmpty(self):
        self.update()
        if self.dirContainsImage():
            return False
        return True
    
    def printDir(self):
        for fileName in self.dirContents:
            if fileName.endswith(self.imgFormat):
                print(self.baseDir + "/" + fileName)
                img = Image.open(self.baseDir + "/" + fileName)
                img.show()
    
    def dirContainsImage(self):
        for fileName in self.dirContents:
            if fileName.endswith(self.imgFormat):
                return True
        return False
    
    def getImgPaths(self):
        return self.imgPaths
    
    def update(self):
        self.dirContents = os.listdir(self.baseDir)
        self.imgPaths = []
        for filename in self.dirContents:
            if filename.endswith(self.imgFormat):
                self.imgPaths.append(self.baseDir + "/" + filename)
        