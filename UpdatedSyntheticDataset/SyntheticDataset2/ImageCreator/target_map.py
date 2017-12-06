from PIL import Image
import random, json
from .settings import Settings
from .random_target import RandomTarget
from SyntheticDataset2.ImageOperations.shape_rotator import ShapeRotator
from SyntheticDataset2.ImageOperations.image_resizer import ImageResizer
from SyntheticDataset2.ImageOperations.cardinal_direction_converter import CardinalDirectionConverter
from SyntheticDataset2.ElementsCreator.background import BackgroundGenerator
from SyntheticDataset2.ElementsCreator.noised_image_generator import NoisedImageGenerator
from SyntheticDataset2.logger import Logger

class TargetMap(object):

    def __init__(self, number_of_targets, shape_type, shape_orientation, letter, shape_color, letter_color, rotation):
        """
        :param number_of_targets: the number of targets to be created.
        :type number_of_targets: int
        """
        self.number_of_targets = number_of_targets
        self.background = BackgroundGenerator(Settings.BACKGROUND_DIRECTORY_PATH).generate_full_background()

        self.shape_type = shape_type
        self.shape_orientation = shape_orientation
        self.letter = letter
        self.shape_color = shape_color
        self.letter_color = letter_color
        self.rotation = rotation

        self.size_range = [Settings.TARGET_GENERATION_SIZE_IN_PIXELS, Settings.TARGET_GENERATION_SIZE_IN_PIXELS]
        self.proportionality_range = Settings.PROPORTIONALITY_RANGE
        self.pixelization_level = Settings.PIXELIZATION_LEVEL
        self.noise_level = Settings.NOISE_LEVEL

        self.target_list = []
        self.total_targets_output = 0

    def create_random_target_map(self):
        """
        Create a map with a specified number of random targets.

        1. Pick an image from path_to_backgrounds as the background.
        2. Generate a random target.
        3. Pick a random location for the target.
        4. With a list of the ranges of previously generated targets,
           Check if the random location overlaps with other targets.
           If so, pick another random location until the newly generated
           location does not overlap or the number of attempts runs out.
           If the attempts runs out, give up on that round.
        5. Store the range of the confirmed random target into the list.
        6. Continue to generate targets until the number of random targets
           is reached. The given-up rounds are counted.
        7. Output the actually targets created and the background itself.
        """
        occupied_spaces = []
        index_number_of_targets = 1

        while index_number_of_targets <= self.number_of_targets:

            random_target = RandomTarget(self.shape_type, self.shape_orientation, self.letter, self.size_range, self.proportionality_range, self.shape_color, self.letter_color, self.rotation, self.pixelization_level, self.noise_level)

            raw_target_image = random_target.create_random_target()
            new_target_dimension = random.randint(Settings.TARGET_SIZE_RANGE_IN_PIXELS[0], Settings.TARGET_SIZE_RANGE_IN_PIXELS[1])

            if raw_target_image.width >= raw_target_image.height:
                new_target_width = new_target_dimension
                new_target_height = new_target_dimension * raw_target_image.height / raw_target_image.width
            else:
                new_target_height = new_target_dimension
                new_target_width = new_target_dimension * raw_target_image.width / raw_target_image.height

            target_image = raw_target_image.resize((new_target_width, new_target_height))

            reroll_needed = True
            attempts_to_reroll = 0

            while reroll_needed == True and attempts_to_reroll < 5:
                reroll_needed = False
                random_x_initial = random.randint(10, self.background.width - target_image.width - 10) - 10
                random_y_initial = random.randint(10, self.background.height - target_image.height - 10) - 10
                random_x_final = random_x_initial + target_image.width + 10
                random_y_final = random_y_initial + target_image.height + 10
                x_taking = [random_x_initial, random_x_final]
                y_taking = [random_y_initial, random_y_final]

                if len(occupied_spaces) > 0:
                    for index_1 in range(0, len(occupied_spaces)):
                        if (x_taking[0] >= occupied_spaces[index_1][0]) and (x_taking[0] <= occupied_spaces[index_1][2]):
                            if (y_taking[0] >= occupied_spaces[index_1][1]) and (y_taking[0] <= occupied_spaces[index_1][3]):
                                reroll_needed = True
                            if ((y_taking[0] + (target_image.height / 4)) >= occupied_spaces[index_1][1]) and ((y_taking[0] + (target_image.height / 4)) <= occupied_spaces[index_1][3]):
                                reroll_needed = True
                            if (((y_taking[0] + y_taking[1]) / 2) >= occupied_spaces[index_1][1]) and (((y_taking[0] + y_taking[1]) / 2) <= occupied_spaces[index_1][3]):
                                reroll_needed = True
                            if ((y_taking[0] + (target_image.height * 3 / 4)) >= occupied_spaces[index_1][1]) and ((y_taking[0] + (target_image.height * 3 / 4)) <= occupied_spaces[index_1][3]):
                                reroll_needed = True
                            if (y_taking[1] >= occupied_spaces[index_1][1]) and (y_taking[1] <= occupied_spaces[index_1][3]):
                                reroll_needed = True

                        if ((x_taking[0] + (target_image.width / 4)) >= occupied_spaces[index_1][0]) and ((x_taking[0] + (target_image.width / 4)) <= occupied_spaces[index_1][2]):
                            if (y_taking[0] >= occupied_spaces[index_1][1]) and (y_taking[0] <= occupied_spaces[index_1][3]):
                                reroll_needed = True
                            if ((y_taking[0] + (target_image.height / 4)) >= occupied_spaces[index_1][1]) and ((y_taking[0] + (target_image.height / 4)) <= occupied_spaces[index_1][3]):
                                reroll_needed = True
                            if (((y_taking[0] + y_taking[1]) / 2) >= occupied_spaces[index_1][1]) and (((y_taking[0] + y_taking[1]) / 2) <= occupied_spaces[index_1][3]):
                                reroll_needed = True
                            if ((y_taking[0] + (target_image.height * 3 / 4)) >= occupied_spaces[index_1][1]) and ((y_taking[0] + (target_image.height * 3 / 4)) <= occupied_spaces[index_1][3]):
                                reroll_needed = True
                            if (y_taking[1] >= occupied_spaces[index_1][1]) and (y_taking[1] <= occupied_spaces[index_1][3]):
                                reroll_needed = True

                        if (((x_taking[0] + x_taking[1]) / 2) >= occupied_spaces[index_1][0]) and (((x_taking[0] + x_taking[1]) / 2) <= occupied_spaces[index_1][2]):
                            if (y_taking[0] >= occupied_spaces[index_1][1]) and (y_taking[0] <= occupied_spaces[index_1][3]):
                                reroll_needed = True
                            if ((y_taking[0] + (target_image.height / 4)) >= occupied_spaces[index_1][1]) and ((y_taking[0] + (target_image.height / 4)) <= occupied_spaces[index_1][3]):
                                reroll_needed = True
                            if (((y_taking[0] + y_taking[1]) / 2) >= occupied_spaces[index_1][1]) and (((y_taking[0] + y_taking[1]) / 2) <= occupied_spaces[index_1][3]):
                                reroll_needed = True
                            if ((y_taking[0] + (target_image.height * 3 / 4)) >= occupied_spaces[index_1][1]) and ((y_taking[0] + (target_image.height * 3 / 4)) <= occupied_spaces[index_1][3]):
                                reroll_needed = True
                            if (y_taking[1] >= occupied_spaces[index_1][1]) and (y_taking[1] <= occupied_spaces[index_1][3]):
                                reroll_needed = True

                        if ((x_taking[0] + (target_image.width * 3 / 4)) >= occupied_spaces[index_1][0]) and ((x_taking[0] + (target_image.width * 3 / 4)) <= occupied_spaces[index_1][2]):
                            if (y_taking[0] >= occupied_spaces[index_1][1]) and (y_taking[0] <= occupied_spaces[index_1][3]):
                                reroll_needed = True
                            if ((y_taking[0] + (target_image.height / 4)) >= occupied_spaces[index_1][1]) and ((y_taking[0] + (target_image.height / 4)) <= occupied_spaces[index_1][3]):
                                reroll_needed = True
                            if (((y_taking[0] + y_taking[1]) / 2) >= occupied_spaces[index_1][1]) and (((y_taking[0] + y_taking[1]) / 2) <= occupied_spaces[index_1][3]):
                                reroll_needed = True
                            if ((y_taking[0] + (target_image.height * 3 / 4)) >= occupied_spaces[index_1][1]) and ((y_taking[0] + (target_image.height * 3 / 4)) <= occupied_spaces[index_1][3]):
                                reroll_needed = True
                            if (y_taking[1] >= occupied_spaces[index_1][1]) and (y_taking[1] <= occupied_spaces[index_1][3]):
                                reroll_needed = True

                        if (x_taking[1] >= occupied_spaces[index_1][0]) and (x_taking[1] <= occupied_spaces[index_1][2]):
                            if (y_taking[0] >= occupied_spaces[index_1][1]) and (y_taking[0] <= occupied_spaces[index_1][3]):
                                reroll_needed = True
                            if ((y_taking[0] + (target_image.height / 4)) >= occupied_spaces[index_1][1]) and ((y_taking[0] + (target_image.height / 4)) <= occupied_spaces[index_1][3]):
                                reroll_needed = True
                            if (((y_taking[0] + y_taking[1]) / 2) >= occupied_spaces[index_1][1]) and (((y_taking[0] + y_taking[1]) / 2) <= occupied_spaces[index_1][3]):
                                reroll_needed = True
                            if ((y_taking[0] + (target_image.height * 3 / 4)) >= occupied_spaces[index_1][1]) and ((y_taking[0] + (target_image.height * 3 / 4)) <= occupied_spaces[index_1][3]):
                                reroll_needed = True
                            if (y_taking[1] >= occupied_spaces[index_1][1]) and (y_taking[1] <= occupied_spaces[index_1][3]):
                                reroll_needed = True

                attempts_to_reroll = attempts_to_reroll + 1

            if reroll_needed == False:

                occupied_spaces.append([random_x_initial - 10, random_y_initial - 10, random_x_final + 10, random_y_final + 10])
                self.target_list.append([random_target, (random_x_initial + random_x_final)/2, (random_y_initial + random_y_final)/2])

                self.background.paste(target_image, (random_x_initial, random_y_initial), target_image)
                index_number_of_targets = index_number_of_targets + 1
                self.total_targets_output = self.total_targets_output + 1
            else:
                index_number_of_targets = index_number_of_targets + 1

        if self.total_targets_output < self.number_of_targets:
            Logger.log("Total Number of Actual Target Output: " + str(self.total_targets_output) + "\n"
                       + "The background is not able to contain the number of targets requested." + "\n")
        else:
            Logger.log("Total Number of Actual Target Output: " + str(self.total_targets_output) + "\n")

        return self.total_targets_output

    def record_random_target_map(self, index_number):
        data = {}
        data["targets"] = []
        for index in range (self.total_targets_output):
            data["targets"].append({
                "shape_type": self.target_list[index][0].shape_type,
                "shape_color": self.target_list[index][0].shape_color,
                "alphanumeric_value": self.target_list[index][0].letter,
                "alphanumeric_color": self.target_list[index][0].letter_color,
                "orientation in degree from north": self.target_list[index][0].rotation,
                "cardinal orientation": CardinalDirectionConverter.convert_to_cardinal_direction(self.target_list[index][0].rotation),
                "target_center_coordinates": (self.target_list[index][1], self.target_list[index][2])
            })

        with open(Settings.SAVE_PATH + Settings.ANSWERS_DIRECTORY + "/target_maps_answers/" + str(index_number) + ".json", 'w') as outfile:
            json.dump(data, outfile, indent=4)
        self.background.save(Settings.SAVE_PATH + Settings.ANSWERS_DIRECTORY + "/target_maps/" + str(index_number) + ".jpg")
