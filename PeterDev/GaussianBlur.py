from PIL import Image
import math
from root.nested.KernelApplier import KernelApplier

class GaussianBlur:
    
    @staticmethod
    def getGaussianFilteredImg(img, image, kernelSize, stdDev):
        gaussianKernel = GaussianBlur.getGaussianKernel(kernelSize, stdDev)
        applyImg = img.copy()
        applyImage = applyImg.load()
        return KernelApplier.getImgAppliedWithKernel(applyImg, applyImage, gaussianKernel)
        
    @staticmethod
    def getGaussianFilteredImgWithAlpha(img, image, kernelSize, stdDev):
        gaussianKernel = GaussianBlur.getGaussianKernel(kernelSize, stdDev)
        applyImg = img.copy()
        applyImage = applyImg.load()
        return KernelApplier.getImgAppliedWithKernelWithAlpha(applyImg, applyImage, gaussianKernel)
    
    @staticmethod
    def getGaussianKernel(kernelSize, stdDev):
        kernel = [[float(1.0/(2.0 * math.pi * stdDev**2)) for j in range(0, kernelSize)] for i in range(0, kernelSize)]
        kernelX = 0
        kernelY = 0
        kernelMargin = int((kernelSize - 1)/2)
        for x in range(-kernelMargin, kernelMargin + 1):
            for y in range(-kernelMargin, kernelMargin + 1):
                numerator = -float(x**2 + y**2)
                denominator = 2.0*(stdDev**2)
                kernel[kernelX][kernelY] *= math.exp(numerator/denominator)
                kernelY += 1
            kernelY = 0
            kernelX += 1
        sum = KernelApplier.getKernelSum(kernel)
        for x in range(0, kernelSize):
            for y in range(0, kernelSize):
                kernel[x][y] /= sum
        return kernel         