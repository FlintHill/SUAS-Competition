from PIL import Image
from SyntheticDataset2.ElementsCreator.shape_types import ShapeTypes

class ShapeOrientator(object):
    """
    Based on the intended orientation of a certain feature of a shape,
    return the degree that a shape needs to be rotated as it is created.
    Different shapes use different features as benchmarks.

    Shapes that use angles as benchmarks:
        quarter_circle,
        triangle,
        square,
        pentagon,
        hexagon,
        heptagon,
        octagon,
        star

    Shapes that use sides as benchmarks:
        half_circle,
        cross (convex side),
        rectangle (shorter side),
        trapezoid (shorter side)

    Circles do not need to rotate.

    Rotation inputs:

    N -> north
    E -> east
    S -> south
    W -> west
    NE -> northeast
    SE -> southeast
    SW -> southwest
    NW -> northwest
    NS -> north-south
    EW -> east-west
    D -> diagonal

    :param shape_image: the image of a shape
    :param shape_type: the type of the shape
    :param shape_orientation: the intended orientation of the shape (orientation is explained above)
    :type shape_image: an image file
    :type shape_type: a string (see ShapeTypes)
    :type shape_orientation: a string (see explanation above)
    """

    @staticmethod
    def orientate_shape(shape_type, shape_orientation):
        if shape_type == ShapeTypes.QUARTERCIRCLE:
            if shape_orientation == "N":
                return 135

            if shape_orientation == "NE":
                return 90

            if shape_orientation == "E":
                return 45

            if shape_orientation == "SE":
                return 0

            if shape_orientation == "S":
                return -45

            if shape_orientation == "SW":
                return -90

            if shape_orientation == "W":
                return -135

            if shape_orientation == "NW":
                return 180

        if shape_type == ShapeTypes.HALFCIRCLE:
            if shape_orientation == "N":
                return 180

            if shape_orientation == "E":
                return 90

            if shape_orientation == "S":
                return 0

            if shape_orientation == "W":
                return -90

        if shape_type == ShapeTypes.CROSS:
            if shape_orientation == "N":
                return 0

            if shape_orientation == "D":
                return 45

        if shape_type == ShapeTypes.TRIANGLE:
            if shape_orientation == "N":
                return 0

            if shape_orientation == "S":
                return 60

        if shape_type == ShapeTypes.SQUARE:
            if shape_orientation == "N":
                return 45

            if shape_orientation == "D":
                return 0

        if shape_type == ShapeTypes.RECTANGLE:
            if shape_orientation == "NS":
                return 0

            if shape_orientation == "EW":
                return 90

        if shape_type == ShapeTypes.TRAPEZOID:
            if shape_orientation == "N":
                return 0

            if shape_orientation == "S":
                return 180

        if shape_type == ShapeTypes.PENTAGON:
            if shape_orientation == "N":
                return 36

            if shape_orientation == "S":
                return 0

        if shape_type == ShapeTypes.HEXAGON:
            if shape_orientation == "N":
                return 0

            if shape_orientation == "D":
                return 30

        if shape_type == ShapeTypes.HEPTAGON:
            if shape_orientation == "N":
                return 180

            if shape_orientation == "S":
                return 0

        if shape_type == ShapeTypes.OCTAGON:
            if shape_orientation == "N":
                return 0

            if shape_orientation == "D":
                return 22.5

        if shape_type == ShapeTypes.STAR:
            if shape_orientation == "N":
                return 180

            if shape_orientation == "S":
                return 0
