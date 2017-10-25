from PIL import Image
import random
from SyntheticDataset2.ElementsCreator.background import BackgroundGenerator
from .random_target_creator import RandomTargetCreator
from SyntheticDataset2.ImageOperations.shape_rotator import ShapeRotator

class TargetMapCreator(object):

    @staticmethod
    def create_random_target_map(number_of_targets, size_range, proportionality_range, path_to_backgrounds):
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

        :param number_of_targets: the number of targets to be created.
        :param size_range: the range of sizes that are to be selected randomly
        :param proportionality_range: the range of proportionality levels that are to be selected randomly
        :param path_to_backgrounds: the directory of images of background
        :type number_of_targets: int
        :type size_range: [min_size, max_size] //:type min_size and max_size: int
        :type proportionality_range: [min_proportionality, max_proportionality] //:type min_proportionality and max_proportionality: double
        :type path_to_backgrounds: directory
        """

        #background = BackgroundGenerator(max(size_range) * number_of_targets * 2, max(size_range) * number_of_targets * 2, path_to_backgrounds).generate_background()

        background = Image.open(path_to_backgrounds)

        occupied_spaces = []

        index_number_of_targets = 1
        total_targets_output = 0

        while index_number_of_targets <= number_of_targets:
            target_image = RandomTargetCreator.create_random_target(size_range, proportionality_range)
            reroll_needed = True
            attempts_to_reroll = 0

            while reroll_needed == True and attempts_to_reroll < 10:
                reroll_needed = False
                random_x_initial = random.randint(10, background.width - target_image.width - 10) - 10
                random_y_initial = random.randint(10, background.height - target_image.height - 10) - 10
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
                background.paste(target_image, (random_x_initial, random_y_initial), target_image)
                index_number_of_targets = index_number_of_targets + 1
                total_targets_output = total_targets_output + 1
            else:
                index_number_of_targets = index_number_of_targets + 1

        print "Total Number of Target Output: " + str(total_targets_output)
        return background
