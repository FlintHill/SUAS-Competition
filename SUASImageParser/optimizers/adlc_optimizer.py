from SUASImageParser.ADLC import ADLCParser
import cv2

class ADLCOptimizer:

    def __init__(self, **kwargs):
        self.debug = kwargs.get("debug", False)

    def optimize(self):
        """
        This creates the optimization data and optimizes the ADLC parser to
        perform with the best results. It then saves that data so that future
        runs of the program use the optimized settings.
        """
        # get starting parameters

        # for each possible combo, run with the set of params

        # return params

    def score(self):
        """
        Compare proposed target and the actual solution.

        Returns:
        - True/False if the target is correct
        - x/5 for number of characteristics correct
        """
        pass

    def load_image(self):
        """
        Load an image and its known solutions
        """
        pass

    def run_params(self, image):
        """
        Run an image through the ADLC Parser, score all of the components found,
        return the resulting information.
        """
        pass
