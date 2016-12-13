class ImageOperations:
    
    @staticmethod
    def cropToRectangle(img, rectangle):
        return img.crop((rectangle.getX(), rectangle.getY(), rectangle.getX() + rectangle.getWidth(), rectangle.getY() + rectangle.getHeight()))
        
        