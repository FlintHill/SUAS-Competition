from SUASImageParser.ADLC import ADLCParser
import cv2
import os

class ADLCOptimizer:

    def __init__(self, **kwargs):
        self.debug = kwargs.get("debug", False)

    def optimize(self, output_file, img_directory):
        """
        This creates the optimization data and optimizes the ADLC parser to
        perform with the best results. It then saves that data so that future
        runs of the program use the optimized settings.
        """
        # get starting parameters

        # get ranges

        # get accuracy

        # for each possible combo, run with the set of params
        images = self.load_images(img_directory)

        # return params
        return {"test" : "empty"}

    def score(self):
        """
        Compare proposed target and the actual solution.

        Returns:
        - True/False if the target is correct
        """
        pass

    def load_images(self, img_directory=None):
        """
        Load an image and its known solutions
        """
        if img_directory == None:
            raise ValueError('load_image() cannot be passed a directory with type None')

        for dir in next(os.walk(img_directory))[1]:
            print(dir)

        for file in next(os.walk(img_directory))[2]:
            print(file)

        return []

    def run_params(self, image):
        """
        Run an image through the ADLC Parser, score all of the components found,
        return the resulting information.
        """
        pass
