from SyntheticDataset2.ElementsCreator.shape_orientations import ShapeOrientations

class CardinalDirectionConverter(object):

    @staticmethod
    def convert_to_cardinal_direction(degree):
        """
        Take a direction in degree and output its cardinal direction.
        """
        if degree <= 22.5 or degree >= 337.5:
            return ShapeOrientations.NORTH

        if degree > 22.5 and degree < 67.5:
            return ShapeOrientations.NORTHWEST

        if degree >= 67.5 and degree <= 112.5:
            return ShapeOrientations.WEST

        if degree > 112.5 and degree < 157.5:
            return ShapeOrientations.SOUTHWEST

        if degree >= 157.5 and degree <= 202.5:
            return ShapeOrientations.SOUTH

        if degree > 202.5 and degree < 247.5:
            return ShapeOrientations.SOUTHEAST

        if degree >= 247.5 and degree <= 292.5:
            return ShapeOrientations.EAST

        if degree > 292.5 and degree < 337.5:
            return ShapeOrientations.NORTHEAST
