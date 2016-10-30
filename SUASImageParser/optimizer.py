from SUASImageParser.optimizers import ADLCOptimizer
from SUASImageParser.utils.color import bcolors
import json
import os

class Optimizer:
    """
    Optimizer for SUAS Image parser. Use this to tune parameters to get the best results.

    author: Vale Tolpegin
    """

    def __init__(self, **kwargs):
        self.debug = kwargs.get("debug", False)
        self.output_file = kwargs.get("output_file", None)
        self.image_directory = kwargs.get("img_directory", None)

        if self.output_file == None:
            raise ValueError('Please specify an output file to save tuned parameters to')

        if self.image_directory == None:
            raise ValueError('Please specify a data directory to get images from')

        self.adlc_optimizer = ADLCOptimizer(debug=self.debug)

    def optimize(self, **kwargs):
        """
        Optimize the parameters
        """
        mode = kwargs.get("mode", None)

        if mode == None:
            raise ValueError('Please specify a mode to use (i.e. "ADLC" if you would like to use the ADLC optimizer)')

        optimized_parameters = {}
        if mode.lower() == "adlc":
            optimized_parameters = self.adlc_optimizer.optimize(self.output_file, self.image_directory)

        self.save_params(optimized_parameters, kwargs.get("output_file"))

    def save_params(self, optimized_parameters, output_file):
        """
        Save the parameters to a file.
        """
        if os.path.exists(output_file):
            if self.debug:
                print(bcolors.WARNING + "[Warning]" + bcolors.ENDC + " Output file already exists")

        with open(output_file, 'w+') as output:
            json.dump(optimized_parameters, output)
