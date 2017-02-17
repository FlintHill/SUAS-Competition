from PIL import Image
import NoiseReduction.GaussianBlur as GaussianBlur
from EdgeProcessing.SobelEdge import SobelEdge
import EdgeProcessing.CannyEdge as CannyEdge
from Stat.KMeans import KMeans
import Color.ColorMath as ColorMath
from Color.ColorSplitter import ColorSplitter

shapeImg = Image.open("/Users/phusisian/Desktop/Senior year/SUAS/Object images/300 crop 6480x4320.jpeg")
#shapeImg = shapeImg.resize((shapeImg.size[0]/4, shapeImg.size[1]/4))
kmeans = KMeans.init_with_img(shapeImg, shapeImg.load(), 3, 20, 3)
ColorMath.round_img_to_colors(shapeImg, shapeImg.load(), kmeans.get_cluster_origins_int())
shapeImg.show()

color_splitter = ColorSplitter(shapeImg, shapeImg.load())
'''shapeImg = shapeImg.convert('L')
shapeImg = GaussianBlur.get_gaussian_filtered_bw_img(shapeImg, shapeImg.load(), 5, 5)
shapeImg.show()
shapeImage = shapeImg.load()


sobel = SobelEdge(shapeImg)
cannyImg = CannyEdge.get_canny_img(sobel, (20, 40))
cannyImg.show()'''