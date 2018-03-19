

class ShapeDetectionSettings(object):

    # shape_classification.py
    CIRCLE_SCORE_THRESHOLD = 0.6
    NOISE_SCORE_THRESHOLD = 0.6
    SQUARE_SIDE_LENGTH_THRESHOLD = 2
    TRAPEZOID_AREA_THRESHOLD = 125
    SQUARE_RECTANGLE_EIGEN_RATIO_THRESHOLD = 1.5
    PENTAGON_STAR_CLUSTER_THRESHOLD = 8
    OCTAGON_CROSS_CLUSTER_THRESHOLD = 10

    QUARTER_CIRCLE_HOUGH_THRESHOLD = 20
    QUADRILATERAL_HOUGH_THRESHOLD = 10

    SHAPE_CHOICES = ("circle", "semicircle", "quarter_circle", "triangle", "square", "rectangle", "trapezoid", "pentagon", "hexagon", "heptagon", "octagon", "star", "cross")
    SHAPE_COMPARISON_CHOICES = ("semicircle", "quarter_circle", "triangle", "square", "rectangle", "trapezoid", "pentagon", "hexagon", "heptagon", "octagon", "star", "cross")

    # polar_side_counter.py
    CIRCLE_DERIV_RANGE = (0.90, 1.10)
    NOISE_DERIV_RANGE = (0.80, 1.20)


    CIRCLE_PATH = "../../../../targets_full_dataset/circle/6.png"
