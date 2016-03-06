import cv2

def row_column_sum(self, img, constraints):
    """
    Sums the rows and columns of the image "img" using the "constraints" as
    a means to determine what to sum. Returns the list
    [rows_small, columns_small], [rows_high, columns_high] where rows_small is
    a list of rows that have a below average sum (as determined by the
    summer), columns_small is a list of columns that have a below average
    sum (as determined by the summer), rows_high is a list of rows that have a
    greater than average sum (as determined by the summer), and columns_high
    is a list of columns that have a greater than average sum (as determined
    by the summer).
    """
    # @TODO: Implement row & column summing

    # Returning the rows and columns that are above and below average
    return [[], []], [[], []]
