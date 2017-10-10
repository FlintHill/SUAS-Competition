from SyntheticDataset2.ElementsCreator import *
import unittest
from PIL import Image

class UpdatedSyntheticDatasetShapesTestCase(unittest.TestCase):


    def test_rectangle(self):
        width = 100
        height = 50
        color = (255,0,0)
        rotation = 45
        midpoint = (250,250)
        test_background = Image.new('RGBA', (500,500), color=(0,0,255))

        test_rectangle = Rectangle(width, height, color, rotation)
        self.assertEqual(test_rectangle.draw().getpixel((50,25)), (255,0,0,255))

        test_rectangle.overlay(midpoint, test_background)
        self.assertEqual(test_background.getpixel(midpoint), (255,0,0,255))

    def test_triangle(self):
        base = 100
        height = 100
        color = (255,0,0)
        rotation = 45
        midpoint = (250,250)
        test_background = Image.new('RGBA', (500,500), color=(0,0,255))

        test_triangle = Triangle(base,height,color,rotation)
        self.assertEqual(test_triangle.draw().getpixel((100,100)), (255,0,0,255))

        test_triangle.overlay(midpoint, test_background)
        self.assertEqual(test_background.getpixel(midpoint), (255,0,0,255))

    def test_circle(self):
        radius = 100
        color = (255,0,0)
        midpoint = (250,250)
        test_background = Image.new('RGBA', (500,500), color=(0,0,255))

        test_circle = Circle(radius,color)
        self.assertEqual(test_circle.draw().getpixel((50,25)), (255,0,0,255))

        test_circle.overlay(midpoint, test_background)
        self.assertEqual(test_background.getpixel(midpoint), (255,0,0,255))

    def test_half_circle(self):
        radius = 100
        color = (255,0,0)
        rotation = 45
        midpoint = (250,250)
        test_background = Image.new('RGBA', (500,500), color=(0,0,255))

        test_half_cirlce = HalfCircle(radius,color,rotation)
        self.assertEqual(test_half_cirlce.draw().getpixel((100,100)), (255,0,0,255))

        test_half_cirlce.overlay(midpoint, test_background)
        self.assertEqual(test_background.getpixel(midpoint), (255,0,0,255))

    def test_square(self):
        base = 100
        color = (255,0,0)
        rotation = 45
        midpoint = (250,250)
        test_background = Image.new('RGBA', (500,500), color=(0,0,255))

        test_square = Square(base,color,rotation)
        self.assertEqual(test_square.draw().getpixel((50,25)), (255,0,0,255))

        test_square.overlay(midpoint, test_background)
        self.assertEqual(test_background.getpixel(midpoint), (255,0,0,255))

    def test_trapezoid(self):
        base1 = 75
        base2 = 100
        height = 100
        color = (255,0,0)
        rotation = 45
        midpoint = (250,250)
        test_background = Image.new('RGBA', (500,500), color=(0,0,255))

        test_trapezoid = Trapezoid(base1,base2,height,color,rotation)
        self.assertEqual(test_trapezoid.draw().getpixel((50,25)), (255,0,0,255))

        test_trapezoid.overlay(midpoint, test_background)
        self.assertEqual(test_background.getpixel(midpoint), (255,0,0,255))

    def test_quarter_circle(self):
        radius = 100
        color = (255,0,0)
        rotation = 45
        midpoint = (250,250)
        test_background = Image.new('RGBA', (500,500), color=(0,0,255))

        test_quarter_circle = QuarterCircle(radius,color,rotation)
        self.assertEqual(test_quarter_circle.draw().getpixel((100,100)), (255,0,0,255))

        test_quarter_circle.overlay(midpoint, test_background)
        self.assertEqual(test_background.getpixel(midpoint), (255,0,0,255))

    def test_cross(self):
        height = 100
        color = (255,0,0)
        rotation = 45
        midpoint = (250,250)
        test_background = Image.new('RGBA', (500,500), color=(0,0,255))

        test_cross = Cross(height,color,rotation)
        self.assertEqual(test_cross.draw().getpixel((100,100)), (255,0,0,255))

        test_cross.overlay(midpoint, test_background)
        self.assertEqual(test_background.getpixel(midpoint), (255,0,0,255))

    def test_pentagon(self):
        radius = 100
        color = (255,0,0)
        rotation = 45
        midpoint = (250,250)
        test_background = Image.new('RGBA', (500,500), color=(0,0,255))

        test_pentagon = Pentagon(radius,color,rotation)
        self.assertEqual(test_pentagon.draw().getpixel((150,150)), (255,0,0,255))

        test_pentagon.overlay(midpoint, test_background)
        self.assertEqual(test_background.getpixel(midpoint), (255,0,0,255))

    def test_star(self):
        radius = 100
        color = (255,0,0)
        rotation = 45
        midpoint = (250,250)
        test_background = Image.new('RGBA', (500,500), color=(0,0,255))

        test_star = Star(radius,color,rotation)
        self.assertEqual(test_star.draw().getpixel((150,150)), (255,0,0,255))

        test_star.overlay(midpoint, test_background)
        self.assertEqual(test_background.getpixel(midpoint), (255,0,0,255))

    def test_hexagon(self):
        radius = 100
        color = (255,0,0)
        rotation = 45
        midpoint = (250,250)
        test_background = Image.new('RGBA', (500,500), color=(0,0,255))

        test_hexagon = Hexagon(radius,color,rotation)
        self.assertEqual(test_hexagon.draw().getpixel((150,150)), (255,0,0,255))

        test_hexagon.overlay(midpoint, test_background)
        self.assertEqual(test_background.getpixel(midpoint), (255,0,0,255))

    def test_heptagon(self):
        radius = 100
        color = (255,0,0)
        rotation = 45
        midpoint = (250,250)
        test_background = Image.new('RGBA', (500,500), color=(0,0,255))

        test_heptagon = Heptagon(radius,color,rotation)
        self.assertEqual(test_heptagon.draw().getpixel((150,150)), (255,0,0,255))

        test_heptagon.overlay(midpoint, test_background)
        self.assertEqual(test_background.getpixel(midpoint), (255,0,0,255))

    def test_octagon(self):
        radius = 100
        color = (255,0,0)
        rotation = 45
        midpoint = (250,250)
        test_background = Image.new('RGBA', (500,500), color=(0,0,255))

        test_octagon = Octagon(radius,color,rotation)
        self.assertEqual(test_octagon.draw().getpixel((150,150)), (255,0,0,255))

        test_octagon.overlay(midpoint, test_background)
        self.assertEqual(test_background.getpixel(midpoint), (255,0,0,255))
