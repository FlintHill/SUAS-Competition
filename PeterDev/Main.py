from PIL import Image
from root.nested import KMeans
from root.nested import EdgeDetection
import ObjectDetection
import Rectangle
import Paint
import ShapeCharacteristics

img = Image.open("/Users/phusisian/Desktop/Senior year/SUAS/Object images/300 crop 6480x4320.jpeg")
#img.show()
image = img.load()
dim = img.size

paint = Paint.Paint()
kmeans = KMeans.KMeans()
edgeDetection = EdgeDetection.EdgeDetection()
objDetection = ObjectDetection.ObjectDetection()
shapeChar = ShapeCharacteristics.ShapeCharacteristics()
kmeansImage = kmeans.getKMeans(img,2, 5)
edges = edgeDetection.getKMeansEdges(kmeansImage)
borderImage = edgeDetection.drawEdges(edges, (255,0,0))
borderImage.show()
rect = Rectangle.Rectangle(0,0,dim[0],dim[1])
borderImage = objDetection.drawBoundedObjects(borderImage, edges, rect)
newRect = Rectangle.Rectangle(13,15,174,165)
layers = objDetection.getImageLayers(edges, rect)
objDetection.fillLayers(layers).show()
singleLayerPic = objDetection.fillLayer(layers, 1, (0,0,255))


#print(shapeChar.countSides(singleLayerPic,  objDetection.getLayerBounds(layers, 1)))
print(shapeChar.countSidesWithLayer(layers, objDetection.getLayerBounds(layers, 1)))
paint.drawRectangle(singleLayerPic, objDetection.getLayerBounds(layers, 1), (0,255,0))
singleLayerPic.show()
kmeansImage.show()
#borderImage.show()