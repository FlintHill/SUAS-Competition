from SUASImageParser.ADLC import ADLCParser
from SUASImageParser.utils.color import bcolors
import cv2
import numpy as np
import os
import timeit
import json

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

        self.total_time = 0.0

        self.ADLC_parser = ADLCParser()
        images = self.load_images(img_directory)

        # return optimized parameters
        optimized_params, score = self.run_optimization(images, parameters)
        return optimized_params

    def run_optimization(self, images, parameters):
        """
        Run optimization on a given set of parameters and images.
        """
        best_score = -1.0
        best_params = {}

        scenarios = self.create_scenarios(0, [], parameters)

        if self.debug:
            print(bcolors.INFO + "[Info]" + bcolors.ENDC + " Calculated " + str(len(scenarios)) + " scenarios to run")

        self.scenario_index = 0
        self.num_scenarios = len(scenarios)
        for scenario in scenarios:
            self.scenario_index += 1
            score = self.run_params(images, scenario)

            if score > best_score:
                best_params = scenario
                best_score = score

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

    def score(self, test, correct):
        """
        Compare proposed target and the actual solution.

        Returns:
        - How many of the targets are correctly found. For every FA
        """
        score = 0.0
        for test_img in test:
            num_pixels = float(len(test_img))
            best_img_score = 0.0
            x,y,w,h = cv2.boundingRect(test_img)

            for correct_img in correct:
                area = float(correct_img["x_finish"] - correct_img["x_start"]) * float(correct_img["y_finish"] - correct_img["y_start"])
                img_score = 0.0

                SI = max(0, max(x + w, correct_img["x_finish"]) - min(x, correct_img["x_start"])) * max(0, max(y + h, correct_img["y_finish"]) - min(y, correct_img["y_start"]))
                img_score = float(h * w) + area - SI

                """for point in test_img:
                    if point[0] > int(correct_img["y_start"]) and point[0] < int(correct_img["y_finish"]):
                        if point[1] > int(correct_img["x_start"]) and point[1] < int(correct_img["x_finish"]):
                            img_score += 1.0 / num_pixels
                """

                if img_score > best_img_score:
                    best_img_score = img_score

            score += best_img_score

        return score / float(len(correct))

    def load_images(self, img_directory=None):
        """
        Load an image and its known solutions
        """
        if img_directory == None:
            raise ValueError('load_image() cannot be passed a directory with type None')

        if self.debug:
            num_images = 0
            for dir in next(os.walk(img_directory))[1]:
                for file in next(os.walk(img_directory + dir + "/"))[2]:
                    if file.endswith(".jpg"):
                        num_images += 1
            print(bcolors.INFO + "[Info]" + bcolors.ENDC + " Loading " + str(num_images) + " images")

        # The storage for images uses the following structure:
        # [
        #   [full_image, target_1, target_2, target_3, target_4],
        #   [full_image, target_1, target_2, target_3, target_4]
        # ]
        images = []
        for dir in next(os.walk(img_directory))[1]:
            new_img_set = []
            for file in next(os.walk(img_directory + dir + "/"))[2]:
                path = img_directory + dir + "/" + file

                if "image" in file and file.endswith(".jpg"):
                    new_img_set = [cv2.imread(path)] + new_img_set
                elif file.endswith(".txt"):
                    with open(path) as data_file:
                        new_img_set.append(json.load(data_file))

            images.append(new_img_set)

        if self.debug:
            print(bcolors.INFO + "[Info]" + bcolors.ENDC + " Images successfully loaded")

        return images

    def run_params(self, images, parameters):
        """
        Run an image through the ADLC Parser, score all of the components found,
        return the resulting information.
        """
        if self.debug:
            print()
            print(bcolors.INFO + "[Info]" + bcolors.ENDC + " Running scenario " + str(self.scenario_index) + " of " + str(self.num_scenarios))

        scores = 0.0
        img_index = 0
        for image in images:
            img_index += 1
            test_image = image[0]
            self.ADLC_parser.setup(parameters)

            if self.debug:
                start_time = timeit.default_timer()

            targets, _, contours = self.ADLC_parser.parse(test_image)
            score = self.score(contours, image[1:])
            scores += score

            if score > 0.0:
                for target in targets:
                    cv2.imshow("target", target)
                    cv2.waitKey(0)
                    cv2.destroyAllWindows()

            if self.debug:
                end_time = timeit.default_timer()
                image_run_time = end_time - start_time
                self.total_time += image_run_time

            if self.debug:
                print(bcolors.INFO + "[Info]" + bcolors.ENDC + " Image number " + str(img_index) + " scored a " + str(score*100) + "% (" + str(image_run_time) + " seconds)")

        scores = scores / float(len(images))

        if self.debug:
            print(bcolors.INFO + "[Info]" + bcolors.ENDC + " Scenario " + str(self.scenario_index) + " got a score of " + str(scores*100) + "%")
            estimated_time_remaining = float(self.num_scenarios) * self.total_time / (3600.0 * self.scenario_index)
            print(bcolors.INFO + "[Info]" + bcolors.ENDC + " Estimated time remaining: " + str(estimated_time_remaining) + " hours")

        return scores
