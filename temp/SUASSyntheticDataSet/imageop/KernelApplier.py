from imageop.Point import Point

class KernelApplier:
    
    '''applies the kernel with an added field in the convolution for the color's alpha'''
    @staticmethod
    def getImgAppliedWithKernelWithAlpha(imgIn, imageIn, kernel):
        img = imgIn.copy()
        image = img.load()
        margin = (len(kernel)-1)/2
        kernelSum = KernelApplier.getKernelSum(kernel)
        for x in range(margin, img.size[0] - margin):
            for y in range(margin, img.size[1] - margin):
                image[x,y] = KernelApplier.applyKernelToPixelWithAlpha(Point(x,y), img, image, kernel, kernelSum)
        return img
    
    '''applies the kernel only accounting for color r,g, and b, no alpha'''
    @staticmethod
    def getImgAppliedWithKernel(imgIn, imageIn, kernel):
        img = imgIn.copy()
        image = img.load()
        margin = (len(kernel)-1)/2
        kernelSum = KernelApplier.getKernelSum(kernel)
        for x in range(margin, img.size[0] - margin):
            for y in range(margin, img.size[1] - margin):
                image[x,y] = KernelApplier.applyKernelToPixel(Point(x,y), img, image, kernel, kernelSum)
                    
        return img
              
    '''really meant to be used by kerneling algorithms, no use outside of that'''  
    @staticmethod
    def applyKernelToPixelWithAlpha(pixelPoint, img, image, kernel, kernelSum): 
        initOffset = (len(kernel) - 1)/2
        kernelArea = len(kernel) * len(kernel[0])
        redAdd = 0
        greenAdd = 0
        blueAdd = 0
        alphaAdd = 0
        kernelX = 0
        kernelY = 0
        for x in range(pixelPoint.getX() - initOffset, pixelPoint.getX() + initOffset + 1):
            for y in range(pixelPoint.getY() - initOffset, pixelPoint.getY() + initOffset + 1):
                redAdd += image[x,y][0] * kernel[kernelX][kernelY]
                greenAdd += image[x,y][1] * kernel[kernelX][kernelY]
                blueAdd += image[x,y][2] * kernel[kernelX][kernelY]
                alphaAdd += image[x,y][3] * kernel[kernelX][kernelY]
                kernelY += 1
            kernelY = 0
            kernelX += 1
        redAdd = int(redAdd)
        greenAdd = int(greenAdd)
        alphaAdd = int(alphaAdd)
        blueAdd = int(blueAdd)
        return (redAdd, greenAdd, blueAdd, alphaAdd)
    
    '''really meant to be used by kerneling algorithms, no use outside of that'''    
    @staticmethod
    def applyKernelToPixel(pixelPoint, img, image, kernel, kernelSum): 
        initOffset = (len(kernel) - 1)/2
        kernelArea = len(kernel) * len(kernel[0])
        redAdd = 0
        greenAdd = 0
        blueAdd = 0
        kernelX = 0
        kernelY = 0
        for x in range(pixelPoint.getX() - initOffset, pixelPoint.getX() + initOffset + 1):
            for y in range(pixelPoint.getY() - initOffset, pixelPoint.getY() + initOffset + 1):
                redAdd += image[x,y][0] * kernel[kernelX][kernelY]
                greenAdd += image[x,y][1] * kernel[kernelX][kernelY]
                blueAdd += image[x,y][2] * kernel[kernelX][kernelY]
                kernelY += 1
            kernelY = 0
            kernelX += 1
        redAdd = int(redAdd)
        greenAdd = int(greenAdd)
        blueAdd = int(blueAdd)
        return (redAdd, greenAdd, blueAdd, image[pixelPoint.getX(), pixelPoint.getY()][3])
    
    '''useful for kernels that must be multiplied by 1/the kernel's sum (such as gaussian blur, had I not applied that to the kernel already)'''
    @staticmethod
    def getKernelSum(kernel):
        kernelAdd = 0
        for x in range(0, len(kernel)):
            for y in range(0, len(kernel[0])):
                kernelAdd += kernel[x][y]
        return kernelAdd