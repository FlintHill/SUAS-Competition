from SUASImageParser.ADLC import ADLCParser
import cv2
import numpy as np
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
        # To set the parameters, provide the following
        # "PARAM_NAME" : {
        #   "STARTING_VAL" : STARTING_VALUE,
        #   "MIN_VAL" : MINIMUM_VALUE,
        #   "MAX_VAL" : MAXIMUM_VALUE,
        #   "ACCURACY" : ACCURACY
        # }
        # NOTE: ACCURACY is the number of decimal places you would like the
        #   optimized parameter to be hypertuned to
        parameters = {
            "THRESH_VALUE" : {
                "STARTING_VAL" : 0.0,
                "MIN_VAL" : 0.0,
                "MAX_VAL" : 255.0,
                "ACCURACY" : 0
            },
            "SCALE_FACTOR" : {
                "STARTING_VAL" : 0.0,
                "MIN_VAL" : 0.0,
                "MAX_VAL" : 1.0,
                "ACCURACY" : 2
            }
        }

        self.ADLC_parser = ADLCParser()
        images = self.load_images(img_directory)

        # return optimized parameters
        optimized_params, score = self.run_optimization(images, parameters)
        return optimized_params

    def run_optimization(self, images, parameters):
        """
        Run optimization on a given set of parameters and images.
        """
        best_score = -1
        best_params = {}

        scenarios = self.create_scenarios(0, [], parameters)

        print(len(scenarios))

        for scenario in scenarios:
            params, score = self.run_params(None, scenario)

            if score > best_score:
                best_params = params

        return best_params, best_score

    def create_scenarios(self, index, scenarios, parameters):
        """
        Create scenarios for optimization
        """
        for_index = 0
        for parameter in parameters:
            if for_index == len(parameters) - 1:
                for param_index_val in np.arange(parameters[parameter]["MIN_VAL"], parameters[parameter]["MAX_VAL"], 10**(-1.0 * parameters[parameter]["ACCURACY"])):
                    parameters[parameter]["STARTING_VAL"] = param_index_val

                    scenarios.append(self.extrapolate_scenario(parameters))
            elif for_index == index:
                for param_index_val in np.arange(parameters[parameter]["MIN_VAL"], parameters[parameter]["MAX_VAL"], 10**(-1.0 * parameters[parameter]["ACCURACY"])):
                    parameters[parameter]["STARTING_VAL"] = param_index_val

                    scenarios = self.create_scenarios(for_index + 1, scenarios, parameters)

            for_index += 1

        return scenarios

    def extrapolate_scenario(self, parameters):
        """
        Extrapolate a scenario from a set of parameters.
        """
        scenario = {}
        for parameter in parameters:
            scenario[parameter] = parameters[parameter]["STARTING_VAL"]

        return scenario

    def score(self):
        """
        Compare proposed target and the actual solution.

        Returns:
        - True/False if the target is correct
        """
        return -2

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

    def run_params(self, image, parameters):
        """
        Run an image through the ADLC Parser, score all of the components found,
        return the resulting information.
        """
        targets, characteristics, locations = self.ADLC_parser.parse(image, parameters)

        return {"test" : "empty"}, -10
