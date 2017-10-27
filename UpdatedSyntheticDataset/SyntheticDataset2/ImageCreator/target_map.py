from PIL import Image
import random
from .settings import Settings
from .random_target import RandomTarget
from SyntheticDataset2.ImageOperations.shape_rotator import ShapeRotator
from SyntheticDataset2.ImageOperations.image_resizer import ImageResizer
from SyntheticDataset2.ElementsCreator.background import BackgroundGenerator
from SyntheticDataset2.ElementsCreator.noised_image_generator import NoisedImageGenerator
from SyntheticDataset2.logger import Logger

class TargetMap(object):

    def __init__(self, number_of_targets):
        """
        :param number_of_targets: the number of targets to be created.
        :type number_of_targets: int
        """
        self.number_of_targets = number_of_targets
        self.background = BackgroundGenerator(Settings.BACKGROUND_DIRECTORY).generate_full_background()
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

            random_target = RandomTarget(self.size_range, self.proportionality_range, self.pixelization_level, self.noise_level)

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

        Logger.log("Total Number of Actual Target Output: " + str(self.total_targets_output))
        if self.total_targets_output < self.number_of_targets:
            Logger.log("The background is not able to contain the number of targets requested.")
        return self.background

    def record_random_target_map(self):
        text = open(Settings.TEXT_SAVING_PATH + "/tester.txt", "a")
        text.write("Total Number of Actual Target Output: " + str(self.total_targets_output))

        for index in range (self.total_targets_output):
            text.write("\n\n" + "Shape Type: " + str(self.target_list[index][0].random_shape_type)
                       + "\nAlphanumeric Value: " + str(self.target_list[index][0].random_letter)
                       + "\nShape Color: " + str(self.target_list[index][0].random_shape_color)
                       + "\nAlphanumeric Color: " + str(self.target_list[index][0].random_letter_color)
                       + "\nOrientation: " + str(self.target_list[index][0].random_rotation)
                       + "\nCenter of Target: (" + str(self.target_list[index][1]) + ", " + str(self.target_list[index][2]) + ")")

        self.background.save(Settings.IMAGE_SAVING_PATH + "/tester.PNG")
